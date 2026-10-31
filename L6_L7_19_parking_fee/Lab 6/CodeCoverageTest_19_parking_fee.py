import pytest
from parking_fee import parking_fee, find_slot, monthly_pass


# Parking fee tests
def test_unknown_vehicle():
    with pytest.raises(ValueError, match="unknown vehicle"):
        parking_fee("scooter", 60, False, False)


def test_negative_duration():
    with pytest.raises(ValueError, match="invalid duration"):
        parking_fee("car", -10, False, False)


def test_free_short_stay():
    assert parking_fee("car", 20, False, False) == 0


def test_exact_hour():
    assert parking_fee("car", 60, False, False) == 30


def test_partial_hour_rounds_up():
    assert parking_fee("bike", 61, False, False) == 20


def test_ev_discount():
    assert parking_fee("car", 120, True, False) == 30


def test_ev_truck_no_discount():
    assert parking_fee("truck", 60, True, False) == 60


def test_lost_ticket_fee():
    assert parking_fee("bike", 60, False, True) == 210


# Parking slot tests
def test_parking_full():
    assert find_slot("car", 0, False) == "full"


def test_disabled_parking():
    assert find_slot("car", 5, True) == "ground floor"


def test_truck_parking():
    assert find_slot("truck", 5, False) == "basement"


def test_any_floor():
    assert find_slot("car", 5, False) == "any floor"


# Monthly pass tests
def test_bike_pass():
    assert monthly_pass("bike", False) == 500


def test_car_pass():
    assert monthly_pass("car", False) == 1500


def test_resident_discount():
    assert monthly_pass("car", True) == 1200


def test_invalid_pass_vehicle():
    with pytest.raises(ValueError, match="no pass for this vehicle"):
        monthly_pass("truck", False)
