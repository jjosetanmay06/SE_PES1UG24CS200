import pytest

from pet_walking_service import process_walking_routes, inspect_gps_collars


def route(**overrides):
    data = {
        "route_confirmed": True,
        "session_type": "standard_30",
        "is_weekend": False,
        "walks": [{"num_pets": 1, "aggression_alert": False, "needs_meds": False}],
    }
    data.update(overrides)
    return data


def test_invalid_routes_type():
    with pytest.raises(ValueError):
        process_walking_routes("not-a-list", 5.0)


def test_negative_transport_fee():
    with pytest.raises(ValueError):
        process_walking_routes([], -1.0)


def test_unconfirmed_route_is_skipped():
    result = process_walking_routes([route(route_confirmed=False)], 5.0)
    assert result == {"total_revenue": 0.0, "status": "ZERO_EARNINGS"}


def test_standard_30_route():
    result = process_walking_routes([route()], 5.0)
    assert result == {"total_revenue": 27.0, "status": "COMPLETED"}


def test_standard_60_route():
    result = process_walking_routes([route(session_type="standard_60")], 5.0)
    assert result["total_revenue"] == 40.0


def test_express_15_route():
    result = process_walking_routes([route(session_type="express_15")], 5.0)
    assert result["total_revenue"] == 19.0


def test_unknown_session_type_records_incident():
    result = process_walking_routes([route(session_type="overnight")], 5.0)
    assert result == {"total_revenue": 0.0, "status": "ZERO_EARNINGS"}


def test_invalid_pet_count_records_incident():
    result = process_walking_routes([route(walks=[{"num_pets": 0}])], 5.0)
    assert result["status"] == "ZERO_EARNINGS"


def test_aggression_on_standard_60_cancels_route():
    walks = [
        {"num_pets": 1, "aggression_alert": False, "needs_meds": False},
        {"num_pets": 1, "aggression_alert": True, "needs_meds": False},
        {"num_pets": 1, "aggression_alert": False, "needs_meds": False},
    ]
    result = process_walking_routes([route(session_type="standard_60", walks=walks)], 5.0)
    assert result == {"total_revenue": 0.0, "status": "ZERO_EARNINGS"}


def test_large_group_discount():
    result = process_walking_routes(
        [route(walks=[{"num_pets": 4, "aggression_alert": False, "needs_meds": False}])],
        5.0,
    )
    assert result["total_revenue"] == 48.6


def test_medication_fee():
    result = process_walking_routes(
        [route(walks=[{"num_pets": 1, "aggression_alert": False, "needs_meds": True}])],
        5.0,
    )
    assert result["total_revenue"] == 33.0


def test_weekend_transport_fee():
    result = process_walking_routes([route(is_weekend=True)], 5.0)
    assert result["total_revenue"] == 32.0


def test_aggression_on_non_60_minute_session():
    result = process_walking_routes(
        [route(walks=[{"num_pets": 1, "aggression_alert": True, "needs_meds": True}])],
        5.0,
    )
    assert result["total_revenue"] == 6.0


def test_more_than_four_incidents_triggers_audit():
    bad_walks = [{"num_pets": 0} for _ in range(5)]
    result = process_walking_routes([route(walks=bad_walks)], 5.0)
    assert result["status"] == "INCIDENT_AUDIT"


def test_empty_gps_data():
    assert inspect_gps_collars([]) == "NO_DATA"


def test_gps_signal_stays_online():
    assert inspect_gps_collars([[25, 18, 30], [40]]) == "ONLINE"


def test_two_consecutive_weak_signals_trigger_alert():
    assert inspect_gps_collars([[25, 18, 19, 30]]) == "LOST_SIGNAL_ALERT"
