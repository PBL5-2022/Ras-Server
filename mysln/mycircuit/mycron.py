from crontab import CronTab
import os
import sqlite3
my_cron = CronTab(user='pi')
dbname = '/home/pi/MyPBL5/DjangoAPI/mysln/db.sqlite3'


def cronAtSpecificTime(mycommand, id, device, status, timesettings):
    job = my_cron.new(command=mycommand, comment=id)
    print(timesettings)
    listtime = timesettings.split(":")
    print(type(listtime))
    for i in range(len(listtime)):
        if i == 0:
            job.minute.on(int(listtime[i]))
        elif i == 2:
            job.hour.on(int(listtime[i]))
        elif i == 3:
            job.day.on(int(listtime[i]))
        elif i == 4:
            job.month.on(int(listtime[i]))
    my_cron.write()
    iter2 = my_cron.find_comment(id)
    logData(id, device, status, str(next(iter2)))


def listCron():
    for job in my_cron:
        print(job)


def logData(id, device, status, timesetting):

    conn = sqlite3.connect(dbname)
    curs = conn.cursor()

    curs.execute(
        "INSERT INTO myapi_schedule(id,device,timesetting,status,timestamp) values((?), (?), (?),(?) , datetime('now'))", (id, device, timesetting, status))
    conn.commit()
    conn.close()


def removeCron():
    my_cron.remove_all()
    my_cron.write()


if __name__ == "__main__":
    # os.system("lib-circuit 12 --turnon")
    # cronAtSpecificTime("lib-circuit g --turnoffled",
    #                    "i11d22255", "led", "TurnOn", "39")
    listCron()
    removeCron()
