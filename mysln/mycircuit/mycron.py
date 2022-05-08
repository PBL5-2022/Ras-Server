from crontab import CronTab
import os
import sqlite3
my_cron = CronTab(user='pi')
dbname = '/home/pi/Ras-Server/mysln/db.sqlite3'


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
    iter2 = str(next(my_cron.find_comment(id))).split(" ")
    timesetting = f"{iter2[0]} {iter2[1]} {iter2[2]} {iter2[3]} {iter2[4]}"
    logData(id, device, status, timesetting)


def listCron():
    result = ""
    for job in my_cron:
        result += job.comment+":"
    return result[0:len(result)-1]


def printCron():
    for job in my_cron:
        print(job)


def logData(id, device, status, timesetting):

    conn = sqlite3.connect(dbname)
    curs = conn.cursor()

    curs.execute(
        "INSERT INTO myapi_schedule(id,device,timesetting,status,timestamp) values((?), (?), (?),(?) , datetime('now'))", (id, device, timesetting, status))
    conn.commit()
    conn.close()


def removeAllCron():
    my_cron.remove_all()
    my_cron.write()


def removeSpecificCron(id):
    for job in my_cron:
        if job.comment == id:
            my_cron.remove(job)
            my_cron.write()


if __name__ == "__main__":
    # os.system("lib-circuit 1 --offled")
    # cronAtSpecificTime("lib-circuit 1 --onled",
    #                    "i12y224hr", "led", "TurnOn", "49")
    # printCron()
    removeAllCron()
