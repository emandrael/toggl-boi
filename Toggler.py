import pendulum
import userdatabases
from toggl.TogglPy import Toggl, Endpoints

def get_work_since_monday(toggl, projectid, task_description, day):
    if day is None:
        day = pendulum.MONDAY

    pendulum.week_starts_at(wday=day)

    monday = pendulum.now().start_of('day')

    while monday.day_of_week != day:
        monday = monday.subtract(days=1)

    data = {
        'pid': projectid
    }

    request = toggl.request(endpoint=Endpoints.TIME_ENTRIES, parameters=data)
    time = 0
    count = 0
    for time_entry in request:
        count += 1
        if time_entry['duration'] >= 0:
            try:
                entry = pendulum.parse(time_entry['start'])
                if entry > monday:
                    if time_entry['description'] == task_description:
                        time += time_entry['duration']
            except:
                continue
    try:
        time += pendulum.parse(toggl.currentRunningTimeEntry()['data']['start']).diff(pendulum.now()).in_minutes()
    except:
        print('No timer.')
    return pendulum.duration(seconds=time).in_minutes()

toggl = Toggl()
prjID = userdatabases