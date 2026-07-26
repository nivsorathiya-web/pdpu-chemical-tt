import os
import re
import json
import base64

desktop_dir = "/Users/nivsorathiya/Desktop"
scratch_dir = "/Users/nivsorathiya/.gemini/antigravity/brain/86195e86-71e1-4bcf-ad67-a126f4380a93/scratch"

# Load Breaking Bad image as Base64 data URI
img_path = os.path.join(desktop_dir, "pdeu-timetable", "breaking_bad.jpg")
with open(img_path, "rb") as img_file:
    b64_image = base64.b64encode(img_file.read()).decode("utf-8")
breaking_bad_src = f"data:image/jpeg;base64,{b64_image}"


# 1. Load official merged student database
merged_path = os.path.join(scratch_dir, "chemical_students_merged.json")
with open(merged_path, "r", encoding="utf-8") as f:
    student_database = json.load(f)

# Format to JS string representation
student_db_js = json.dumps(student_database, indent=12)

# Load reconstructed timetables database
sched_path = os.path.join(scratch_dir, "schedules_reconstructed.json")
with open(sched_path, "r", encoding="utf-8") as f:
    schedules_data = json.load(f)
schedules_js = json.dumps(schedules_data, indent=8)

# Now let's assemble chemical.html. We will read the CSS structure and base JS template of CSBS custom timetable.html,
# and insert our new arrays, profiles, mappings, and download URLs.
template_path = "/Users/nivsorathiya/Desktop/pdeu-timetable/CSBS custom timetable.html"
with open(template_path, "r", encoding="utf-8") as f:
    orig = f.read()

# Let's customize key details in chemical.html:
# 1. Update Title and Headers to Chemical Engineering
orig = orig.replace("<title>Timetable</title>", "<title>Chemical Engineering Timetable</title>")
orig = orig.replace('const savedRoll = localStorage.getItem("csbs_user_roll");', 'const savedRoll = localStorage.getItem("chemical_user_roll");')
orig = orig.replace('localStorage.setItem("csbs_user_roll", roll);', 'const unused_var = 1;') # no-op replacement to avoid conflict
orig = orig.replace('localStorage.removeItem("csbs_user_roll");', 'localStorage.removeItem("chemical_user_roll");')
orig = orig.replace('localStorage.setItem("csbs_user_roll", student.roll);', 'localStorage.setItem("chemical_user_roll", student.roll);')

old_hidden_inputs = """            <!-- Hidden Control Inputs (Maintained for Internal Timetable Engine Compatibility) -->
            <div style="display:none;">
                <select id="div-select" onchange="onDivisionChange()"><option value="1">1</option><option value="2">2</option></select>
                <select id="group-select" onchange="updateAppUI()"></select>
                <select id="elective-select" onchange="updateAppUI()"><option value="bs">bs</option><option value="cs">cs</option><option value="cd">cd</option></select>
            </div>"""

new_hidden_inputs = """            <!-- Hidden Control Inputs (Maintained for Internal Timetable Engine Compatibility) -->
            <div style="display:none;">
                <select id="div-select" onchange="onDivisionChange()">
                    <option value="1">1</option>
                    <option value="2">2</option>
                    <option value="3">3</option>
                </select>
                <select id="group-select" onchange="updateAppUI()"></select>
                <select id="elective-select" onchange="updateAppUI()">
                    <option value="ree">ree</option>
                    <option value="sgc">sgc</option>
                    <option value="prpc">prpc</option>
                </select>
            </div>"""

orig = orig.replace(old_hidden_inputs, new_hidden_inputs)

old_populate_groups = """        // Populate Groups Dropdown (Hidden helper)
        function populateGroups() {
            const divSelect = document.getElementById("div-select");
            const groupSelect = document.getElementById("group-select");
            const division = divSelect.value;
            groupSelect.innerHTML = "";
            if (division === "1") {
                groupSelect.add(new Option("Group J1", "J1"));
                groupSelect.add(new Option("Group J2", "J2"));
            } else {
                groupSelect.add(new Option("Group J3", "J3"));
                groupSelect.add(new Option("Group J4", "J4"));
            }
        }"""

new_populate_groups = """        // Populate Groups Dropdown (Hidden helper)
        function populateGroups() {
            const divSelect = document.getElementById("div-select");
            const groupSelect = document.getElementById("group-select");
            const division = divSelect.value;
            groupSelect.innerHTML = "";
            if (division === "1") {
                groupSelect.add(new Option("Group E1", "E1"));
                groupSelect.add(new Option("Group E2", "E2"));
                groupSelect.add(new Option("Group E3", "E3"));
            } else if (division === "2") {
                groupSelect.add(new Option("Group E4", "E4"));
                groupSelect.add(new Option("Group E5", "E5"));
                groupSelect.add(new Option("Group E6", "E6"));
            } else if (division === "3") {
                groupSelect.add(new Option("Group E7", "E7"));
                groupSelect.add(new Option("Group E8", "E8"));
                groupSelect.add(new Option("Group E9", "E9"));
            }
        }"""

orig = orig.replace(old_populate_groups, new_populate_groups)

# Replace visual CSBS labels in the template with Chemical Engineering
orig = orig.replace("PDEU B.Tech CSBS · Sem 5", "PDEU B.Tech Chemical Engineering · Sem 5")
orig = orig.replace("CSBS Semester 5", "Chemical Engineering Semester 5")
orig = orig.replace("B.Tech Computer Science & Business Systems · Semester 5", "B.Tech Chemical Engineering · Semester 5")
orig = orig.replace("B.Tech CSBS · Sem 5", "B.Tech Chemical Engineering · Sem 5")
orig = orig.replace("Group J1", "Group E1")
orig = orig.replace("Group J2", "Group E1")

# 2. Update CSS classes in :root for Chemical subjects
subject_root_css = """
            /* Subject Theme Badges & Left Accent Borders */
            --color-cdc-bg: #f8fafc;
            --color-cdc-text: #334155;
            --color-cdc-border: #64748b;
            
            --color-mto-bg: #eff6ff;
            --color-mto-text: #1d4ed8;
            --color-mto-border: #2563eb;
            
            --color-cre-bg: #f0fdf4;
            --color-cre-text: #15803d;
            --color-cre-border: #16a34a;
            
            --color-ped-bg: #faf5ff;
            --color-ped-text: #7e22ce;
            --color-ped-border: #9333ea;
            
            --color-eco-bg: #fff7ed;
            --color-eco-text: #c2410c;
            --color-eco-border: #ea580c;
            
            --color-elective-bg: #fef9c3;
            --color-elective-text: #854d0e;
            --color-elective-border: #eab308;
"""

# Find subject CSS colors in original file and replace
css_start = orig.find("/* Subject Theme Badges")
css_end = orig.find("/* PDF Print Maroon Theme")
if css_start != -1 and css_end != -1:
    orig = orig[:css_start] + subject_root_css + orig[css_end:]

