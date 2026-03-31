"""
grade-evaluator.py
ALU Lab 1 – Grade Evaluator
Reads grades.csv, validates data, computes GPA, and determines Pass/Fail.
"""

import csv
import os
import sys


# ──────────────────────────────────────────────
# STEP 1 – Load the CSV file with error handling
# ──────────────────────────────────────────────
def load_grades(filepath="grades.csv"):
    if not os.path.exists(filepath):
        print(f"ERROR: '{filepath}' not found. Make sure the file is in the same folder.")
        sys.exit(1)

    rows = []
    try:
        with open(filepath, newline="", encoding="utf-8") as f:
            reader = csv.DictReader(f)

            if reader.fieldnames is None:
                print("ERROR: grades.csv is empty. No data to evaluate.")
                sys.exit(1)

            required_columns = {"assignment", "group", "score", "weight"}
            if not required_columns.issubset(set(reader.fieldnames)):
                print(f"ERROR: CSV is missing required columns. Expected: {required_columns}")
                print(f"       Found: {set(reader.fieldnames)}")
                sys.exit(1)

            for line_num, row in enumerate(reader, start=2):
                assignment = row["assignment"].strip()
                group      = row["group"].strip()

                try:
                    score = float(row["score"])
                except ValueError:
                    print(f"ERROR (row {line_num}): Score for '{assignment}' is not a number "
                          f"(got '{row['score']}').")
                    sys.exit(1)

                try:
                    weight = float(row["weight"])
                except ValueError:
                    print(f"ERROR (row {line_num}): Weight for '{assignment}' is not a number "
                          f"(got '{row['weight']}').")
                    sys.exit(1)

                rows.append({
                    "assignment": assignment,
                    "group":      group,
                    "score":      score,
                    "weight":     weight,
                })

    except Exception as e:
        print(f"ERROR: Could not read '{filepath}': {e}")
        sys.exit(1)

    if len(rows) == 0:
        print("ERROR: grades.csv has headers but no assignment rows. Nothing to evaluate.")
        sys.exit(1)

    return rows


# ──────────────────────────────────────────────
# STEP 2 – Validate grades (0–100 range)
# ──────────────────────────────────────────────
def validate_grades(rows):
    errors = []
    for row in rows:
        if not (0 <= row["score"] <= 100):
            errors.append(
                f"  • '{row['assignment']}' has score {row['score']} (must be 0–100)"
            )
    if errors:
        print("VALIDATION ERROR – The following scores are out of range:")
        print("\n".join(errors))
        sys.exit(1)


# ──────────────────────────────────────────────
# STEP 3 – Validate weights
# ──────────────────────────────────────────────
def validate_weights(rows):
    total_weight     = sum(r["weight"] for r in rows)
    formative_weight = sum(r["weight"] for r in rows if r["group"].lower() == "formative")
    summative_weight = sum(r["weight"] for r in rows if r["group"].lower() == "summative")

    errors = []
    if total_weight != 100:
        errors.append(f"  • Total weight is {total_weight} (must be 100).")
    if formative_weight != 60:
        errors.append(f"  • Formative weight is {formative_weight} (must be 60).")
    if summative_weight != 40:
        errors.append(f"  • Summative weight is {summative_weight} (must be 40).")

    if errors:
        print("VALIDATION ERROR – Weight rules violated:")
        print("\n".join(errors))
        sys.exit(1)


# ──────────────────────────────────────────────
# STEP 4 – Calculate GPA & category percentages
# ──────────────────────────────────────────────
def calculate_results(rows):
    total_grade = sum(r["score"] * r["weight"] for r in rows) / 100

    formative_rows   = [r for r in rows if r["group"].lower() == "formative"]
    formative_weight = sum(r["weight"] for r in formative_rows)
    formative_pct    = (
        sum(r["score"] * r["weight"] for r in formative_rows) / formative_weight
        if formative_weight else 0
    )

    summative_rows   = [r for r in rows if r["group"].lower() == "summative"]
    summative_weight = sum(r["weight"] for r in summative_rows)
    summative_pct    = (
        sum(r["score"] * r["weight"] for r in summative_rows) / summative_weight
        if summative_weight else 0
    )

    gpa = (total_grade / 100) * 5.0

    return {
        "total_grade":   round(total_grade, 2),
        "gpa":           round(gpa, 2),
        "formative_pct": round(formative_pct, 2),
        "summative_pct": round(summative_pct, 2),
    }


# ──────────────────────────────────────────────
# STEP 5 – Pass / Fail decision
# ──────────────────────────────────────────────
def determine_status(results):
    passed = results["formative_pct"] >= 50 and results["summative_pct"] >= 50
    return "PASSED" if passed else "FAILED"


# ──────────────────────────────────────────────
# STEP 6 – Resubmission logic
# ──────────────────────────────────────────────
def find_resubmissions(rows):
    failed_formative = [
        r for r in rows
        if r["group"].lower() == "formative" and r["score"] < 50
    ]

    if not failed_formative:
        return []

    max_weight = max(r["weight"] for r in failed_formative)
    eligible   = [r["assignment"] for r in failed_formative if r["weight"] == max_weight]
    return eligible


# ──────────────────────────────────────────────
# STEP 7 – Print the report
# ──────────────────────────────────────────────
def print_report(rows, results, status, resubmissions):
    print("=" * 55)
    print("        STUDENT GRADE REPORT")
    print("=" * 55)

    print(f"\n{'Assignment':<40} {'Group':<12} {'Score':>6} {'Weight':>7}")
    print("-" * 67)
    for r in rows:
        print(f"{r['assignment']:<40} {r['group']:<12} {r['score']:>6.1f} {r['weight']:>7.1f}")

    print("-" * 67)
    print(f"\n{'Formative weighted score:':<35} {results['formative_pct']:>6.2f}%")
    print(f"{'Summative weighted score:':<35} {results['summative_pct']:>6.2f}%")
    print(f"{'Overall weighted grade:':<35} {results['total_grade']:>6.2f}%")
    print(f"{'GPA (out of 5.0):':<35} {results['gpa']:>6.2f}")

    print("\n" + "=" * 55)
    print(f"  FINAL STATUS: {status}")
    print("=" * 55)

    if resubmissions:
        print("\n Eligible for Resubmission (highest-weight failed Formative):")
        for name in resubmissions:
            print(f"   → {name}")
    else:
        print("\n No resubmissions required.")
    print()


# ──────────────────────────────────────────────
# MAIN
# ──────────────────────────────────────────────
def main():
    print("\nLoading grades...\n")
    rows = load_grades("grades.csv")
    validate_grades(rows)
    validate_weights(rows)
    results       = calculate_results(rows)
    status        = determine_status(results)
    resubmissions = find_resubmissions(rows)
    print_report(rows, results, status, resubmissions)


if __name__ == "__main__":
    main()
