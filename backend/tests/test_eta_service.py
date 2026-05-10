from app.services.eta_service import ETAService


def test_eta_uses_default_speed_when_speed_missing():
    eta = ETAService().estimate_eta_minutes(distance_miles=10, speed_mph=None)
    assert eta is not None
    assert eta > 0


def test_eta_zero_distance_is_zero_minutes():
    eta = ETAService().estimate_eta_minutes(distance_miles=0, speed_mph=20)
    assert eta == 0