# 3. Update JavaScript mappings, databases, and schedules
# First find studentDatabase block
db_start_idx = orig.find("const studentDatabase = [")
db_end_idx = orig.find("];", db_start_idx)
if db_start_idx != -1 and db_end_idx != -1:
    orig = orig[:db_start_idx] + "const studentDatabase = " + student_db_js + orig[db_end_idx + 2:]

# Next replace electiveNames, electiveInfo, profFullNames, subjectFullNames, electiveSchedules, schedules
target_block_start = orig.find("const electiveNames = {")
target_block_end = orig.find("let currentDay = \"Monday\";", target_block_start)

new_js_block = """const electiveNames = {
            "ree": "Renewable Energy Engineering",
            "sgc": "Sustainability & Green Chemistry",
            "prpc": "Petroleum Refining & Petrochemicals"
        };

        const electiveInfo = {
            "ree": { code: "24CH332T", name: "Renewable Energy Engineering" },
            "sgc": { code: "24CH333T", name: "Sustainability & Green Chemistry" },
            "prpc": { code: "24CH331T", name: "Petroleum Refining & Petrochemicals" }
        };

        const profFullNames = {
            "ABY-L": "Prof. Abhishek Yadav",
            "ABY-P": "Prof. Abhishek Yadav (Lab)",
            "ASU-L": "Prof. Ashish Unnarkat",
            "ASU-P": "Prof. Ashish Unnarkat (Lab)",
            "AYD-L": "Prof. Ayush Dave",
            "AYD-P": "Prof. Ayush Dave (Lab)",
            "CDCT-L": "CD Cell Trainer",
            "GRRA-L": "Prof. Griva Raval",
            "HIC-L": "Prof. Himanshu Choksi",
            "HIC-P": "Prof. Himanshu Choksi (Lab)",
            "JAJ-L": "Prof. Jainesh Jhaveri",
            "JAJ-P": "Prof. Jainesh Jhaveri (Lab)",
            "MNS-P": "Prof. Manan Shah (Lab)",
            "MSI-L": "Prof. Manish Sinha",
            "MSI-P": "Prof. Manish Sinha (Lab)",
            "PRK-L": "Prof. Pravin Kodgire",
            "PRKU-L": "Prof. Prashant Kumar",
            "PRKU-P": "Prof. Prashant Kumar (Lab)",
            "SMIT-P": "Prof. Shirsendu Mitra (Lab)",
            "UDA-L": "Prof. Utsav Dalal",
            "UDA-P": "Prof. Utsav Dalal (Lab)"
        };

        // Helper function to format and combine multiple lab faculty names cleanly
        function getProfNames(profStr) {
            if (!profStr || profStr === "—") return "—";
            if (profStr.includes(" + ")) {
                return profStr.split(" + ").map(code => {
                    const cleanCode = code.trim();
                    let name = profFullNames[cleanCode] || cleanCode;
                    return name.replace(/\\s*\\(Lab\\)/gi, "");
                }).join(" & ");
            }
            return profFullNames[profStr] || profStr;
        }

        const subjectFullNames = {
            "CDC Training": "Career Development Training (CDC)",
            "Mass Transfer Operations - I": "Mass Transfer Operations - I",
            "Mass Transfer Operations - I Lab": "Mass Transfer Operations - I Lab",
            "Chemical Reaction Engineering I": "Chemical Reaction Engineering I",
            "Chemical Reaction Engineering I Lab": "Chemical Reaction Engineering I Lab",
            "Process Equipment Design": "Process Equipment Design",
            "Process Equipment Design Lab": "Process Equipment Design Lab",
            "Engineering Economics": "Engineering Economics"
        };

        const electiveSchedules = {
            "ree": {
                "Monday_13:10-14:05": { room: "E005", prof: "PRKU-L" },
                "Tuesday_13:10-14:05": { room: "E005", prof: "PRKU-L" },
                "Wednesday_13:10-14:05": { room: "E005", prof: "PRKU-L" }
            },
            "sgc": {
                "Monday_13:10-14:05": { room: "E101", prof: "PRK-L" },
                "Tuesday_13:10-14:05": { room: "E101", prof: "PRK-L" },
                "Wednesday_13:10-14:05": { room: "E101", prof: "PRK-L" }
            },
            "prpc": {
                "Monday_13:10-14:05": { room: "E004", prof: "AYD-L" },
                "Tuesday_13:10-14:05": { room: "E004", prof: "AYD-L" },
                "Wednesday_13:10-14:05": { room: "E004", prof: "AYD-L" }
            }
        };

        const schedules = """ + schedules_js + """;

        """

if target_block_start != -1 and target_block_end != -1:
    orig = orig[:target_block_start] + new_js_block + orig[target_block_end:]

# 4. Fix HTML title texts in DOM
orig = orig.replace("CSBS Timetable Console", "Chemical Engineering Console")
orig = orig.replace("PDEU B.Tech CSBS Semester 5 Timetable", "PDEU B.Tech Chemical Engineering Sem 5")
orig = orig.replace("Punit Gupta, Samir Dwivedi", "Ashish Unnarkat, Himanshu Choksi, Manish Sinha")
orig = orig.replace("CSBS Timetable System", "Chemical Engineering Timetable")

# Fix Default Student Preview Card to Chemical Student
orig = orig.replace("NIVKUMAR JAYANTILAL SORATHIYA", "Aaditya Manoj Agrawal")
orig = orig.replace("Group J2", "Group E1")
orig = orig.replace("Business Strategy", "Renewable Energy Engineering")
orig = orig.replace("24BCB037@sot.pdpu.ac.in", "24bch001@spt.pdpu.ac.in")

# Switch link to index.html
orig = orig.replace('Switch to Chemical Engineering Timetable ➔', 'Switch to CSBS Timetable ➔')
orig = orig.replace('href="chemical.html"', 'href="index.html"')

# 5. Customize UI classes mapping helper in javascript to match new colors
orig = orig.replace(
    'if (type.includes("dt")) return "type-dt";\n            if (type.includes("se")) return "type-se";\n            if (type.includes("cn")) return "type-cn";\n            if (type.includes("cloud")) return "type-cloud";\n            if (type.includes("cdcell")) return "type-cdcell";\n            if (type.includes("minor")) return "type-minor";',
    'if (type.includes("mto")) return "type-mto";\n            if (type.includes("cre")) return "type-cre";\n            if (type.includes("ped")) return "type-ped";\n            if (type.includes("eco")) return "type-eco";\n            if (type.includes("cdc")) return "type-cdc";'
)

