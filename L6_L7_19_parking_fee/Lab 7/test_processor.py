"""Hypothesis fuzz tests for all three parking-fee application functions."""

import pytest
from hypothesis import given, settings, strategies as st

from processor import find_slot, monthly_pass, parking_fee


VALID_VEHICLES = st.sampled_from(["bike", "car", "truck"])
PASS_VEHICLES = st.sampled_from(["bike", "car"])

INVALID_VEHICLE = st.one_of(
    st.none(),
    st.booleans(),
    st.integers(),
    st.text().filter(lambda value: value not in {"bike", "car", "truck"}),
    st.lists(st.integers()),
    st.dictionaries(st.text(), st.integers()),
)
INVALID_PASS_VEHICLE = st.one_of(
    st.none(),
    st.booleans(),
    st.integers(),
    st.text().filter(lambda value: value not in {"bike", "car"}),
    st.lists(st.integers()),
)
INVALID_FLAG = st.one_of(
    st.none(), st.integers(), st.text(), st.lists(st.integers())
)


# Tests for parking_fee()
@given(VALID_VEHICLES, st.integers(min_value=0, max_value=10**7),
       st.booleans(), st.booleans())
@settings(max_examples=200)
def test_parking_fee_never_returns_negative(vehicle, minutes, is_ev, lost_ticket):
    assert parking_fee(vehicle, minutes, is_ev, lost_ticket) >= 0


@given(VALID_VEHICLES, st.integers(min_value=0, max_value=10**6),
       st.booleans())
def test_stays_of_thirty_minutes_or_less_are_free(vehicle, minutes, is_ev):
    if minutes <= 30:
        assert parking_fee(vehicle, minutes, is_ev, False) == 0


@given(VALID_VEHICLES, st.integers(min_value=0, max_value=10**6),
       st.booleans())
def test_lost_ticket_adds_exactly_two_hundred(vehicle, minutes, is_ev):
    with_ticket = parking_fee(vehicle, minutes, is_ev, True)
    without_ticket = parking_fee(vehicle, minutes, is_ev, False)
    assert with_ticket == without_ticket + 200


@given(VALID_VEHICLES, st.integers(min_value=31, max_value=10**6))
def test_parking_fee_does_not_decrease_when_duration_increases(vehicle, minutes):
    assert parking_fee(vehicle, minutes + 1, False, False) >= (
        parking_fee(vehicle, minutes, False, False)
    )


@given(INVALID_VEHICLE)
def test_parking_fee_rejects_invalid_vehicle(vehicle):
    with pytest.raises(ValueError, match="unknown vehicle"):
        parking_fee(vehicle, 60, False, False)


@given(st.one_of(
    st.none(), st.text(), st.floats(allow_nan=False),
    st.booleans(), st.integers(max_value=-1)
))
def test_parking_fee_rejects_invalid_duration(minutes):
    with pytest.raises(ValueError, match="invalid duration"):
        parking_fee("car", minutes, False, False)


@given(st.sampled_from(["is_ev", "lost_ticket"]), INVALID_FLAG)
def test_parking_fee_rejects_non_boolean_flags(flag_name, invalid_value):
    flags = {"is_ev": False, "lost_ticket": False}
    flags[flag_name] = invalid_value
    with pytest.raises(ValueError, match="invalid flag"):
        parking_fee("car", 60, **flags)


# Tests for find_slot()
@given(VALID_VEHICLES, st.integers(min_value=1, max_value=10**6),
       st.booleans())
def test_find_slot_returns_a_valid_location(vehicle, free_slots, is_disabled):
    assert find_slot(vehicle, free_slots, is_disabled) in {
        "ground floor", "basement", "any floor"
    }


@given(VALID_VEHICLES, st.booleans())
def test_find_slot_returns_full_when_no_slots_are_free(vehicle, is_disabled):
    assert find_slot(vehicle, 0, is_disabled) == "full"


@given(INVALID_VEHICLE)
def test_find_slot_rejects_invalid_vehicle(vehicle):
    with pytest.raises(ValueError, match="unknown vehicle"):
        find_slot(vehicle, 1, False)


@given(st.one_of(
    st.none(), st.text(), st.floats(allow_nan=False),
    st.booleans(), st.integers(max_value=-1)
))
def test_find_slot_rejects_invalid_free_slot_count(free_slots):
    with pytest.raises(ValueError, match="invalid free slots"):
        find_slot("car", free_slots, False)


@given(INVALID_FLAG)
def test_find_slot_rejects_non_boolean_disabled_flag(flag):
    with pytest.raises(ValueError, match="invalid flag"):
        find_slot("car", 1, flag)


# Tests for monthly_pass()
@given(PASS_VEHICLES, st.booleans())
def test_monthly_pass_never_returns_negative(vehicle, is_resident):
    assert monthly_pass(vehicle, is_resident) >= 0


@given(PASS_VEHICLES)
def test_residents_receive_twenty_percent_discount(vehicle):
    regular_price = monthly_pass(vehicle, False)
    resident_price = monthly_pass(vehicle, True)
    assert resident_price == regular_price - regular_price // 5


@given(INVALID_PASS_VEHICLE)
def test_monthly_pass_rejects_unsupported_vehicle(vehicle):
    with pytest.raises(ValueError, match="no pass for this vehicle"):
        monthly_pass(vehicle, False)


@given(INVALID_FLAG)
def test_monthly_pass_rejects_non_boolean_resident_flag(flag):
    with pytest.raises(ValueError, match="invalid flag"):
        monthly_pass("car", flag)
