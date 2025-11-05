import os
from datetime import datetime
from celery import Celery
from celery.schedules import crontab

from mobile_network_analytics.schemas.utils import Interval


directory_path = os.environ.get("DIRECTORY_PATH", "/data")
end_timestamp = os.environ.get("END_TIME", None)
end_time = datetime.strptime(end_timestamp, "%Y-%m-%d %H:%M:%S") if end_timestamp else datetime.now()


app = Celery(
    "celery",
    broker="redis://redis:6379/0",
    backend="redis://redis:6379/0",
    include=["mobile_network_analytics.celery.tasks"],
)

app.conf.beat_schedule = {
    "services_kpi_5min": {
        "task": "mobile_network_analytics.celery.tasks.calculate_service_kpis_task",
        "schedule": crontab(minute="1-59/5"),  # runs at minute 1, 6, 11, ... past every hour
        "args" : (directory_path, Interval.FIVE_MINUTE, end_time),
    },
    "services_kpi_1hour": {
        "task": "mobile_network_analytics.celery.tasks.calculate_service_kpis_task",
        "schedule": crontab(minute=1),  # runs at 1 minute past every hour
        "args" : (directory_path, Interval.ONE_HOUR, end_time),
    },
    "cells_kpi_5min": {
        "task": "mobile_network_analytics.celery.tasks.calculate_cell_kpis_task",
        "schedule": crontab(minute="1-59/5"),  # runs at minute 1, 6, 11, ... past every hour
        "args" : (directory_path, Interval.FIVE_MINUTE, end_time),
    },
    "cells_kpi_1hour": {
        "task": "mobile_network_analytics.celery.tasks.calculate_cell_kpis_task",
        "schedule": crontab(minute=1),  # runs at 1 minute past every hour
        "args" : (directory_path, Interval.ONE_HOUR, end_time),
    },
}