# 6. Delete old pseudo-element active after CSS rule
old_active_after_css = """        .mobile-card.is-currently-active::after {
            content: 'LIVE NOW';
            position: absolute;
            top: 10px;
            right: 12px;
            background: #22c55e;
            color: #ffffff;
            font-size: 0.65rem;
            font-weight: 900;
            padding: 2px 8px;
            border-radius: 10px;
            box-shadow: 0 0 10px rgba(34, 197, 94, 0.5);
            animation: pulse 2s infinite;
        }"""
orig = orig.replace(old_active_after_css, "")

# 7. Premium Mobile Card styles optimization (offset vertical indicator pill, pulsing border glow, and live badge container)
old_mobile_card_css = """        /* Mobile Timeline Card Item */
        .mobile-card {
            background: var(--bg-surface);
            border: 1px solid var(--border-color);
            border-radius: 18px;
            padding: 1.1rem 1.25rem;
            display: flex;
            flex-direction: column;
            gap: 0.65rem;
            position: relative;
            overflow: hidden;
            transition: all 0.2s ease;
            box-shadow: 0 4px 15px rgba(0, 0, 0, 0.04);
        }

        .mobile-card::before {
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            width: 5px;
            height: 100%;
            background-color: var(--card-border-color, var(--accent-primary));
            border-radius: 5px 0 0 5px;
        }

        /* Currently Active Class Glow */
        .mobile-card.is-currently-active {
            border: 2px solid #22c55e;
            box-shadow: 0 8px 25px rgba(34, 197, 94, 0.25);
            background: #f0fdf4;
        }"""

new_mobile_card_css = """        /* Mobile Timeline Card Item (Premium Offset Pill style) */
        .mobile-card {
            background: var(--bg-surface);
            border: 1px solid var(--border-color);
            border-radius: 18px;
            padding: 1.1rem 1.25rem 1.1rem 1.75rem;
            display: flex;
            flex-direction: column;
            gap: 0.65rem;
            position: relative;
            overflow: hidden;
            transition: all 0.25s cubic-bezier(0.4, 0, 0.2, 1);
            box-shadow: 0 4px 18px rgba(0, 0, 0, 0.03);
        }

        .mobile-card:hover {
            transform: translateY(-2px);
            box-shadow: 0 8px 24px rgba(0, 0, 0, 0.06);
        }

        .mobile-card::before {
            content: '';
            position: absolute;
            top: 14px;
            left: 12px;
            width: 5px;
            height: calc(100% - 28px);
            background-color: var(--card-border-color, var(--accent-primary));
            border-radius: 99px;
        }

        @keyframes pulse-border-glow {
            0% {
                border-color: #22c55e;
                box-shadow: 0 4px 18px rgba(0, 0, 0, 0.03), 0 0 12px rgba(34, 197, 94, 0.2);
            }
            50% {
                border-color: #10b981;
                box-shadow: 0 8px 24px rgba(0, 0, 0, 0.05), 0 0 20px rgba(16, 185, 129, 0.45);
            }
            100% {
                border-color: #22c55e;
                box-shadow: 0 4px 18px rgba(0, 0, 0, 0.03), 0 0 12px rgba(34, 197, 94, 0.2);
            }
        }

        /* Currently Active Class Glow */
        .mobile-card.is-currently-active {
            border: 2px solid #22c55e;
            background: linear-gradient(135deg, #f0fdf4 0%, #ffffff 100%);
            animation: pulse-border-glow 2.5s infinite ease-in-out;
            padding-right: 5.5rem;
        }

        /* Live Indicator Badge (Moved to bottom right of card) */
        .live-indicator-badge {
            position: absolute;
            bottom: 12px;
            right: 14px;
            background: #22c55e;
            color: #ffffff;
            font-size: 0.62rem;
            font-weight: 800;
            padding: 3px 8px;
            border-radius: 99px;
            display: flex;
            align-items: center;
            gap: 5px;
            box-shadow: 0 2px 8px rgba(34, 197, 94, 0.3);
            letter-spacing: 0.03em;
        }

        .live-pulse-dot {
            width: 6px;
            height: 6px;
            background-color: #ffffff;
            border-radius: 50%;
            display: inline-block;
            animation: dot-pulse 1.5s infinite ease-in-out;
        }

        @keyframes dot-pulse {
            0% { transform: scale(0.8); opacity: 0.5; }
            50% { transform: scale(1.4); opacity: 1; }
            100% { transform: scale(0.8); opacity: 0.5; }
        }"""

orig = orig.replace(old_mobile_card_css, new_mobile_card_css)

orig = orig.replace(
    'const profileSummary = `Div ${loggedInStudent.div} &middot; ${loggedInStudent.group} &middot; ${electiveNames[loggedInStudent.elective]}`;',
    'const profileSummary = `Div ${loggedInStudent.div} &middot; Group ${loggedInStudent.group} &middot; ${electiveNames[loggedInStudent.elective]}`;'
)

# 8. Update isLunchSlot helper function
old_lunch_fn = """        function isLunchSlot(division, day, slot) {
            if (division === "1") {
                if (day === "Friday") return slot === "1:10 to 2:05";
                return slot === "12.10 to 1.05";
            } else {
                if (day === "Wednesday" || day === "Friday") return slot === "1:10 to 2:05";
                return slot === "12.10 to 1.05";
            }
        }"""

new_lunch_fn = """        function isLunchSlot(division, day, slot) {
            return slot === "12:10-13:05";
        }"""

orig = orig.replace(old_lunch_fn, new_lunch_fn)

# 9. Update timeRanges array inside updateLiveClockEngine()
old_clock_ranges = """            const timeRanges = [
                { start: 480, end: 535, slot: "08:00 to 08:55", label: "8:00 AM – 8:55 AM" },
                { start: 540, end: 595, slot: "9.00 to 9. 55", label: "9:00 AM – 9:55 AM" },
                { start: 600, end: 655, slot: "10.00 to 10.55", label: "10:00 AM – 10:55 AM" },
                { start: 655, end: 670, slot: "10:55 to 11:10", isBreak: true, label: "10:55 AM – 11:10 AM" },
                { start: 670, end: 725, slot: "11.10 to 12.05", label: "11:10 AM – 12:05 PM" },
                { start: 730, end: 785, slot: "12.10 to 1.05", label: "12:10 PM – 1:05 PM" },
                { start: 790, end: 845, slot: "1:10 to 2:05", label: "1:10 PM – 2:05 PM" },
                { start: 850, end: 905, slot: "2.10 to 3.05", label: "2:10 PM – 3:05 PM" },
                { start: 910, end: 965, slot: "3.10 to 4.05", label: "3:10 PM – 4:05 PM" },
                { start: 965, end: 975, slot: "4:05 to 4:15", isBreak: true, label: "4:05 PM – 4:15 PM" },
                { start: 975, end: 1030, slot: "4.15 to 5.10", label: "4:15 PM – 5:10 PM" },
                { start: 1035, end: 1090, slot: "5.15 to 6.10", label: "5:15 PM – 6:10 PM" }
            ];"""

