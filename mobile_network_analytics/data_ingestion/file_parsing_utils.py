import csv
from collections import defaultdict
from pydantic import ValidationError

from mobile_network_analytics.models import ServiceData, CellData
from mobile_network_analytics.schemas.traffic_record import TrafficRecord
from mobile_network_analytics.schemas.utils import Interval


def parse_files(files: list[str]) -> list[TrafficRecord]:
    """
    Parses a CSV file and returns a list of validated TrafficRecord objects.
    """
    records: list[TrafficRecord] = []

    for file in files:
        with open(file, mode="r", newline="", encoding="utf-8") as csvfile:
            reader = csv.DictReader(csvfile)
            for row_number, row in enumerate(reader, start=1):
                try:
                    row["interval_start_timestamp"] = str(row["interval_start_timestamp"])
                    row["interval_end_timestamp"] = str(row["interval_end_timestamp"])
                    row["msisdn"] = int(row["msisdn"])
                    row["bytes_uplink"] = int(row["bytes_uplink"])
                    row["bytes_downlink"] = int(row["bytes_downlink"])
                    row["service_id"] = int(row["service_id"])
                    row["cell_id"] = int(row["cell_id"])

                    record = TrafficRecord(**row)
                    records.append(record)

                except (KeyError, ValueError, ValidationError) as e:
                    print(f"[WARNING] Invalid record in {file} at row {row_number}: {e}")

    return records


def calculate_services_kpis(records: list[TrafficRecord], start_ts: int, end_ts: int, interval: Interval) -> list[ServiceData]:
    """
    Aggregates total bytes per service_id and returns ServiceData records.
    """
    if not records:
        return []

    # Aggregate bytes by service_id
    traffic_by_service: dict[int, int] = defaultdict(int)
    for rec in records:
        total_bytes = rec.bytes_uplink + rec.bytes_downlink
        traffic_by_service[rec.service_id] += total_bytes

    top_services = sorted(
        traffic_by_service.items(),
        key=lambda kv: kv[1],
        reverse=True
    )[:3]

    # Convert to ServiceData ORM objects
    service_data_records: list[ServiceData] = []
    for service_id, total_bytes in top_services:
        entry = ServiceData(
            interval_start_timestamp=start_ts,
            interval_end_timestamp=end_ts,
            service_id=service_id,
            total_bytes=total_bytes,
            interval=interval,
        )
        service_data_records.append(entry)

    return service_data_records


def calculate_cells_kpis(records: list[TrafficRecord], start_ts: int, end_ts: int, interval: Interval) -> list[ServiceData]:
    """
    Aggregates number of unique users per cell_id and returns CellData records.
    """
    if not records:
        return []

    # Aggregate unique users by cell_id
    users_by_cell: dict[int, set[int]] = defaultdict(set)
    for rec in records:
        users_by_cell[rec.cell_id].add(rec.msisdn)

    unique_users_count_by_cell: dict[int, int] = {
        cell_id: len(users)
        for cell_id, users in users_by_cell.items()
    }

    top_cells = sorted(
        unique_users_count_by_cell.items(),
        key=lambda kv: kv[1],
        reverse=True
    )[:3]

    # Convert to CellData ORM objects
    cell_data_records: list[CellData] = []
    for cell_id, unique_user_count in top_cells:
        entry = CellData(
            interval_start_timestamp=start_ts,
            interval_end_timestamp=end_ts,
            cell_id=cell_id,
            number_of_unique_users=unique_user_count,
            interval=interval,
        )
        cell_data_records.append(entry)

    return cell_data_records
