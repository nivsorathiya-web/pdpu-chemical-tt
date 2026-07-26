import os
import json
import re

scratch_dir = "/Users/nivsorathiya/.gemini/antigravity/brain/86195e86-71e1-4bcf-ad67-a126f4380a93/scratch"

# Subject details mapping
subject_details = {
    "CDC Training": {"code": "22CDC005", "type": "cdc"},
    "Mass Transfer Operations - I": {"code": "24CH301T", "type": "mto"},
    "Mass Transfer Operations - I Lab": {"code": "24CH301P", "type": "mto-lab", "isLab": True},
    "Chemical Reaction Engineering I": {"code": "24CH302T", "type": "cre"},
    "Chemical Reaction Engineering I Lab": {"code": "24CH302P", "type": "cre-lab", "isLab": True},
    "Process Equipment Design": {"code": "24CH303T", "type": "ped"},
    "Process Equipment Design Lab": {"code": "24CH303P", "type": "ped-lab", "isLab": True},
    "Engineering Economics": {"code": "24HS301T", "type": "eco"}
}

def clean_subject_name(text):
    text = text.replace("★", "").strip()
    if "CDC Training" in text or "22CDC005" in text:
        return "CDC Training"
    if "Mass Transfer" in text and "Lab" in text:
        return "Mass Transfer Operations - I Lab"
    if "Mass Transfer" in text:
        return "Mass Transfer Operations - I"
    if "Chemical Reaction" in text and "Lab" in text:
        return "Chemical Reaction Engineering I Lab"
    if "Chemical Reaction" in text:
        return "Chemical Reaction Engineering I"
    if "Process Equipment" in text and "Lab" in text:
        return "Process Equipment Design Lab"
    if "Process Equipment" in text:
        return "Process Equipment Design"
    if "Engineering Economics" in text or "24HS301T" in text:
        return "Engineering Economics"
    return None

# Define time slots per division
division_time_slots = {
    "div1": [
        {"slot": "09:00-09:55", "x": 179.5},
        {"slot": "10:00-10:55", "x": 225.6},
        {"slot": "10:55-11:10", "x": 271.8, "isBreak": True},
        {"slot": "11:10-12:05", "x": 318.0},
        {"slot": "12:10-13:05", "x": 364.2, "isLunch": True},
        {"slot": "13:10-14:05", "x": 410.1},
        {"slot": "14:10-15:05", "x": 463.3},
        {"slot": "15:10-16:05", "x": 516.6},
        {"slot": "16:05-16:15", "x": 562.5, "isBreak": True},
        {"slot": "16:15-17:10", "x": 608.4},
        {"slot": "17:15-18:10", "x": 661.4}
    ],
    "div2": [
        {"slot": "09:00-09:55", "x": 92.4},
        {"slot": "10:00-10:55", "x": 156.5},
        {"slot": "10:55-11:10", "x": 194.5, "isBreak": True},
        {"slot": "11:10-12:05", "x": 263.9},
        {"slot": "12:10-13:05", "x": 333.3, "isLunch": True},
        {"slot": "13:10-14:05", "x": 400.0},
        {"slot": "14:10-15:05", "x": 495.1},
        {"slot": "15:10-16:05", "x": 588.3},
        {"slot": "16:05-16:15", "x": 653.0, "isBreak": True},
        {"slot": "16:15-17:10", "x": 719.4},
        {"slot": "17:15-18:10", "x": 785.8}
    ],
    "div3": [
        {"slot": "09:00-09:55", "x": 60.0},
        {"slot": "10:00-10:55", "x": 122.4},
        {"slot": "10:55-11:10", "x": 185.8, "isBreak": True},
        {"slot": "11:10-12:05", "x": 249.2},
        {"slot": "12:10-13:05", "x": 315.6, "isLunch": True},
        {"slot": "13:10-14:05", "x": 382.0},
        {"slot": "14:10-15:05", "x": 469.5},
        {"slot": "15:10-16:05", "x": 556.7},
        {"slot": "16:05-16:15", "x": 619.9, "isBreak": True},
        {"slot": "16:15-17:10", "x": 681.1},
        {"slot": "17:15-18:10", "x": 766.2}
    ]
}

