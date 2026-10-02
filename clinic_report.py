#!/usr/bin/env python3
"""Summarize one week of clinic encounters and save the two report files."""

from pathlib import Path

from vitals_tools import (
    count_patients,
    mean_systolic,
    patients_at_or_above,
    systolic_readings,
)


DATA_PATH = Path("data") / "clinic_encounters.csv"
OUTPUT_DIR = Path("output")


def read_encounters(data_path):
    """One usable encouter like a dictionary that contains the variables for patient id, the visit data, etc.
    """
    with open(data_path, encoding="utf-8") as data_file:
        rows = data_file.read().splitlines()

    encounters = []
    skipped = 0
    for row in rows[1:]:
        if not row.strip():
            print("Skipping a blank row.")
            skipped += 1
            continue
        fields = row.strip().split(",")
        if len(fields) != 3:
            print(f"Skipping a row with {len(fields)} fields: {row.strip()}")
            skipped += 1
            continue
        patient_id, visit_date, raw_systolic = fields
        try:
            systolic = int(raw_systolic)
        except ValueError as error:
            print(f"Skipping {patient_id}: {error}")
            skipped += 1
            continue
        if not 60 <= systolic <= 250:
            print(f"Skipping {patient_id}: {systolic} mmHg is outside 60-250")
            skipped += 1
            continue
        encounters.append({"patient_id": patient_id, "visit_date": visit_date, "systolic": systolic})

    return encounters, skipped


def main():
    """The two artifacts this writes are the vitals_report and the followup_list text files."""
    encounters, skipped = read_encounters(DATA_PATH)
    readings = systolic_readings(encounters)
    OUTPUT_DIR.mkdir(exist_ok=True)

    report_lines = [
        f"Usable encounters: {len(encounters)}",
        f"Skipped rows: {skipped}",
        f"Patients seen: {count_patients(encounters)}",
        f"Mean systolic: {mean_systolic(readings):.1f} mmHg",
        f"Highest systolic: {max(readings)} mmHg",
        f"Lowest systolic: {min(readings)} mmHg",
    ]
    report_path = OUTPUT_DIR / "vitals_report.txt"
    with open(report_path, "w", encoding="utf-8") as report_file:
        report_file.write("\n".join(report_lines) + "\n")
    with open(report_path, encoding="utf-8") as report_file:
        print(f"Read back from {report_path}:")
        print(report_file.read())

    cutoff = 150
    reason = "I chose the cutoff of 150 because I know that the typical blood pressure level is 120 and when it is 150 it is usually the lowest value when there is concern."
    followup_lines = [f"Cutoff: {cutoff} mmHg", f"Reason: {reason}"]
    followup_lines += patients_at_or_above(encounters, cutoff)
    with open(OUTPUT_DIR / "followup_list.txt", "w", encoding="utf-8") as followup_file:
        followup_file.write("\n".join(followup_lines) + "\n")


if __name__ == "__main__":
    main()