new_clock_ranges = """            const timeRanges = [
                { start: 540, end: 595, slot: "09:00-09:55", label: "09:00 AM – 09:55 AM" },
                { start: 600, end: 655, slot: "10:00-10:55", label: "10:00 AM – 10:55 AM" },
                { start: 655, end: 670, slot: "10:55-11:10", isBreak: true, label: "10:55 AM – 11:10 AM" },
                { start: 670, end: 725, slot: "11:10-12:05", label: "11:10 AM – 12:05 PM" },
                { start: 730, end: 785, slot: "12:10-13:05", label: "12:10 PM – 01:05 PM" },
                { start: 790, end: 845, slot: "13:10-14:05", label: "01:10 PM – 02:05 PM" },
                { start: 850, end: 905, slot: "14:10-15:05", label: "02:10 PM – 03:05 PM" },
                { start: 910, end: 965, slot: "15:10-16:05", label: "03:10 PM – 04:05 PM" },
                { start: 965, end: 975, slot: "16:05-16:15", isBreak: true, label: "04:05 PM – 04:15 PM" },
                { start: 975, end: 1030, slot: "16:15-17:10", label: "04:15 PM – 05:10 PM" },
                { start: 1035, end: 1090, slot: "17:15-18:10", label: "05:15 PM – 6:10 PM" }
            ];"""

orig = orig.replace(old_clock_ranges, new_clock_ranges)

# 10. Update timeSlots array in renderMobileCards() with clean 12-hour hours format (AM/PM) without leading zeros
old_mobile_slots = """            const timeSlots = [
                { slot: "08:00 to 08:55", start: 480, end: 535, label: "8:00 AM – 8:55 AM" },
                { slot: "9.00 to 9. 55", start: 540, end: 595, label: "9:00 AM – 9:55 AM" },
                { slot: "10.00 to 10.55", start: 600, end: 655, label: "10:00 AM – 10:55 AM" },
                { slot: "10:55 to 11:10", start: 655, end: 670, label: "10:55 AM – 11:10 AM", type: "break" },
                { slot: "11.10 to 12.05", start: 670, end: 725, label: "11:10 AM – 12:05 PM" },
                { slot: "12.10 to 1.05", start: 730, end: 785, label: "12:10 PM – 1:05 PM" },
                { slot: "1:10 to 2:05", start: 790, end: 845, label: "1:10 PM – 2:05 PM" },
                { slot: "2.10 to 3.05", start: 850, end: 905, label: "2:10 PM – 3:05 PM" },
                { slot: "3.10 to 4.05", start: 910, end: 965, label: "3:10 PM – 4:05 PM" },
                { slot: "4:05 to 4:15", start: 965, end: 975, label: "4:05 PM – 4:15 PM", type: "break" },
                { slot: "4.15 to 5.10", start: 975, end: 1030, label: "4:15 PM – 5:10 PM" },
                { slot: "5.15 to 6.10", start: 1035, end: 1090, label: "5:15 PM – 6:10 PM" }
            ];"""

new_mobile_slots = """            const timeSlots = [
                { slot: "09:00-09:55", start: 540, end: 595, label: "9:00 AM – 9:55 AM" },
                { slot: "10:00-10:55", start: 600, end: 655, label: "10:00 AM – 10:55 AM" },
                { slot: "10:55-11:10", start: 655, end: 670, label: "10:55 AM – 11:10 AM", type: "break" },
                { slot: "11:10-12:05", start: 670, end: 725, label: "11:10 AM – 12:05 PM" },
                { slot: "12:10-13:05", start: 730, end: 785, label: "12:10 PM – 1:05 PM" },
                { slot: "13:10-14:05", start: 790, end: 845, label: "1:10 PM – 2:05 PM" },
                { slot: "14:10-15:05", start: 850, end: 905, label: "2:10 PM – 3:05 PM" },
                { slot: "15:10-16:05", start: 910, end: 965, label: "3:10 PM – 4:05 PM" },
                { slot: "16:05-16:15", start: 965, end: 975, label: "4:05 PM – 4:15 PM", type: "break" },
                { slot: "16:15-17:10", start: 975, end: 1030, label: "4:15 PM – 5:10 PM" },
                { slot: "17:15-18:10", start: 1035, end: 1090, label: "5:15 PM – 6:10 PM" }
            ];"""

orig = orig.replace(old_mobile_slots, new_mobile_slots)

# 11. Remove View Mode Switcher from HTML
old_switcher = """            <!-- View Mode Switcher -->
            <div class="mode-segmented-bar">
                <button id="btn-mode-cards" class="mode-btn active" onclick="switchViewMode('cards')">
                    <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><rect width="7" height="7" x="3" y="3" rx="1"/><rect width="7" height="7" x="14" y="3" rx="1"/><rect width="7" height="7" x="14" y="14" rx="1"/><rect width="7" height="7" x="3" y="14" rx="1"/></svg>
                    Mobile Cards
                </button>
                <button id="btn-mode-pdf" class="mode-btn" onclick="switchViewMode('blueprint')">
                    <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><path d="M14.5 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V7.5L14.5 2z"/><polyline points="14 2 14 8 20 8"/></svg>
                    A4 Blueprint View
                </button>
            </div>"""

orig = orig.replace(old_switcher, "")

# 12. Remove Blueprint Container & Floating Action Download Bar using robust regex
orig = re.sub(
    r'<!-- Landscape Blueprint View Container -->.*?<!-- Subject Inspection & Profile Detail Modal Sheet -->',
    '</div>\n\n    <!-- Subject Inspection & Profile Detail Modal Sheet -->',
    orig,
    flags=re.DOTALL
)

# 13. Update live device clock banner/dashboard box to include Next Class preview container & Personal Greeting (Clean Contrast styling)
old_status_card_html = """        <!-- Live Device Clock & Today's Status Banner Card -->
        <div class="live-status-card">
            <div class="live-card-top">
                <span class="live-date-text" id="live-date-str">Wednesday, Jul 22</span>
                <span class="live-clock-badge" id="live-clock-str">06:40 PM</span>
            </div>
            <div class="live-current-headline" id="live-headline">
                🟢 Today's Schedule Active
            </div>
            <div class="live-current-sub" id="live-subtext">
                Checking current timetable for your division & group...
            </div>
        </div>"""

