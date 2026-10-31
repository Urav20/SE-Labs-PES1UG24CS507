import pytest
from parking_fee import parking_fee, find_slot, monthly_pass


# Parking fee branches
@pytest.mark.parametrize("vehicle", ["bike", "car", "truck"])
def test_all_vehicle_types(vehicle):
    assert parking_fee(vehicle, 60, False, False) >= 0


def test_unknown_vehicle_branch():
    with pytest.raises(ValueError):
        parking_fee("scooter", 60, False, False)


def test_negative_duration_branch():
    with pytest.raises(ValueError):
        parking_fee("car", -1, False, False)


def test_free_duration_branch():
    assert parking_fee("bike", 30, False, False) == 0


def test_paid_duration_branch():
    assert parking_fee("bike", 31, False, False) == 10


def test_exact_hour_branch():
    assert parking_fee("car", 60, False, False) == 30


def test_partial_hour_branch():
    assert parking_fee("car", 61, False, False) == 60


def test_ev_discount_branch():
    assert parking_fee("car", 60, True, False) == 15


def test_ev_truck_branch():
    assert parking_fee("truck", 60, True, False) == 60


def test_lost_ticket_branch():
    assert parking_fee("bike", 60, False, True) == 210


def test_no_lost_ticket_branch():
    assert parking_fee("bike", 60, False, False) == 10


# Parking slot branches
def test_no_free_slots_branch():
    assert find_slot("car", 0, False) == "full"


def test_disabled_slot_branch():
    assert find_slot("car", 1, True) == "ground floor"


def test_truck_slot_branch():
    assert find_slot("truck", 1, False) == "basement"


def test_regular_slot_branch():
    assert find_slot("car", 1, False) == "any floor"


# Monthly pass branches
def test_bike_monthly_pass_branch():
    assert monthly_pass("bike", False) == 500


def test_car_monthly_pass_branch():
    assert monthly_pass("car", False) == 1500


def test_invalid_monthly_pass_branch():
    with pytest.raises(ValueError):
        monthly_pass("truck", False)


def test_resident_discount_branch():
    assert monthly_pass("car", True) == 1200


def test_non_resident_branch():
    assert monthly_pass("car", False) == 1500
