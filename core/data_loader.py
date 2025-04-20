import csv
from typing import List, Tuple

csv_path = "./data/attendees.csv"

def read_attendees() -> List[Tuple[str,str, str]]:
    out = []
    with open(csv_path, newline="", encoding="utf-8") as f:
        reader = csv.reader(f)
        next(reader)
        for name, paragraph in reader:
            out.append((name, paragraph))
    return out

def append_attendee(name: str, paragraph: str, hobby: str):
    with open(csv_path, "a", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow([name, paragraph])