new_status_card_html = """        <!-- Live Device Clock & Today's Status Banner Card (Extended with Next Class Preview & Greeting) -->
        <div class="live-status-card">
            <div id="live-greeting" style="font-size: 0.85rem; font-weight: 700; opacity: 0.9; letter-spacing: 0.02em;">Welcome!</div>
            <div class="live-card-top" style="margin-top: 0.15rem;">
                <span class="live-date-text" id="live-date-str">Wednesday, Jul 22</span>
                <span class="live-clock-badge" id="live-clock-str">06:40 PM</span>
            </div>
            <div class="live-current-headline" id="live-headline">
                🟢 Today's Schedule Active
            </div>
            <div class="live-current-sub" id="live-subtext">
                Checking current timetable for your division & group...
            </div>
            <!-- Next Class Container (Not highlighted, clean contrast design) -->
            <div id="live-next-container" style="margin-top: 0.6rem; padding-top: 0.6rem; border-top: 1px solid rgba(255, 255, 255, 0.2); display: none; flex-direction: column; gap: 0.2rem;">
                <div style="font-size: 0.65rem; text-transform: uppercase; font-weight: 850; letter-spacing: 0.05em; opacity: 0.7;">➡️ Next Class</div>
                <div style="font-size: 0.8rem; font-weight: 600; opacity: 0.9;" id="live-next-headline">Next Class Title</div>
                <div style="font-size: 0.72rem; opacity: 0.75;" id="live-next-subtext">Next Class Room & Prof</div>
            </div>
        </div>"""

orig = orig.replace(old_status_card_html, new_status_card_html)

# 14. Update openProfileSheet() to show clean profile info (No PDF download options)
old_profile_sheet = """        // Open Profile Sheet Modal
        function openProfileSheet() {
            if (!loggedInStudent) {
                showLoginModal();
                return;
            }

            const grid = document.getElementById("modal-details-grid");
            document.getElementById("modal-title").innerText = loggedInStudent.name;
            document.getElementById("modal-code").innerText = `Roll Number: ${loggedInStudent.roll}`;

            grid.innerHTML = `
                <div class="detail-card">
                    <span class="detail-label">Student Email</span>
                    <span class="detail-value">${loggedInStudent.email}</span>
                </div>
                <div class="detail-card">
                    <span class="detail-label">Division & Group</span>
                    <span class="detail-value">Division ${loggedInStudent.div} · Group ${loggedInStudent.group}</span>
                </div>
                <div class="detail-card">
                    <span class="detail-label">Chosen Elective Subject</span>
                    <span class="detail-value">${electiveNames[loggedInStudent.elective]}</span>
                </div>
                <button class="switch-account-btn" onclick="switchAccountAction()">
                    <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><path d="M21 12a9 9 0 0 0-9-9 9.75 9.75 0 0 0-6.74 2.74L3 8"/><path d="M3 3v5h5"/><path d="M3 12a9 9 0 0 0 9 9 9.75 9.75 0 0 0 6.74-2.74L21 16"/><path d="M16 16h5v5"/></svg>
                    Switch Profile / Login Different Roll No
                </button>
            `;

            document.getElementById("detail-modal").classList.add("active");
        }"""

new_profile_sheet = """        // Open Profile Sheet Modal
        function openProfileSheet() {
            if (!loggedInStudent) {
                showLoginModal();
                return;
            }

            const grid = document.getElementById("modal-details-grid");
            document.getElementById("modal-title").innerText = loggedInStudent.name;
            document.getElementById("modal-code").innerText = `Roll Number: ${loggedInStudent.roll}`;

            grid.innerHTML = `
                <div class="detail-card">
                    <span class="detail-label">Student Email</span>
                    <span class="detail-value">${loggedInStudent.email}</span>
                </div>
                <div class="detail-card">
                    <span class="detail-label">Division & Group</span>
                    <span class="detail-value">Division ${loggedInStudent.div} · Group ${loggedInStudent.group}</span>
                </div>
                <div class="detail-card">
                    <span class="detail-label">Chosen Elective Subject</span>
                    <span class="detail-value">${electiveNames[loggedInStudent.elective]}</span>
                </div>
                <button class="switch-account-btn" onclick="switchAccountAction()">
                    <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><path d="M21 12a9 9 0 0 0-9-9 9.75 9.75 0 0 0-6.74 2.74L3 8"/><path d="M3 3v5h5"/><path d="M3 12a9 9 0 0 0 9 9 9.75 9.75 0 0 0 6.74-2.74L21 16"/><path d="M16 16h5v5"/></svg>
                    Switch Profile / Login Different Roll No
                </button>
            `;

            document.getElementById("detail-modal").classList.add("active");
        }"""

orig = orig.replace(old_profile_sheet, new_profile_sheet)

# 15. Update switchViewMode to be a no-op (enforces cards mode only)
old_switch_view_mode = """        // View Mode Switcher ("cards" or "blueprint")
        function switchViewMode(mode) {
            currentMode = mode;
            const btnCards = document.getElementById("btn-mode-cards");
            const btnPdf = document.getElementById("btn-mode-pdf");
            const dayNavBar = document.getElementById("day-nav-bar");
            const cardsView = document.getElementById("mobile-cards-view");
            const blueprintView = document.getElementById("blueprint-view-container");

            if (mode === 'cards') {
                btnCards.classList.add('active');
                btnPdf.classList.remove('active');
                dayNavBar.style.display = 'flex';
                cardsView.style.display = 'flex';
                blueprintView.style.display = 'none';
            } else {
                btnPdf.classList.add('active');
                btnCards.classList.remove('active');
                dayNavBar.style.display = 'none';
                cardsView.style.display = 'none';
                blueprintView.style.display = 'block';
                adjustScale();
            }
        }"""

new_switch_view_mode = """        // View Mode Switcher (Enforces cards mode only)
        function switchViewMode(mode) {
            currentMode = 'cards';
        }"""

orig = orig.replace(old_switch_view_mode, new_switch_view_mode)

# 16. Update updateAppUI() to only render mobile cards & clock
old_update_ui = """        // Main Refresh Function
        function updateAppUI() {
            renderMobileCards();
            renderBlueprintGrid();
            updateLiveClockEngine();
        }"""

new_update_ui = """        // Main Refresh Function
        function updateAppUI() {
            renderMobileCards();
            updateLiveClockEngine();
        }

        // Blueprint elements removed
        function renderBlueprintGrid() {}
        function adjustScale() {}
        function downloadCustomPDF() {}
        function downloadOfficialPDF() {}"""

orig = orig.replace(old_update_ui, new_update_ui)

# 17. Replace downloadTimetablePDF() with a clean empty no-op
old_download_func = """        // Download High-Resolution A4 PDF (Works from both Mobile Cards & Blueprint views)
        function downloadTimetablePDF() {
            const container = document.getElementById("blueprint-view-container");
            const element = document.getElementById("timetable-pdf-sheet");
            
            const isHidden = (window.getComputedStyle(container).display === "none");

            if (isHidden) {
                container.style.position = "absolute";
                container.style.left = "-9999px";
                container.style.top = "-9999px";
                container.style.display = "block";
            }

            const originalTransform = element.style.transform;
            element.style.transform = "none";

            const division = document.getElementById("div-select").value;
            const group = document.getElementById("group-select").value;
            const electiveSelect = document.getElementById("elective-select");
            const electiveName = electiveSelect.options[electiveSelect.selectedIndex].text.replace(/\s+/g, '');
            const filename = `Timetable_Div${division}_${group}_${electiveName}.pdf`;

            const opt = {
                margin:       0,
                filename:     filename,
                image:        { type: 'jpeg', quality: 0.98 },
                html2canvas:  { scale: 2.5, useCORS: true, letterRendering: true },
                jsPDF:        { unit: 'in', format: 'a4', orientation: 'landscape' }
            };

            html2pdf().set(opt).from(element).save().then(() => {
                element.style.transform = originalTransform;
                if (isHidden) {
                    container.style.display = "none";
                    container.style.position = "";
                    container.style.left = "";
                    container.style.top = "";
                }
            });
        }"""

