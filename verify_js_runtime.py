import subprocess
import os

html_path = "/Users/nivsorathiya/Desktop/pdeu-timetable/chemical.html"
with open(html_path, "r", encoding="utf-8") as f:
    html = f.read()

# Extract script content
script_start = html.find("<script>") + len("<script>")
script_end = html.find("</script>", script_start)
script_code = html[script_start:script_end]

# Node script wrapper with stubs for browser objects
node_code = """
// Browser Stubs
global.saturdayName = "Student";
const elementsCache = {};
global.document = {
    getElementById: (id) => {
        if (!elementsCache[id]) {
            elementsCache[id] = {
                id: id,
                classList: {
                    add: () => {},
                    remove: () => {}
                },
                style: {},
                options: [{ text: "RenewableEnergyEngineering", value: "ree" }],
                selectedIndex: 0,
                value: "",
                innerText: "",
                innerHTML: "",
                appendChild: () => {},
                add: (opt) => {
                    if (!elementsCache[id].optionsList) elementsCache[id].optionsList = [];
                    elementsCache[id].optionsList.push(opt);
                }
            };
        }
        return elementsCache[id];
    },
    querySelector: () => ({
        offsetWidth: 800,
        offsetHeight: 600,
        style: {}
    }),
    createElement: () => ({
        style: {
            setProperty: () => {}
        },
        classList: { add: () => {} },
        appendChild: () => {}
    })
};

global.navigator = {
    userAgent: "Mozilla/5.0 (iPhone; CPU iPhone OS 16_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.0 Mobile/15E148 Safari/604.1",
    standalone: false
};

global.window = {
    addEventListener: () => {},
    getComputedStyle: () => ({ display: "block" }),
    navigator: global.navigator
};

global.setInterval = () => {};
global.setTimeout = () => {};

global.localStorage = {
    getItem: () => "24BCH140",
    setItem: () => {},
    removeItem: () => {}
};

// Option class helper
global.Option = class Option {
    constructor(text, value) {
        this.text = text;
        this.value = value;
    }
};

global.location = {
    reload: () => {}
};

// Inline HTML2PDF stub
global.html2pdf = () => ({
    set: () => ({
        from: () => ({
            save: () => Promise.resolve()
        })
    })
});

// Evaluate the script code
try {
    eval(`{script_code}`);
    console.log("Success: Script parsed successfully in JS engine.");
    
    // Simulate window onload event
    if (typeof window.onload === 'function') {
        window.onload();
        console.log("Success: window.onload() executed.");
    } else {
        console.log("Error: window.onload is not a function.");
        process.exit(1);
    }
    
    // Let's print the logged in student to verify
    // console.log("Logged in student:", loggedInStudent);
    
    // Simulate updating UI
    updateAppUI();
    console.log("Success: updateAppUI() executed without errors!");
    
    // Verify that the dropdowns were populated with the correct Chemical Engineering options
    const divSelect = document.getElementById("div-select");
    const groupSelect = document.getElementById("group-select");
    const electiveSelect = document.getElementById("elective-select");
    
    console.log("div-select value:", divSelect.value);
    console.log("group-select options populated:", groupSelect.optionsList ? groupSelect.optionsList.map(o => o.value) : []);
    
} catch (e) {
    console.error("Runtime Crash Error:", e);
    process.exit(1);
}
""".replace("{script_code}", script_code.replace("`", "\\`").replace("${", "\\${"))

# Save and run node script
temp_js = "/Users/nivsorathiya/.gemini/antigravity/brain/86195e86-71e1-4bcf-ad67-a126f4380a93/scratch/test_js_runtime.js"
with open(temp_js, "w", encoding="utf-8") as f:
    f.write(node_code)

try:
    res = subprocess.run(["node", temp_js], capture_output=True, text=True, check=True)
    print("=== Execution Logs ===")
    print(res.stdout)
except subprocess.CalledProcessError as e:
    print("=== Execution Failed ===")
    print(e.stderr)
    print(e.stdout)
