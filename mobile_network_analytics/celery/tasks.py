from datetime import datetime
from mobile_network_analytics.celery.celery import app
from mobile_network_analytics.data_ingestion.file_extraction_utils import get_interval_files, get_time_window
from mobile_network_analytics.data_ingestion.file_parsing_utils import (
    calculate_cells_kpis,
    calculate_services_kpis,
    parse_files,
)
from mobile_network_analytics.db import get_db_session_context
from mobile_network_analytics.schemas.utils import Interval


@app.task
def calculate_service_kpis_task(directory_path: str, interval: Interval, end_time: datetime = datetime.now()):

    start_ts, end_ts = get_time_window(interval, end_time)

    interval_files = get_interval_files(directory_path, start_ts, end_ts)

    traffic_records = parse_files(interval_files)

    service_data_records = calculate_services_kpis(traffic_records, start_ts, end_ts, interval)

    with get_db_session_context() as session:
        for record in service_data_records:
            session.add(record)
        session.commit()


@app.task
def calculate_cell_kpis_task(directory_path: str, interval: Interval, end_time: datetime = datetime.now()):

    start_ts, end_ts = get_time_window(interval, end_time)

    interval_files = get_interval_files(directory_path, start_ts, end_ts)

    traffic_records = parse_files(interval_files)

    cell_data_records = calculate_cells_kpis(traffic_records, start_ts, end_ts, interval)

    with get_db_session_context() as session:
        for record in cell_data_records:
            session.add(record)
        session.commit()