new_download_func = """        // PDF Timetable Downloads Disabled
        function downloadTimetablePDF() {}"""

orig = orig.replace(old_download_func, new_download_func)

# 18. Add Automatic Background Cache-Buster and Version Check
old_script_start = """    <script>
        // Official Database of all 112 CSBS Students (Regular + Diploma)"""

new_script_start = """    <script>
        // Automatic cache buster and version check to clear stale service workers/cache
        (function() {
            const CURRENT_VERSION = "1.1.3";
            const savedVersion = localStorage.getItem("chemical_app_version");
            if (savedVersion !== CURRENT_VERSION) {
                localStorage.setItem("chemical_app_version", CURRENT_VERSION);
                localStorage.removeItem("chemical_user_roll");
                if (typeof navigator !== 'undefined' && 'serviceWorker' in navigator) {
                    navigator.serviceWorker.getRegistrations().then(function(registrations) {
                        for(let registration of registrations) {
                            registration.unregister();
                        }
                    });
                }
                if (typeof window !== 'undefined' && window.location && typeof window.location.reload === 'function') {
                    window.location.reload(true);
                }
            }
        })();

        // Official Database of all 112 CSBS Students (Regular + Diploma)"""

orig = orig.replace(old_script_start, new_script_start)

# 19. Standard switch account action
old_switch_action = """        function switchAccountAction() {
            closeModal();
            localStorage.removeItem("csbs_user_roll");
            showLoginModal();
        }"""

new_switch_action = """        function switchAccountAction() {
            closeModal();
            localStorage.removeItem("chemical_user_roll");
            showLoginModal();
        }"""

orig = orig.replace(old_switch_action, new_switch_action)

# 20. Inject new updateLiveClockEngine JS logic with next class previewing & time of day greetings (12-hour format slot keys, no leading zeros)
clock_engine_start = orig.find("function updateLiveClockEngine() {")
clock_engine_end = orig.find("// 1. Render Mobile Timeline Cards", clock_engine_start)
new_clock_engine_js = """function updateLiveClockEngine() {
            const now = new Date();
            const daysMap = ["Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"];
            const todayName = daysMap[now.getDay()];
            
            // Format Live Date & Time String
            const options = { weekday: 'long', month: 'short', day: 'numeric', year: 'numeric' };
            document.getElementById("live-date-str").innerText = now.toLocaleDateString('en-US', options);
            
            // Force 12-hour format with AM/PM explicitly without leading zeros for hours
            document.getElementById("live-clock-str").innerText = now.toLocaleTimeString([], { hour: 'numeric', minute: '2-digit', hour12: true });

            // Generate dynamic time-of-day greeting (Good Morning, Afternoon, Evening, Night)
            const hours = now.getHours();
            let greetingStr = "Hello";
            if (hours >= 5 && hours < 12) {
                greetingStr = "Good Morning";
            } else if (hours >= 12 && hours < 17) {
                greetingStr = "Good Afternoon";
            } else if (hours >= 17 && hours < 21) {
                greetingStr = "Good Evening";
            } else {
                greetingStr = "Good Night";
            }
            const greetingName = loggedInStudent ? getFirstName(loggedInStudent.name) : "Student";
            const greetingElem = document.getElementById("live-greeting");
            if (greetingElem) {
                greetingElem.innerText = `${greetingStr}, ${greetingName}!`;
            }

            const currentMinutes = now.getHours() * 60 + now.getMinutes();

            const headline = document.getElementById("live-headline");
            const subtext = document.getElementById("live-subtext");
            const nextContainer = document.getElementById("live-next-container");

            if (todayName === "Sunday" || todayName === "Saturday") {
                headline.innerHTML = "☕ Weekend — No Classes Today";
                subtext.innerText = "Enjoy your weekend break! Classes resume Monday 9:00 AM.";
                if (nextContainer) nextContainer.style.display = "none";
                return;
            }

            const division = document.getElementById("div-select").value;
            const group = document.getElementById("group-select").value;
            const electiveKey = document.getElementById("elective-select").value;
            const divKey = "div" + division;
            const activeSchedule = schedules[divKey][group];
            const activeElectiveName = electiveNames[electiveKey];

            // Define Time Slot Minute Boundaries
            const timeRanges = [
                { start: 540, end: 595, slot: "09:00-09:55", label: "9:00 AM – 9:55 AM" },
                { start: 600, end: 655, slot: "10:00-10:55", label: "10:00 AM – 10:55 AM" },
                { start: 655, end: 670, slot: "10:55-11:10", isBreak: true, label: "10:55 AM – 11:10 AM" },
                { start: 670, end: 725, slot: "11:10-12:05", label: "11:10 AM – 12:05 PM" },
                { start: 730, end: 785, slot: "12:10-13:05", label: "12:10 PM – 1:05 PM" },
                { start: 790, end: 845, slot: "13:10-14:05", label: "1:10 PM – 2:05 PM" },
                { start: 850, end: 905, slot: "14:10-15:05", label: "2:10 PM – 3:05 PM" },
                { start: 910, end: 965, slot: "15:10-16:05", label: "3:10 PM – 4:05 PM" },
                { start: 965, end: 975, slot: "16:05-16:15", isBreak: true, label: "4:05 PM – 4:15 PM" },
                { start: 975, end: 1030, slot: "16:15-17:10", label: "4:15 PM – 5:10 PM" },
                { start: 1035, end: 1090, slot: "17:15-18:10", label: "5:15 PM – 6:10 PM" }
            ];

            // Find next class preview first to populate container
            let nextClassMatch = null;
            let nextClassData = null;
            for (let range of timeRanges) {
                if (range.start >= currentMinutes) {
                    if (range.isBreak) continue;
                    if (isLunchSlot(division, todayName, range.slot)) continue;
                    
                    let data = activeSchedule[todayName] ? activeSchedule[todayName][range.slot] : null;
                    if (data) {
                        if (data === "ELECTIVE") {
                            const electiveSchedKey = `${todayName}_${range.slot}`;
                            const electiveDetails = electiveSchedules[electiveKey][electiveSchedKey];
                            data = {
                                title: activeElectiveName,
                                code: electiveInfo[electiveKey].code,
                                room: electiveDetails ? electiveDetails.room : "—",
                                prof: electiveDetails ? electiveDetails.prof : "—"
                            };
                        }
                        nextClassMatch = range;
                        nextClassData = data;
                        break;
                    }
                }
            }

            if (nextContainer) {
                if (nextClassMatch && nextClassData) {
                    nextContainer.style.display = "flex";
                    // Timing formatted in 12-hour format without leading zero (e.g. 2:10 PM – 3:05 PM)
                    const timing12h = nextClassMatch.label.replace(/^0/, '');
                    document.getElementById("live-next-headline").innerText = `${subjectFullNames[nextClassData.title] || nextClassData.title} (${timing12h})`;
                    const nextProfName = getProfNames(nextClassData.prof);
                    document.getElementById("live-next-subtext").innerText = `Room: ${nextClassData.room || '—'} · Faculty: ${nextProfName}`;
                } else {
                    nextContainer.style.display = "none";
                }
            }

            // 1. Check if before first class
            if (currentMinutes < 540) {
                headline.innerHTML = "🌅 Morning — Classes Start at 9:00 AM";
                subtext.innerText = `First lecture for Div ${division} (${group}): class starts at 9:00 AM.`;
                return;
            }

            // 2. Check if after last class
            if (currentMinutes > 1090) {
                headline.innerHTML = "🌙 Evening — All Classes Completed Today";
                subtext.innerText = "No more lectures scheduled for today. Have a great evening!";
                if (nextContainer) nextContainer.style.display = "none";
                return;
            }

            // 3. Find active slot right now
            let activeMatch = null;
            for (let range of timeRanges) {
                if (currentMinutes >= range.start && currentMinutes < range.end) {
                    activeMatch = range;
                    break;
                }
            }

            if (activeMatch) {
                if (activeMatch.isBreak) {
                    headline.innerHTML = "☕ Short Break Right Now";
                    subtext.innerText = `Classes resume shortly at ${activeMatch.end === 670 ? '11:10 AM' : '4:15 PM'}.`;
                    return;
                }

                if (isLunchSlot(division, todayName, activeMatch.slot)) {
                    headline.innerHTML = "🍱 Lunch Break Time Right Now";
                    subtext.innerText = "Enjoy your lunch! Next class starts at 1:10 PM.";
                    return;
                }

                let cellData = activeSchedule[todayName] ? activeSchedule[todayName][activeMatch.slot] : null;

                if (cellData === "ELECTIVE") {
                    const electiveSchedKey = `${todayName}_${activeMatch.slot}`;
                    const electiveDetails = electiveSchedules[electiveKey][electiveSchedKey];
                    cellData = {
                        title: activeElectiveName,
                        code: electiveInfo[electiveKey].code,
                        room: electiveDetails ? electiveDetails.room : "—",
                        prof: electiveDetails ? electiveDetails.prof : "—"
                    };
                }

                if (cellData) {
                    const fullSubject = subjectFullNames[cellData.title] || cellData.title;
                    const fullProf = getProfNames(cellData.prof);
                    headline.innerHTML = `🟢 NOW: ${fullSubject}`;
                    subtext.innerText = `Room ${cellData.room || '—'} · ${fullProf} (${activeMatch.label.replace(/^0/, '')})`;
                    return;
                } else {
                    headline.innerHTML = "📖 Free Study Slot";
                    subtext.innerText = `No lecture scheduled for Group ${group} during this time slot (${activeMatch.label.replace(/^0/, '')}).`;
                    return;
                }
            }

            headline.innerHTML = "⏱️ Passing Time / Between Slots";
            subtext.innerText = `Next slot starting soon for Division ${division} Group ${group}.`;
        }

        """
