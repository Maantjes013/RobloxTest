import json
import os

# --- CONFIGURATION ---
FILENAME = "20251109 Go Ahead Eagles vs Feyenoord SciSportsEvents - 2560935.json"
OUTPUT_FILE = "structure_output.txt"
# ---------------------

def analyze_structure():
    if not os.path.exists(FILENAME):
        print(f"Error: Could not find file '{FILENAME}'")
        return

    print(f"Reading {FILENAME}...")
    
    try:
        with open(FILENAME, 'r', encoding='utf-8') as f:
            data = json.load(f)
    except Exception as e:
        print(f"Error parsing JSON: {e}")
        return

    with open(OUTPUT_FILE, 'w', encoding='utf-8') as out:
        out.write("=== JSON STRUCTURE ANALYSIS ===\n\n")
        
        # Check if Root is List or Dict
        if isinstance(data, list):
            out.write(f"Root Type: LIST (Length: {len(data)})\n")
            if len(data) > 0:
                out.write("\n--- FIRST ITEM IN LIST (SAMPLE) ---\n")
                out.write(json.dumps(data[0], indent=4))
        
        elif isinstance(data, dict):
            out.write(f"Root Type: DICT (Keys: {list(data.keys())})\n")
            
            # If it's a dict, look for a key that might hold the list
            found_list = False
            for key, value in data.items():
                if isinstance(value, list):
                    out.write(f"\n--- FOUND LIST UNDER KEY: '{key}' (Length: {len(value)}) ---\n")
                    if len(value) > 0:
                        out.write(f"--- SAMPLE ITEM FROM '{key}' ---\n")
                        # Dump the first item so we see the keys (baseTypeName, etc.)
                        out.write(json.dumps(value[0], indent=4))
                        
                        # If there is a second item, dump that too just in case
                        if len(value) > 1:
                            out.write(f"\n\n--- SECOND ITEM FROM '{key}' ---\n")
                            out.write(json.dumps(value[1], indent=4))
                    found_list = True
            
            if not found_list:
                out.write("\nNo lists found in the root dictionary. Dumping full root dict (truncated):\n")
                out.write(json.dumps(data, indent=4)[:1000])

    print(f"Done! Please open '{OUTPUT_FILE}' and paste the content back to the chat.")

if __name__ == "__main__":
    analyze_structure()