def get_slot_for_x(x, div_key):
    slots = division_time_slots.get(div_key, [])
    closest_slot = None
    min_dist = 9999.0
    for slot in slots:
        dist = abs(slot['x'] - x)
        if dist < min_dist:
            min_dist = dist
            closest_slot = slot
    if min_dist < 35:
        return closest_slot
    return None

# Parse layout files
schedules = {
    "div1": {g: {} for g in ["E1", "E2", "E3"]},
    "div2": {g: {} for g in ["E4", "E5", "E6"]},
    "div3": {g: {} for g in ["E7", "E8", "E9"]}
}

div_files = {
    "div1": "5_1_layout.txt",
    "div2": "5_2_layout.txt",
    "div3": "5_3_layout.txt"
}

for div_key, layout_file in div_files.items():
    layout_path = os.path.join(scratch_dir, layout_file)
    if not os.path.exists(layout_path):
        print(f"Error: {layout_path} not found!")
        continue
        
    with open(layout_path, "r", encoding="utf-8") as f:
        content = f.read()
        
    # Group content by day
    # We find rows and check which day they correspond to
    # Days coordinates in layouts:
    # We parse each line: "Y=xxx.x: [x1] text1 | [x2] text2 ..."
    lines = content.split("\n")
    day_labels = {}
    row_elements = []
    
    for line in lines:
        if not line.strip():
            continue
        match_y = re.match(r'^Y=(\d+\.\d+): (.*)$', line)
        if match_y:
            y = float(match_y.group(1))
            parts_str = match_y.group(2)
            # Parse parts: "[x] text"
            parts = parts_str.split(" | ")
            for p in parts:
                match_p = re.match(r'^\[(\d+\.\d+)\] (.*)$', p)
                if match_p:
                    x = float(match_p.group(1))
                    text = match_p.group(2).strip()
                    if text in ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"]:
                        day_labels[text] = y
                    row_elements.append({
                        'x': x,
                        'y': y,
                        'text': text
                    })
                    
    # Sort row elements by Y descending
    print(f"\n--- Processing {div_key} ({layout_file}) ---")
    print("Day Y-coordinates:", day_labels)
    
    # Process each element to associate it with a Day
    for idx, el in enumerate(row_elements):
        if el['y'] > 530 or el['y'] < 390 if div_key in ["div2", "div3"] else el['y'] < 170:
            # Skip title, headers, faculty tables
            continue
            
        # Find which day this element belongs to based on Y-boundaries
        closest_day = None
        if div_key == "div1":
            if el['y'] > 440:
                closest_day = "Monday"
            elif el['y'] > 360:
                closest_day = "Tuesday"
            elif el['y'] > 290:
                closest_day = "Wednesday"
            elif el['y'] > 230:
                closest_day = "Thursday"
            else:
                closest_day = "Friday"
        elif div_key == "div2":
            if el['y'] > 491:
                closest_day = "Monday"
            elif el['y'] > 460:
                closest_day = "Tuesday"
            elif el['y'] > 430:
                closest_day = "Wednesday"
            elif el['y'] > 420:
                closest_day = "Thursday"
            else:
                closest_day = "Friday"
        elif div_key == "div3":
            if el['y'] > 496:
                closest_day = "Monday"
            elif el['y'] > 469:
                closest_day = "Tuesday"
            elif el['y'] > 443:
                closest_day = "Wednesday"
            elif el['y'] > 425:
                closest_day = "Thursday"
            else:
                closest_day = "Friday"
                
        if not closest_day:
            continue
            
        # Find which slot this element is in
        slot_info = get_slot_for_x(el['x'], div_key)
        if not slot_info or slot_info.get('isBreak') or slot_info.get('isLunch'):
            continue
            
        slot_name = slot_info['slot']
        text = el['text']
        
        # Parse targets (e.g., "E4E5E6 (24CH331T) E004, AYD-L")
        # Match E1-E9, Q1-Q6 prefixes
        match_prefix = re.match(r'^(E\dE\dE\d|E\d|Q\d)\s*\((.*?)\)', text)
        if not match_prefix:
            continue
            
        prefix = match_prefix.group(1)
        code = match_prefix.group(2)
        room = "—"
        prof = "—"
        
        # Check if room and prof are in the same text element
        match_inline = re.search(r'\((.*?)\)\s*([^,·\s]+)\s*[,·]\s*([^\s]+)', text)
        if match_inline:
            room = match_inline.group(2).strip()
            prof = match_inline.group(3).strip()
        else:
            # Look at the next element in the same division row to see if it is the room/prof
            if idx + 1 < len(row_elements):
                next_el = row_elements[idx + 1]
                if abs(next_el['y'] - el['y']) < 2 and (next_el['x'] - el['x']) < 25:
                    if ',' in next_el['text']:
                        parts = next_el['text'].split(',', 1)
                        room = parts[0].strip()
                        prof = parts[1].strip()
                    elif '·' in next_el['text']:
                        parts = next_el['text'].split('·', 1)
                        room = parts[0].strip()
                        prof = parts[1].strip()
                    else:
                        # Maybe just a room or prof
                        room = next_el['text'].strip()
                
        # If code is found, resolve subject name
        subject_name = None
        if code:
            for name, details in subject_details.items():
                if details['code'] == code:
                    subject_name = name
                    break
        
        if not subject_name:
            # Maybe elective: "E4E5E6 (24CH331T) E004, AYD-L"
            if "24CH331T" in text or code == "24CH331T":
                subject_name = "ELECTIVE"
            elif "24CH332T" in text or code == "24CH332T":
                subject_name = "ELECTIVE"
            elif "24CH333T" in text or code == "24CH333T":
                subject_name = "ELECTIVE"
                
        if subject_name:
            # Determine which groups this prefix maps to
            target_groups = []
            if prefix.startswith("E"):
                if len(prefix) == 6: # e.g. E4E5E6
                    target_groups = [prefix[i:i+2] for i in range(0, 6, 2)]
                else: # e.g. E6
                    target_groups = [prefix]
            elif prefix.startswith("Q"):
                q_map = {
                    "Q1": ["E1", "E2"], "Q2": ["E3"],
                    "Q3": ["E4", "E5"], "Q4": ["E6"],
                    "Q5": ["E7", "E8"], "Q6": ["E9"]
                }
                target_groups = q_map.get(prefix, [])
                
            for g in target_groups:
                if g in schedules[div_key]:
                    if closest_day not in schedules[div_key][g]:
                        schedules[div_key][g][closest_day] = {}
                        
                    # If it is an elective, just set as "ELECTIVE"
                    if subject_name == "ELECTIVE":
                        schedules[div_key][g][closest_day][slot_name] = "ELECTIVE"
                        print(f"Mapped {g} | {closest_day} | {slot_name} -> ELECTIVE")
                    else:
                        details = subject_details[subject_name]
                        existing = schedules[div_key][g][closest_day].get(slot_name)
                        if existing and isinstance(existing, dict) and existing.get("title") == subject_name:
                            existing_prof = existing.get("prof", "")
                            if prof not in existing_prof:
                                combined_prof = f"{existing_prof} + {prof}"
                                existing["prof"] = combined_prof
                                print(f"Combined profs for {g} | {closest_day} | {slot_name} -> {combined_prof}")
                        else:
                            schedules[div_key][g][closest_day][slot_name] = {
                                "title": subject_name,
                                "code": details["code"],
                                "room": room,
                                "prof": prof,
                                "type": details["type"]
                            }
                            if details.get("isLab"):
                                schedules[div_key][g][closest_day][slot_name]["isLab"] = True
                                next_slots = {
                                    "09:00-09:55": "10:00-10:55",
                                    "14:10-15:05": "15:10-16:05",
                                    "16:15-17:10": "17:15-18:10"
                                }
                                if slot_name in next_slots:
                                    n_slot = next_slots[slot_name]
                                    schedules[div_key][g][closest_day][n_slot] = schedules[div_key][g][closest_day][slot_name]
                            print(f"Mapped {g} | {closest_day} | {slot_name} -> {subject_name} ({prof} @ {room})")

# Let's save the reconstructed schedules to a JSON file
out_path = os.path.join(scratch_dir, "schedules_reconstructed.json")
with open(out_path, "w", encoding="utf-8") as f:
    json.dump(schedules, f, indent=4)
print(f"\nSaved reconstructed schedules to {out_path}")
