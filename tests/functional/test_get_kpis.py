import mobile_network_analytics.models as models
from mobile_network_analytics.schemas.utils import Interval


def test_get_services_kpis(client, db_session):
    db_session.add(
        models.DBServiceData(
            interval_start_timestamp="1488355200000",
            interval_end_timestamp="1488355500000",
            service_id=1,
            total_bytes=1000,
            interval=Interval.FIVE_MINUTE
        )
    )
    db_session.commit()

    response = client.get("/kpi/services")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1
    assert data[0]["service_id"] == 1
    assert data[0]["total_bytes"] == 1000


def test_get_cells_kpis(client, db_session):
    db_session.add(
        models.DBCellData(
            interval_start_timestamp="1488355200000",
            interval_end_timestamp="1488355500000",
            cell_id=101,
            number_of_unique_users=50,
            interval=Interval.FIVE_MINUTE
        )
    )
    db_session.commit()

    response = client.get("/kpi/cells")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1
    assert data[0]["cell_id"] == 101
    assert data[0]["number_of_unique_users"] == 50
