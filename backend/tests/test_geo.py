from app.utils.geo import haversine_distance_miles


def test_haversine_distance_same_point_is_zero():
    distance = haversine_distance_miles(35.0, -80.0, 35.0, -80.0)
    assert distance == 0


def test_haversine_distance_positive_for_different_points():
    distance = haversine_distance_miles(35.0, -80.0, 35.1, -80.1)
    assert distance > 0
