# Lab 1 – Grade Evaluator & Archiver
**African Leadership University | Intro to Python & Databases | BSE Year 1**

## What This Project Does
- Reads student grades from `grades.csv`
- Validates scores (0–100) and weights (Formative=60, Summative=40)
- Calculates GPA on a 5.0 scale
- Determines Pass/Fail (must score ≥50% in BOTH categories)
- Identifies assignments eligible for resubmission
- Archives old grade files with timestamps via a shell script

---

## How to Run the Python Script

### Requirements
- Python 3 installed
- A `grades.csv` file in the same folder with columns: `assignment, group, score, weight`

### Run it
```bash
python3 grade-evaluator.py
```

### Expected Output
The script prints a full grade report including:
- Per-assignment scores
- Formative and Summative weighted percentages
- Overall grade and GPA
- PASSED or FAILED status
- Assignments eligible for resubmission (if any)

---

## How to Run the Shell Script

### Make it executable (first time only)
```bash
chmod +x organizer.sh
```

### Run it
```bash
./organizer.sh
```

### What it does
1. Checks that `grades.csv` exists
2. Creates an `archive/` folder if it doesn't exist
3. Renames and moves `grades.csv` to `archive/grades_YYYYMMDD-HHMMSS.csv`
4. Creates a fresh empty `grades.csv`
5. Appends a log entry to `organizer.log`

---

## Project Files

| File | Description |
|------|-------------|
| `grade-evaluator.py` | Main Python application |
| `organizer.sh` | Bash archiving script |
| `grades.csv` | Sample grade data |
| `README.md` | This file |
```

---

## Step 6 — Commit and Push to GitHub

In VS Code, open the **Source Control** panel (the branch icon on the left sidebar, or `Ctrl + Shift + G`):

1. You'll see all your new files listed under **Changes**
2. Click the **+** next to each file to stage them (or click **+** next to "Changes" to stage all)
3. Type a commit message in the box at the top, like:
```
   Add grade-evaluator.py, organizer.sh, grades.csv and README
