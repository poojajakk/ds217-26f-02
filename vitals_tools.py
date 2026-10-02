"""Reusable helpers for summarizing clinic systolic readings."""


def systolic_readings(encounters):
    """This gives us the systolic reading in the encounter record."""
    readings = []
    for encounter in encounters:
        readings.append(encounter["systolic"])
    return readings



def mean_systolic(readings):
    """This give us the mean of the readings, or "None" when the list is empty."""
    if not readings:
        return None
    return sum(readings) / len(readings)


def count_patients(encounters):
    """This gives us the number of patient IDs that show in the encounters."""
    patient_ids = set()
    for encounter in encounters:
        patient_ids.add(encounter["patient_id"])
    return len(patient_ids)


def patients_at_or_above(encounters, cutoff):
    """ This gives us the IDs of the patients with any reading greater than or equal to the cutoff."""
    flagged = set()
    for encounter in encounters:
        if encounter["systolic"] >= cutoff:
            flagged.add(encounter["patient_id"])
    return sorted(flagged)
