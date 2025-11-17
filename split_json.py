import json
import math
import os

# --- CONFIGURATION ---

# 1. The name of your giant 58MB file
SOURCE_FILE = "LiveData.json"

# 2. *** THIS IS THE FIX ***
#    Based on your data, the key holding the list is "data"
SNAPSHOT_ARRAY_KEY = "data" 

# 3. The prefix for your new split files
OUTPUT_PREFIX = "live_part"

# 4. How many files you want to create
NUM_FILES = 20

# --- END CONFIGURATION ---

def split_file():
    if not os.path.exists(SOURCE_FILE):
        print(f"Error: Cannot find file '{SOURCE_FILE}'.")
        return

    print(f"Reading and parsing {SOURCE_FILE}...")
    print("(This may take a minute for a 58MB file)")
    
    try:
        with open(SOURCE_FILE, 'r', encoding='utf-8') as f:
            data = json.load(f)
    except json.JSONDecodeError as e:
        print(f"Error: The file is not valid JSON. {e}")
        return
    except Exception as e:
        print(f"An error occurred reading the file: {e}")
        return

    all_objects = []
    if SNAPSHOT_ARRAY_KEY == "":
        # Case 1: The *entire file* is one big array: [{"t":...}, ...]
        if isinstance(data, list):
            all_objects = data
        else:
            print(f"Error: SNAPSHOT_ARRAY_KEY is empty, but the file is not a list (it's a {type(data)}).")
            return
    else:
        # Case 2: The snapshots are in a key: {"data": [...]}
        if SNAPSHOT_ARRAY_KEY in data:
            if isinstance(data[SNAPSHOT_ARRAY_KEY], list):
                all_objects = data[SNAPSHOT_ARRAY_KEY] # This will get the list from "data"
            else:
                print(f"Error: The key '{SNAPSHOT_ARRAY_KEY}' does not contain a list (it's a {type(data[SNAPSHOT_ARRAY_KEY])}).")
                return
        else:
            print(f"Error: Could not find key '{SNAPSHOT_ARRAY_KEY}' in the JSON file.")
            print(f"Found these keys instead: {list(data.keys())}")
            return

    total_objects = len(all_objects)
    if total_objects == 0:
        print("Error: No snapshot objects were found in the array.")
        return

    print(f"Success! Found {total_objects} total snapshot objects inside the '{SNAPSHOT_ARRAY_KEY}' list.")
    
    objects_per_file = math.ceil(total_objects / NUM_FILES)
    print(f"Splitting into {NUM_FILES} files with ~{objects_per_file} objects each.")

    file_counter = 0
    for i in range(0, total_objects, objects_per_file):
        file_counter += 1
        
        chunk_objects = all_objects[i : i + objects_per_file]
        
        # Convert each Python dict *back into a JSON string*
        string_chunks = [json.dumps(obj) for obj in chunk_objects]
        
        # Join them with commas.
        chunk_content = ",".join(string_chunks)
        
        output_filename = f'{OUTPUT_PREFIX}_{file_counter}.json'
        
        print(f"Writing {len(chunk_objects)} objects to {output_filename}...")
        with open(output_filename, 'w', encoding='utf-8') as out_f:
            out_f.write(chunk_content)

    print("-" * 20)
    print(f"Success! Created {file_counter} split files.")

# Run the script
if __name__ == "__main__":
    split_file()