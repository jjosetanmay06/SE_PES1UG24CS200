import pytest

from pet_walking_service import process_walking_routes, inspect_gps_collars


def make_route(**overrides):
    data = {
        "route_confirmed": True,
        "session_type": "standard_30",
        "is_weekend": False,
        "walks": [{"num_pets": 1, "aggression_alert": False, "needs_meds": False}],
    }
    data.update(overrides)
    return data


@pytest.mark.parametrize("invalid_routes,fee", [
    ("invalid", 5.0),
    ([], -0.01),
])
def test_input_validation_branches(invalid_routes, fee):
    with pytest.raises(ValueError):
        process_walking_routes(invalid_routes, fee)


def test_unconfirmed_route_branch():
    assert process_walking_routes([make_route(route_confirmed=False)], 5.0)["status"] == "ZERO_EARNINGS"


@pytest.mark.parametrize("session,expected", [
    ("standard_60", 35.0 + 5.0),
    ("standard_30", 22.0 + 5.0),
    ("express_15", 14.0 + 5.0),
])
def test_each_supported_session_branch(session, expected):
    result = process_walking_routes(
        [make_route(session_type=session, walks=[{"num_pets": 1}])], 5.0
    )
    assert result["total_revenue"] == expected


def test_unknown_session_branch():
    assert process_walking_routes([make_route(session_type="unknown")], 5.0)["status"] == "ZERO_EARNINGS"


def test_zero_and_negative_pet_count_branch():
    result = process_walking_routes(
        [make_route(walks=[{"num_pets": 0}, {"num_pets": -2}])], 5.0
    )
    assert result["status"] == "ZERO_EARNINGS"


def test_aggression_standard_60_break_branch():
    walks = [
        {"num_pets": 1, "aggression_alert": False},
        {"num_pets": 1, "aggression_alert": True},
        {"num_pets": 2, "aggression_alert": False},
    ]
    result = process_walking_routes([make_route(session_type="standard_60", walks=walks)], 5.0)
    assert result["total_revenue"] == 0.0


def test_aggression_other_session_continues_and_meds_branch():
    walks = [
        {"num_pets": 1, "aggression_alert": True, "needs_meds": True},
        {"num_pets": 1, "aggression_alert": False, "needs_meds": False},
    ]
    result = process_walking_routes([make_route(walks=walks)], 5.0)
    assert result["total_revenue"] == 33.0


def test_more_than_three_pets_discount_branch():
    result = process_walking_routes(
        [make_route(walks=[{"num_pets": 4, "aggression_alert": False}])], 5.0
    )
    assert result["total_revenue"] == 48.6


def test_three_or_fewer_pets_regular_fee_branch():
    result = process_walking_routes(
        [make_route(walks=[{"num_pets": 3, "aggression_alert": False}])], 5.0
    )
    assert result["total_revenue"] == 37.0


def test_medication_false_and_true_branches():
    walks = [
        {"num_pets": 1, "needs_meds": False},
        {"num_pets": 1, "needs_meds": True},
    ]
    result = process_walking_routes([make_route(walks=walks)], 5.0)
    assert result["total_revenue"] == 60.0


def test_weekend_false_and_true_branches():
    routes = [
        make_route(is_weekend=False),
        make_route(is_weekend=True),
    ]
    result = process_walking_routes(routes, 5.0)
    assert result["total_revenue"] == 59.0


def test_incident_audit_threshold_branch():
    result = process_walking_routes(
        [make_route(walks=[{"num_pets": 0} for _ in range(5)])], 5.0
    )
    assert result["status"] == "INCIDENT_AUDIT"


def test_zero_earnings_status_branch():
    result = process_walking_routes([], 5.0)
    assert result == {"total_revenue": 0.0, "status": "ZERO_EARNINGS"}


def test_completed_status_branch():
    result = process_walking_routes([make_route()], 5.0)
    assert result["status"] == "COMPLETED"


def test_empty_gps_matrix_branch():
    assert inspect_gps_collars([]) == "NO_DATA"


def test_gps_inner_loop_zero_iteration_and_online_branch():
    assert inspect_gps_collars([[], [30, 25]]) == "ONLINE"


def test_weak_signal_streak_resets_when_signal_recovers():
    assert inspect_gps_collars([[10, 30, 10]]) == "ONLINE"


def test_first_weak_signal_does_not_alert():
    assert inspect_gps_collars([[10]]) == "ONLINE"


def test_two_consecutive_weak_signals_alert():
    assert inspect_gps_collars([[10, 19]]) == "LOST_SIGNAL_ALERT"


def test_gps_outer_loop_checks_multiple_collars():
    assert inspect_gps_collars([[30, 30], [10, 10]]) == "LOST_SIGNAL_ALERT"
