import discord
import pendulum
from PIL import Image
from toggl.TogglPy import Toggl, Endpoints
from discord.ext import tasks
import userdatabases
import Toggler
from discord.ext import commands

client = discord.Client()

toggle_channel = 825147812466524180
discordAPI = 

toggler = Toggler

database = userdatabases

toggl = Toggl()


@client.event
async def on_ready():
    print("Logged in as {0.user}!".format(client))
    print('Newer Version I promise')


@client.event
async def on_message(message):
    if message.content.startswith('tbc'):

        arguments = message.content.replace("tbc", "")
        arguments = arguments.strip().split()
        channel_id = message.author.voice.channel.id

        task = userdatabases.get_toggle_task(message.author.id, channel_id)
        goal = userdatabases.get_toggle_task_goal(message.author.id, channel_id) * 60
        print(goal)

        if task is None:
            await message.channel.send(
                "Go into a deep work channel first before you use this function! {0}".format(message.author.mention))
            return

        project_id = task[2]
        task_name = task[3]

        if len(arguments) > 1:
            await message.channel.send("Not today baisaab.")
            return

        toggl.setAPIKey(userdatabases.get_discord_toggl_user_token(message.author.id))

        goal_in_hours = pendulum.duration(minutes=goal).in_hours()

        time_this_week = toggler.get_work_since_monday(toggl, project_id, task_name, pendulum.MONDAY)

        minutes_over = time_this_week - goal

        time_over_in_words = pendulum.duration(minutes=minutes_over).in_words()

        percentage = time_this_week / goal * 100
        sentence = "You have clocked in, {0} out of {1} minutes. \n" \
                   "{2}% Done!".format(time_this_week, goal, percentage)

        if percentage < 10:
            sentence = "{0}% Done of {1} hours for {2}  \n" \
                       "Instead of checking how little work you've done this week, " \
                       "maybe get to work?\n" \
                       "I wasn't asking bitch".format(
                        percentage, goal_in_hours, task_name)
            await send_image(message, 'gru-angry.jpg')
        elif percentage < 20:
            sentence = "{0}% Done of {1} hours \n" \
                       "Why are you even checking?".format(percentage, goal_in_hours)
            await send_image(message, 'catwhat.png')
        elif percentage > 100:
            sentence = "You have achieved your goal of doing {0} hours!" \
                       " With an additional {1}".format(goal_in_hours, time_over_in_words)
            await send_image(message, 'thanos.png')
        await message.channel.send(sentence)

    if message.content.startswith("tb add task"):
        arguments = message.content.replace("tb add task", "")
        arguments = arguments.strip().split()
        if len(arguments) > 2 or len(arguments) <= 1:
            await message.channel.send("Not today baisaab.")
            return
        discord_userid = message.author.id
        task_name = arguments[0]
        project_id = arguments[1]
        channel_id = message.author.voice.channel.id
        userdatabases.add_toggl_task(discord_userid, task_name, project_id, channel_id)


@client.event
async def on_voice_state_update(member, before_state, after):

    channel = client.get_channel(toggle_channel)
    toggl.setAPIKey(userdatabases.get_discord_toggl_user_token(member.id))

    try:
        before_state_task = userdatabases.get_toggle_task(member.id, before_state.channel.id)
    except AttributeError:
        before_state_task = None
    if before_state_task is not None:
        try:
            before_task_prj_name = toggl.getProject(before_state_task[2])['data']['name']
            current_timer_data = toggl.currentRunningTimeEntry()['data']
            current_timer_id = current_timer_data['id']
            current_timer_timer = (pendulum.now() - pendulum.parse(current_timer_data['start'])).in_words()
            toggl.stopTimeEntry(current_timer_id)
            print(current_timer_timer)
            await channel.send("You have clocked in {2}, for {0} - {1}.{3}".format(before_state_task[3],
                                                                                   before_task_prj_name,
                                                                                   current_timer_timer,
                                                                                   member.mention))
        except TypeError:
            print("Type error, before task is probably null.")
    elif before_state_task is None:
        pass
    try:
        after_state_task = userdatabases.get_toggle_task(member.id, after.channel.id)
    except AttributeError:
        print("{0} left the server, timer stopped.".format(member.name))
        return

    if after_state_task is None:
        return
    after_task_prj_name = toggl.getProject(after_state_task[2])['data']['name']
    toggl.startTimeEntry(after_state_task[3], after_state_task[2])
    await channel.send(
        "Started {0} Timer in {1} for {2}".format(after_state_task[3],
                                                  after_task_prj_name,
                                                  member.mention))
    toggl.setAPIKey('Null')


async def send_message(message, to_send):
    await message.channel.send(to_send)


async def send_image(message, to_send):
    await message.channel.send(file=discord.File(to_send))


client.run(discordAPI)
