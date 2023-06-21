from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger

from bot.worker.tasks import send_daily_schedule, database_cleanup

scheduler = AsyncIOScheduler()

morning_trigger = CronTrigger(
    month="1-6, 9-12",
    hour="6",
    day_of_week='mon-fri',
    timezone='Europe/Kyiv'
)

cleanup_trigger = CronTrigger(
    hour='2',
    day='last',
    timezone='Europe/Kyiv'
)

scheduler.add_job(send_daily_schedule, trigger=morning_trigger, name="daily schedule")
scheduler.add_job(database_cleanup, trigger=cleanup_trigger, name="cleanup")
