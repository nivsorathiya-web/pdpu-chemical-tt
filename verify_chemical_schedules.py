import subprocess
import json

file_path = "/Users/nivsorathiya/Desktop/pdeu-timetable/chemical.html"

# Run node to extract and dump schedules as clean JSON
node_code = """
const fs = require('fs');
const content = fs.readFileSync('""" + file_path + """', 'utf8');
const match = content.match(/const schedules = ({[\\s\\S]*?});\\s*\\n/);
if (match) {
    try {
        const sched = eval('(' + match[1] + ')');
        console.log(JSON.stringify(sched));
    } catch (e) {
        console.error('JS Eval Error:', e);
        process.exit(1);
    }
} else {
    console.error('const schedules regex match not found');
    process.exit(1);
}
"""

try:
    result = subprocess.run(['node', '-e', node_code], capture_output=True, text=True, check=True)
    schedules = json.loads(result.stdout)
    print("Success: schedules JS variable evaluated successfully via Node.js!")
    print("Divisions found in database:", list(schedules.keys()))
    
    # Check each division has its groups
    expected = {
        'div1': ['E1', 'E2', 'E3'],
        'div2': ['E4', 'E5', 'E6'],
        'div3': ['E7', 'E8', 'E9']
    }
    
    for div, groups in expected.items():
        if div not in schedules:
            print(f"Error: {div} not found in schedules!")
            exit(1)
        for group in groups:
            if group not in schedules[div]:
                print(f"Error: Group {group} not found in schedules[{div}]!")
                exit(1)
            # Check days
            days = list(schedules[div][group].keys())
            if not days:
                print(f"Warning: Group {group} schedule is empty!")
            else:
                print(f"Verified: {div} Group {group} has schedule for days: {days}")
                # Check sample day (Monday) slots
                mon_slots = list(schedules[div][group].get('Monday', {}).keys())
                print(f"  Monday slots for {group}: {mon_slots}")
                
except subprocess.CalledProcessError as e:
    print(f"Subprocess failed: {e.stderr}")
    exit(1)
except Exception as e:
    print(f"Verification script failed: {e}")
    exit(1)
