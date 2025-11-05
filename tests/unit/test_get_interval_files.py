import pytest
from mobile_network_analytics.data_ingestion.file_extraction_utils import get_interval_files, extract_timestamp_from_filename


def test_get_interval_files(tmp_path):
    # Create test files with different timestamps
    filenames = [
        "ipflow_data.ts-1488355500000.1.csv",
        "ipflow_data.ts-1488355600000.1.csv",
        "ipflow_data.ts-1488355700000.1.csv",
        "ipflow_data.ts-1488355800000.1.csv",
    ]

    for filename in filenames:
        (tmp_path / filename).touch()

    start_ts = 1488355550000  # Between first and second file
    end_ts = 1488355750000    # Between third and fourth file

    expected_files = {
        str(tmp_path / "ipflow_data.ts-1488355600000.1.csv"),
        str(tmp_path / "ipflow_data.ts-1488355700000.1.csv"),
    }

    result_files = set(get_interval_files(str(tmp_path), start_ts, end_ts))

    assert result_files == expected_files


def test_get_interval_files_no_matches(tmp_path):
    # Create test files with different timestamps
    filenames = [
        "ipflow_data.ts-1488355500000.1.csv",  # 1488355500000
        "ipflow_data.ts-1488355600000.1.csv",  # 1488355600000
    ]

    for filename in filenames:
        (tmp_path / filename).touch()

    start_ts = 1488355700000  # After all files
    end_ts = 1488355800000    # After all files

    result_files = get_interval_files(str(tmp_path), start_ts, end_ts)

    assert result_files == []