if clock_engine_start != -1 and clock_engine_end != -1:
    orig = orig[:clock_engine_start] + new_clock_engine_js + orig[clock_engine_end:]

# 21. Inject new card template inside renderMobileCards() to append the bottom right live-indicator-badge
old_card_template_str = """                    card.innerHTML = `
                        <div class="card-top">
                            <div class="card-time">
                                <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><circle cx="12" cy="12" r="10"/><polyline points="12 6 12 12 16 14"/></svg>
                                ${endLabel}
                            </div>
                            <span class="card-badge" style="background: var(--color-${cellData.type.replace('-lab','')}-bg); color: var(--color-${cellData.type.replace('-lab','')}-text);">
                                ${cellData.type.toUpperCase().replace('-LAB', ' LAB')}
                            </span>
                        </div>
                        <div class="card-title">${fullSubjectTitle}</div>
                        ${cellData.isLab ? `<div class="lab-span-badge">★ 2-Hour Practical Lab Session</div>` : ''}
                        <div class="card-meta">
                            <div class="meta-pill">
                                <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><path d="M20 10c0 6-8 12-8 12s-8-6-8-12a8 8 0 0 1 16 0Z"/><circle cx="12" cy="10" r="3"/></svg>
                                <span>Room: <strong>${cellData.room || '—'}</strong></span>
                            </div>
                            <div class="meta-pill">
                                <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><path d="M19 21v-2a4 4 0 0 0-4-4H9a4 4 0 0 0-4 4v2"/><circle cx="12" cy="7" r="4"/></svg>
                                <span>Prof: <strong>${fullProfName}</strong></span>
                            </div>
                        </div>
                    `;"""

new_card_template_str = """                    card.innerHTML = `
                        <div class="card-top">
                            <div class="card-time">
                                <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><circle cx="12" cy="12" r="10"/><polyline points="12 6 12 12 16 14"/></svg>
                                ${endLabel.replace(/^0/, '')}
                            </div>
                            <span class="card-badge" style="background: var(--color-${cellData.type.replace('-lab','')}-bg); color: var(--color-${cellData.type.replace('-lab','')}-text);">
                                ${cellData.type.toUpperCase().replace('-LAB', ' LAB')}
                            </span>
                        </div>
                        <div class="card-title">${fullSubjectTitle}</div>
                        ${cellData.isLab ? `<div class="lab-span-badge">★ 2-Hour Practical Lab Session</div>` : ''}
                        <div class="card-meta">
                            <div class="meta-pill">
                                <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><path d="M20 10c0 6-8 12-8 12s-8-6-8-12a8 8 0 0 1 16 0Z"/><circle cx="12" cy="10" r="3"/></svg>
                                <span>Room: <strong>${cellData.room || '—'}</strong></span>
                            </div>
                            <div class="meta-pill">
                                <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><path d="M19 21v-2a4 4 0 0 0-4-4H9a4 4 0 0 0-4 4v2"/><circle cx="12" cy="7" r="4"/></svg>
                                <span>Prof: <strong>${fullProfName}</strong></span>
                            </div>
                        </div>
                        ${isCurrentlyActive ? `
                        <div class="live-indicator-badge">
                            <span class="live-pulse-dot"></span>
                            <span>LIVE NOW</span>
                        </div>
                        ` : ''}
                    `;"""

