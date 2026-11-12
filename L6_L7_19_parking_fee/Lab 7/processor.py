"""Parking fee, slot allocation, and monthly pass calculations."""

HOURLY_RATE = {"bike": 10, "car": 30, "truck": 60}
SUPPORTED_VEHICLES = frozenset(HOURLY_RATE)
PASS_PRICES = {"bike": 500, "car": 1500}


def _require_vehicle(vehicle):
    if not isinstance(vehicle, str) or vehicle not in SUPPORTED_VEHICLES:
        raise ValueError("unknown vehicle")


def _require_non_negative_integer(value, name):
    # bool is a subclass of int in Python, so reject it explicitly.
    if isinstance(value, bool) or not isinstance(value, int) or value < 0:
        raise ValueError(f"invalid {name}")


def parking_fee(vehicle, minutes, is_ev, lost_ticket):
    """Calculate a fee, rounding every started hour up to a full hour."""
    _require_vehicle(vehicle)
    _require_non_negative_integer(minutes, "duration")
    if not isinstance(is_ev, bool) or not isinstance(lost_ticket, bool):
        raise ValueError("invalid flag")

    if minutes <= 30:
        fee = 0
    else:
        hours = (minutes + 59) // 60
        fee = hours * HOURLY_RATE[vehicle]

    if is_ev and vehicle != "truck":
        fee //= 2
    if lost_ticket:
        fee += 200
    return fee


def find_slot(vehicle, free_slots, is_disabled):
    """Choose a parking area based on availability and vehicle needs."""
    _require_vehicle(vehicle)
    _require_non_negative_integer(free_slots, "free slots")
    if not isinstance(is_disabled, bool):
        raise ValueError("invalid flag")

    if free_slots == 0:
        return "full"
    if is_disabled:
        return "ground floor"
    if vehicle == "truck":
        return "basement"
    return "any floor"


def monthly_pass(vehicle, is_resident):
    """Return the monthly pass price, including the resident discount."""
    if not isinstance(vehicle, str) or vehicle not in PASS_PRICES:
        raise ValueError("no pass for this vehicle")
    if not isinstance(is_resident, bool):
        raise ValueError("invalid flag")

    price = PASS_PRICES[vehicle]
    if is_resident:
        price -= price // 5
    return price


if __name__ == "__main__":
    print("Parking Fee Calculator")
    print("Car, 90 minutes:", parking_fee("car", 90, False, False))
    print("EV bike, 120 minutes:", parking_fee("bike", 120, True, False))
    print("Truck, 45 minutes with lost ticket:",
          parking_fee("truck", 45, False, True))
    print("Car slot:", find_slot("car", 5, False))
    print("Truck slot:", find_slot("truck", 3, False))
    print("Resident car pass:", monthly_pass("car", True))
