import sqlite3


# conn.execute('''CREATE TABLE TOGGL_USERS
#    ([Discord_ID] text, [Toggl_API_Token] text)''')

# '''CREATE TABLE TOGGL_USERS
#        ([Discord_ID] text, [Toggl_API_Token] text)'''

def create_databases(name, sql_statement):
    con = sqlite3.connect(name)
    c = con.cursor()
    try:
        con.execute(sql_statement)
    except:
        print("Database Already Exists.")
    con.commit()
    con.close()


def add_discord_toggl_user(discord_id, toggl_api_token):
    conn = sqlite3.connect('UserDatabase.db')
    c = conn.cursor()
    try:
        c.execute("INSERT INTO TOGGL_USERS VALUES (?,?)", (discord_id, toggl_api_token))
    except sqlite3.IntegrityError:
        print("User: {0} already has a Toggl API Token.")
    conn.commit()
    conn.close()
    print('Added user.')


def get_discord_toggl_user_token(discordid):
    conn = sqlite3.connect('UserDatabase.db')
    c = conn.cursor()
    c.execute("SELECT * FROM TOGGL_USERS WHERE Discord_ID IS '{0}'".format(discordid))
    output = c.fetchone()
    conn.close()
    return output[1]


def add_toggl_task(discord_id, task_name, project_id, channel_id):
    conn = sqlite3.connect("UserDatabase.db")
    c = conn.cursor()
    sql = "INSERT INTO TOGGL_TASKS (Discord_ID, Discord_Channel_ID, Toggl_Project_ID, Toggl_Task_Name) VALUES ('{0}','{1}','{2}','{3}')".format(
        discord_id, channel_id, project_id, task_name)
    c.execute(sql)
    conn.commit()
    conn.close()


def get_toggle_task(discord_id, channel_id):
    sql = 'SELECT * FROM TOGGL_TASKS WHERE Discord_ID IS "{0}" AND Discord_Channel_ID is "{1}"'.format(discord_id,
                                                                                                       channel_id)
    conn = sqlite3.connect("UserDatabase.db")
    c = conn.cursor()
    c.execute(sql)
    output = c.fetchone()
    conn.close()
    return output


def get_toggle_task_goal(discord_id, channel_id):
    sql = 'SELECT * FROM TOGGL_TASKS WHERE Discord_ID IS "{0}" AND Discord_Channel_ID is "{1}"'.format(discord_id,
                                                                                                       channel_id)
    conn = sqlite3.connect("UserDatabase.db")
    c = conn.cursor()
    c.execute(sql)
    output = c.fetchone()
    conn.close()
    return output[4]


def get_all_data_from(table):
    conn = sqlite3.connect('UserDatabase.db')
    c = conn.cursor()
    users = c.execute("SELECT * FROM {0}".format(table))
    conn.close()
    return users
