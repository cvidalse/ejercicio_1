from crontab import CronTab

cron = CronTab(user='root')

job = cron.new(command='/usr/local/bin/python3.7 /mlflow/app/run_controller.py')

job.every(1).minute()

print(job)
cron.write()
