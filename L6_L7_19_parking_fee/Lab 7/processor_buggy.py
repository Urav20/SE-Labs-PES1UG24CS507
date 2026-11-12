"""Original Lab 6 parking-fee logic, retained for the Lab 7 baseline run."""

HOURLY_RATE = {"bike": 10, "car": 30, "truck": 60}


def parking_fee(vehicle, minutes, is_ev, lost_ticket):
    if vehicle not in HOURLY_RATE:
        raise ValueError("unknown vehicle")
    if minutes < 0:
        raise ValueError("invalid duration")
    if minutes <= 30:
        fee = 0
    else:
        hours = minutes // 60
        if minutes % 60 != 0:
            hours += 1
        fee = hours * HOURLY_RATE[vehicle]
    if is_ev and vehicle != "truck":
        fee = fee // 2
    if lost_ticket:
        fee += 200
    return fee


def find_slot(vehicle, free_slots, is_disabled):
    if free_slots <= 0:
        return "full"
    if is_disabled:
        return "ground floor"
    if vehicle == "truck":
        return "basement"
    return "any floor"


def monthly_pass(vehicle, is_resident):
    if vehicle == "bike":
        price = 500
    elif vehicle == "car":
        price = 1500
    else:
        raise ValueError("no pass for this vehicle")
    if is_resident:
        price -= price // 5
    return price


if __name__ == "__main__":
    print("Original Parking Fee Calculator (before fuzz-test fixes)")
    print("Car, 90 minutes:", parking_fee("car", 90, False, False))
    print("Car slot:", find_slot("car", 5, False))
    print("Resident car pass:", monthly_pass("car", True))
