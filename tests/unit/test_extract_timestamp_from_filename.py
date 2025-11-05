from mobile_network_analytics.data_ingestion.file_extraction_utils import extract_timestamp_from_filename


def test_extract_timestamp_from_filename():
    filename = "ipflow_data.ts-1488355500000.1.csv"
    assert extract_timestamp_from_filename(filename) == 1488355500000


def test_extract_timestamp_from_filename_invalid():
    filename = "invalid_filename.csv"
    assert extract_timestamp_from_filename(filename) is None
