#!/bin/bash
# organizer.sh
# ALU Lab 1 – Archiver & Workspace Reset Script
#
# What this script does, in order:
#   1. Verifies grades.csv exists before trying to archive it
#   2. Creates the 'archive/' directory if it does not already exist
#   3. Generates a timestamp string (YYYYMMDD-HHMMSS)
#   4. Renames + moves grades.csv → archive/grades_<timestamp>.csv
#   5. Creates a fresh, empty grades.csv so the environment is ready
#   6. Appends a log entry to organizer.log

# ── STEP 1: Make sure there is a grades.csv to archive ──────────────────────
GRADES_FILE="grades.csv"

if [ ! -f "$GRADES_FILE" ]; then
    echo "ERROR: '$GRADES_FILE' does not exist. Nothing to archive."
    exit 1
fi

# ── STEP 2: Create the archive directory if it does not exist ───────────────
ARCHIVE_DIR="archive"

if [ ! -d "$ARCHIVE_DIR" ]; then
    mkdir "$ARCHIVE_DIR"
    echo "Created directory: $ARCHIVE_DIR/"
else
    echo "Archive directory already exists: $ARCHIVE_DIR/"
fi

# ── STEP 3: Generate a timestamp  (format: YYYYMMDD-HHMMSS) ─────────────────
TIMESTAMP=$(date +"%Y%m%d-%H%M%S")

# ── STEP 4: Build the new filename and move the file ────────────────────────
NEW_FILENAME="grades_${TIMESTAMP}.csv"
ARCHIVE_PATH="${ARCHIVE_DIR}/${NEW_FILENAME}"

mv "$GRADES_FILE" "$ARCHIVE_PATH"

if [ $? -ne 0 ]; then
    echo "ERROR: Failed to move '$GRADES_FILE' to '$ARCHIVE_PATH'."
    exit 1
fi

echo "Archived: $GRADES_FILE  →  $ARCHIVE_PATH"

# ── STEP 5: Create a fresh empty grades.csv ──────────────────────────────────
touch "$GRADES_FILE"
echo "Created fresh empty file: $GRADES_FILE"

# ── STEP 6: Append log entry to organizer.log ────────────────────────────────
LOG_FILE="organizer.log"

{
    echo "---"
    echo "Timestamp   : $TIMESTAMP"
    echo "Original    : $GRADES_FILE"
    echo "Archived as : $ARCHIVE_PATH"
} >> "$LOG_FILE"

echo "Log updated : $LOG_FILE"
echo ""
echo "Done. Workspace is ready for the next batch of grades."
