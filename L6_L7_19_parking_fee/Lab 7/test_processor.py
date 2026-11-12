"""Property-based fuzz tests for the parking fee application."""

import pytest
from hypothesis import given, settings, strategies as st

from parking_fee import find_slot, monthly_pass, parking_fee


VALID_VEHICLES = st.sampled_from(["bike", "car", "truck"])
PASS_VEHICLES = st.sampled_from(["bike", "car"])


# parking_fee properties
@given(VALID_VEHICLES, st.integers(min_value=0, max_value=10**7),
       st.booleans(), st.booleans())
@settings(max_examples=200)
def test_parking_fee_never_returns_negative(vehicle, minutes, is_ev, lost_ticket):
    assert parking_fee(vehicle, minutes, is_ev, lost_ticket) >= 0


@given(VALID_VEHICLES, st.integers(min_value=0, max_value=10**6),
       st.booleans())
def test_short_stay_is_free_without_lost_ticket(vehicle, minutes, is_ev):
    if minutes <= 30:
        assert parking_fee(vehicle, minutes, is_ev, False) == 0


@given(VALID_VEHICLES, st.integers(min_value=31, max_value=10**6),
       st.booleans())
def test_lost_ticket_adds_exactly_200(vehicle, minutes, is_ev):
    assert parking_fee(vehicle, minutes, is_ev, True) == (
        parking_fee(vehicle, minutes, is_ev, False) + 200
    )


@given(VALID_VEHICLES, st.integers(min_value=31, max_value=10**6))
def test_partial_hour_rounding_is_monotonic(vehicle, minutes):
    assert parking_fee(vehicle, minutes + 1, False, False) >= (
        parking_fee(vehicle, minutes, False, False)
    )


@given(st.one_of(st.none(), st.integers(), st.text(), st.lists(st.integers())))
def test_parking_fee_rejects_invalid_vehicle(vehicle):
    with pytest.raises(ValueError, match="unknown vehicle"):
        parking_fee(vehicle, 60, False, False)


@given(st.one_of(st.none(), st.text(), st.floats(allow_nan=False),
                 st.booleans(), st.integers(max_value=-1)))
def test_parking_fee_rejects_invalid_duration(minutes):
    with pytest.raises(ValueError, match="invalid duration"):
        parking_fee("car", minutes, False, False)


@pytest.mark.parametrize("flag_position", ["is_ev", "lost_ticket"])
@given(st.one_of(st.none(), st.integers(), st.text(), st.lists(st.integers())))
def test_parking_fee_rejects_non_boolean_flags(flag_position, invalid):
    flags = {"is_ev": False, "lost_ticket": False}
    flags[flag_position] = invalid
    with pytest.raises(ValueError, match="invalid flag"):
        parking_fee("car", 60, **flags)


# find_slot properties
@given(VALID_VEHICLES, st.integers(min_value=1, max_value=10**6),
       st.booleans())
def test_find_slot_returns_valid_location(vehicle, free_slots, is_disabled):
    result = find_slot(vehicle, free_slots, is_disabled)
    assert result in {"ground floor", "basement", "any floor"}


@given(VALID_VEHICLES, st.booleans())
def test_no_slots_always_returns_full(vehicle, is_disabled):
    assert find_slot(vehicle, 0, is_disabled) == "full"


@given(st.one_of(st.none(), st.text(), st.floats(allow_nan=False),
                 st.booleans(), st.integers(max_value=-1)))
def test_find_slot_rejects_invalid_slot_count(free_slots):
    with pytest.raises(ValueError, match="invalid free slots"):
        find_slot("car", free_slots, False)


@given(st.one_of(st.none(), st.integers(), st.text(), st.lists(st.integers())))
def test_find_slot_rejects_invalid_vehicle(vehicle):
    with pytest.raises(ValueError, match="unknown vehicle"):
        find_slot(vehicle, 1, False)


@given(st.one_of(st.none(), st.integers(), st.text()))
def test_find_slot_rejects_non_boolean_disabled_flag(flag):
    with pytest.raises(ValueError, match="invalid flag"):
        find_slot("car", 1, flag)


# monthly_pass properties
@given(PASS_VEHICLES, st.booleans())
def test_monthly_pass_is_non_negative(vehicle, is_resident):
    assert monthly_pass(vehicle, is_resident) >= 0


@given(PASS_VEHICLES)
def test_resident_gets_twenty_percent_discount(vehicle):
    regular = monthly_pass(vehicle, False)
    resident = monthly_pass(vehicle, True)
    assert resident == regular - regular // 5


@given(st.one_of(st.none(), st.integers(), st.text(), st.lists(st.integers())))
def test_monthly_pass_rejects_unsupported_vehicle(vehicle):
    with pytest.raises(ValueError, match="no pass for this vehicle"):
        monthly_pass(vehicle, False)


@given(st.one_of(st.none(), st.integers(), st.text()))
def test_monthly_pass_rejects_non_boolean_resident_flag(flag):
    with pytest.raises(ValueError, match="invalid flag"):
        monthly_pass("car", flag)
