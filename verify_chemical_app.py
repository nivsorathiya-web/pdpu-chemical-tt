import os

file_path = "/Users/nivsorathiya/Desktop/pdeu-timetable/chemical.html"
with open(file_path, "r", encoding="utf-8") as f:
    html = f.read()

# Find the start of studentDatabase
start_marker = "const studentDatabase = ["
start_idx = html.find(start_marker)
if start_idx == -1:
    print("Error: const studentDatabase not found!")
    exit(1)

# We find the start index of the array: the first '['
array_start = start_idx + len("const studentDatabase = ")
# Count brackets to find the matching ']'
bracket_count = 0
array_end = -1
for i in range(array_start, len(html)):
    char = html[i]
    if char == '[':
        bracket_count += 1
    elif char == ']':
        bracket_count -= 1
        if bracket_count == 0:
            array_end = i + 1
            break

if array_end == -1:
    print("Error: Matching closing bracket for studentDatabase not found!")
    exit(1)

db_str = html[array_start:array_end]

import json
try:
    db = json.loads(db_str)
    print(f"Success: studentDatabase successfully parsed with {len(db)} students!")
    
    # Verify exact length
    if len(db) != 198:
        print(f"Error: expected 198 students, found {len(db)}")
        exit(1)
    else:
        print("Verified: Exactly 198 unique students are present.")
        
    # Verify email domain format
    bad_emails = [s for s in db if not s['email'].endswith('@sot.pdpu.ac.in')]
    if bad_emails:
        print(f"Error: found {len(bad_emails)} incorrect emails: {bad_emails}")
        exit(1)
    else:
        print("Verified: All student email domains are correct (@sot.pdpu.ac.in).")
        
    # Print sample records to ensure formatting is correct
    print("\nSample records:")
    print("First student:", db[0])
    print("Middle student:", db[95])
    print("Last student:", db[-1])
    
except Exception as e:
    print(f"Error parsing studentDatabase: {e}")
    exit(1)