orig = orig.replace(old_card_template_str, new_card_template_str)

# 22. Update Saturday break card template to show Breaking Bad theme card with student name dynamic replacement
old_saturday_check = """            if (currentDay === "Saturday") {
                container.innerHTML = `
                    <div class="mobile-card is-break">
                        <div class="card-title" style="text-align: center; width: 100%; font-style: italic; padding: 1.5rem 0; color: var(--text-secondary);">
                            ☕ Saturday — No Classes Scheduled
                        </div>
                    </div>
                `;
                return;
            }"""

new_saturday_check = """            if (currentDay === "Saturday") {
                const saturdayName = loggedInStudent ? getFirstName(loggedInStudent.name) : "Jesse";
                container.innerHTML = `
                    <div class="saturday-card" style="display: flex; flex-direction: column; align-items: center; justify-content: center; background: #0f172a; border-radius: 20px; padding: 1.5rem; border: 1px solid #1e293b; box-shadow: 0 10px 30px rgba(0,0,0,0.25); text-align: center; color: #f8fafc; overflow: hidden; gap: 1rem; margin-top: 0.5rem;">
                        <img src=\"""" + breaking_bad_src + """\" alt="Breaking Bad" style="width: 100%; border-radius: 12px; max-height: 280px; object-fit: cover; box-shadow: 0 4px 15px rgba(0,0,0,0.3);" />
                        <div style="display: flex; flex-direction: column; gap: 0.4rem; padding: 0.5rem 0.2rem 0.2rem 0.2rem;">
                            <div style="font-size: 1.15rem; font-weight: 850; color: #4ade80; letter-spacing: -0.01em;">🧪 ${saturdayName}, we don't need to cook today!</div>
                            <div style="font-size: 0.88rem; font-weight: 550; color: #94a3b8; line-height: 1.45;">No classes scheduled for Saturday. Enjoy your weekend break! We start cooking again from Monday. ⚗️</div>
                        </div>
                    </div>
                `;
                return;
            }"""

orig = orig.replace(old_saturday_check, new_saturday_check)

# 23. Replace profFullNames lookup in renderMobileCards with getProfNames helper
orig = orig.replace(
    "const fullProfName = profFullNames[cellData.prof] || cellData.prof || \"—\";",
    "const fullProfName = getProfNames(cellData.prof);"
)

# 24. Replace highlightActiveDayChip in JS to scroll the active day chip into middle of nav bar
old_highlight_fn = """        function highlightActiveDayChip(todayName) {
            const daysOrder = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"];
            daysOrder.forEach((dName) => {
                const chip = document.getElementById(`chip-${dName}`);
                if (!chip) return;
                
                if (dName === currentDay) {
                    chip.classList.add("active");
                } else {
                    chip.classList.remove("active");
                }

                if (dName === todayName) {
                    chip.classList.add("is-today");
                } else {
                    chip.classList.remove("is-today");
                }
            });
        }"""

new_highlight_fn = """        function highlightActiveDayChip(todayName) {
            const daysOrder = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"];
            daysOrder.forEach((dName) => {
                const chip = document.getElementById(`chip-${dName}`);
                if (!chip) return;
                
                if (dName === currentDay) {
                    chip.classList.add("active");
                } else {
                    chip.classList.remove("active");
                }

                if (dName === todayName) {
                    chip.classList.add("is-today");
                } else {
                    chip.classList.remove("is-today");
                }
            });

            // Scroll the active day chip into the center of the day selection bar
            const activeChip = document.getElementById(`chip-${currentDay}`);
            if (activeChip) {
                setTimeout(() => {
                    activeChip.scrollIntoView({ behavior: 'smooth', block: 'nearest', inline: 'center' });
                }, 100);
            }
        }"""

orig = orig.replace(old_highlight_fn, new_highlight_fn)

# 25. Replace user-profile-badge-bar CSS styles with responsive flex-wrap layout
old_badge_bar_css = """        /* Clean Auto-Assigned Profile Badge Bar (Replaces Manual Dropdowns) */
        .user-profile-badge-bar {
            display: grid;
            grid-template-columns: 1fr 1fr 1.3fr;
            gap: 0.5rem;
            background: #f8fafc;
            border: 1px solid #e2e8f0;
            border-radius: 14px;
            padding: 0.6rem 0.75rem;
        }

        .profile-badge-item {
            display: flex;
            flex-direction: column;
            gap: 0.15rem;
        }

        .profile-badge-item .badge-label {
            font-size: 0.65rem;
            font-weight: 700;
            color: var(--text-tertiary);
            text-transform: uppercase;
            letter-spacing: 0.05em;
        }

        .profile-badge-item strong {
            font-size: 0.82rem;
            font-weight: 800;
            color: #0f172a;
            white-space: nowrap;
            overflow: hidden;
            text-overflow: ellipsis;
        }"""

new_badge_bar_css = """        /* Clean Auto-Assigned Profile Badge Bar (Replaces Manual Dropdowns) */
        .user-profile-badge-bar {
            display: grid;
            grid-template-columns: 1fr 1fr 1.3fr;
            gap: 0.5rem;
            background: #f8fafc;
            border: 1px solid #e2e8f0;
            border-radius: 14px;
            padding: 0.6rem 0.75rem;
        }

        .profile-badge-item {
            display: flex;
            flex-direction: column;
            gap: 0.15rem;
        }

        .profile-badge-item .badge-label {
            font-size: 0.65rem;
            font-weight: 700;
            color: var(--text-tertiary);
            text-transform: uppercase;
            letter-spacing: 0.05em;
        }

        .profile-badge-item strong {
            font-size: 0.82rem;
            font-weight: 800;
            color: #0f172a;
            white-space: nowrap;
            overflow: hidden;
            text-overflow: ellipsis;
        }

        @media (max-width: 480px) {
            .user-profile-badge-bar {
                display: flex;
                flex-wrap: wrap;
                gap: 0.6rem;
            }
            .profile-badge-item {
                flex: 1 1 calc(50% - 0.3rem);
            }
            .profile-badge-item:last-child {
                flex: 1 1 100%;
                border-top: 1px solid #e2e8f0;
                padding-top: 0.5rem;
                margin-top: 0.1rem;
            }
            .profile-badge-item:last-child strong {
                white-space: normal;
                overflow: visible;
                text-overflow: clip;
                line-height: 1.3;
            }
        }"""

orig = orig.replace(old_badge_bar_css, new_badge_bar_css)

# Write to chemical.html
output_file = "/Users/nivsorathiya/Desktop/pdeu-timetable/chemical.html"
with open(output_file, "w", encoding="utf-8") as f:
    f.write(orig)

print(f"Successfully generated Chemical Engineering Timetable: {output_file}")
