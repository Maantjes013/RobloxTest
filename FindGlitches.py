import json
import os
import math

# --- CONFIGURATION ---
FILENAME = "LiveData.json"
# ---------------------

def ms_to_min_sec(ms):
    seconds = (ms // 1000) % 60
    minutes = (ms // (1000 * 60))
    return f"{minutes:02}:{seconds:02}"

def analyze_integrity():
    if not os.path.exists(FILENAME):
        print(f"Error: Could not find file '{FILENAME}'")
        return

    print(f"Reading {FILENAME}...")
    try:
        with open(FILENAME, 'r', encoding='utf-8') as f:
            raw_data = json.load(f)
    except Exception as e:
        print(f"Error parsing JSON: {e}")
        return

    frames = raw_data if isinstance(raw_data, list) else raw_data.get('data', [])
    
    print("-" * 80)
    print(f"{'TIME':<8} | {'PID':<6} | {'ERROR TYPE':<15} | {'DETAILS'}")
    print("-" * 80)

    last_positions = {}
    error_count = 0

    for frame in frames:
        t = frame.get('t', 0)
        timestamp = ms_to_min_sec(t)
        
        # Check Home and Away lists
        players = frame.get('h', []) + frame.get('a', [])

        for p in players:
            pid = p.get('p')
            
            # 1. CHECK MISSING ID
            if pid is None:
                print(f"{timestamp:<8} | N/A    | MISSING ID      | Player entry has no 'p' field")
                error_count += 1
                continue

            x = p.get('x')
            y = p.get('y')

            # 2. CHECK MISSING COORDS (None/Null)
            if x is None or y is None:
                print(f"{timestamp:<8} | {pid:<6} | NULL DATA       | x: {x}, y: {y}")
                error_count += 1
                continue

            # 3. CHECK INVALID NUMBERS (NaN / Inf)
            # JSON usually handles NaN as null, but if it's a string "NaN" or extreme float
            if not isinstance(x, (int, float)) or not isinstance(y, (int, float)):
                 print(f"{timestamp:<8} | {pid:<6} | TYPE ERROR      | x: {type(x)}, y: {type(y)}")
                 error_count += 1
                 continue
            
            if math.isnan(x) or math.isinf(x) or math.isnan(y) or math.isinf(y):
                print(f"{timestamp:<8} | {pid:<6} | MATH ERROR      | x: {x}, y: {y} (NaN/Inf)")
                error_count += 1
                continue

            # 4. CHECK ZERO SNAP (The "Teleport to Origin" Bug)
            # It is extremely rare for a player to be at exactly 0.000000, 0.000000
            if x == 0.0 and y == 0.0:
                # Only flag if they weren't near zero previously
                if pid in last_positions:
                    lx, ly = last_positions[pid]
                    dist = math.sqrt((x - lx)**2 + (y - ly)**2)
                    if dist > 5.0: # If they jumped >5 meters to hit exactly 0,0
                        print(f"{timestamp:<8} | {pid:<6} | ZERO SNAP       | Jumped {dist:.2f}m to (0,0)")
                        error_count += 1

            last_positions[pid] = (x, y)

    print("-" * 80)
    print(f"Scan complete. Found {error_count} data integrity issues.")

if __name__ == "__main__":
    analyze_integrity()