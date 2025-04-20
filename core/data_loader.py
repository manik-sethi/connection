import csv
from typing import List, Tuple

csv_path = "data/attendees.csv"

def read_attendees() -> List[Tuple[str,str,str]]:
    out = []
    with open(csv_path, newline="", encoding="utf-8") as f:
        reader = csv.reader(f)
        next(reader)  # skip header
        for row in reader:
            # skip blank lines
            if not row or all(cell.strip()=="" for cell in row):
                continue
            # first column = name, last = hobby, middle = paragraph (re‑join)
            name      = row[0].strip()
            hobby     = row[-1].strip()
            paragraph = ",".join(cell.strip() for cell in row[1:-1])
            out.append((name, paragraph, hobby))
    return out

def append_attendee(name: str, paragraph: str, hobby: str):
    # when you write, wrap fields that contain commas in quotes
    with open(csv_path, "a", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow([name, paragraph, hobby])
