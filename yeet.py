#!/usr/bin/python3
from argparse import ArgumentParser
from shutil import move
from os import getcwd, mkdir, path, chdir, system
from time import time
import json
import shutil

# Constants
CWD = getcwd()
USER_DIR = path.expanduser("~")
YEET_DIR = f"{USER_DIR}/.yeet"
YEETED_JSON = f"{YEET_DIR}/yeeted.json"
YEET_EXPIRY_SECONDS = 60 * 60 * 24 * 7 # 7 days 
CURRENT_TIME = time()

def init_yeet() -> None: # Creates the yeet directory and yeet.json file if they don't exist
    if not path.exists(YEET_DIR):
        mkdir(YEET_DIR)
    
    if not path.exists(YEETED_JSON):
        with open(YEETED_JSON, "w") as f:
            f.write("{}")
            
# Moves a file to the yeet directory and logs its name as the key and its original location as the value
def yeet(file: str) -> None:
    absolute_path = f"{CWD}/{file}"
    
    if not path.exists(absolute_path):
        print(f"File {absolute_path} does not exist, and is therefore unyeetable.")
        return
    
    if path.exists(f"{YEET_DIR}/{file}"):
        print(f"File {file} has already been yeeted.")
        return
    
    # Move the file to the yeet directory
    move(absolute_path, YEET_DIR)
    
    # Add the file to the yeet.json file
    with open(YEETED_JSON, "r") as f:
        yeeted_json = json.load(f)
        
    yeeted_json[file] = {
        "path": absolute_path,
        "expires": CURRENT_TIME + YEET_EXPIRY_SECONDS,
    }
    
    with open(YEETED_JSON, "w") as f:
        json.dump(yeeted_json, f)
    
    print(f"Yeeted {file} to {YEET_DIR}")
    
# Restores a file from the yeet directory to its original location
def restore(file: str) -> None:
    with open(YEETED_JSON, "r") as f:
        yeet_json = json.load(f)
        
    if file not in yeet_json:
        print(f"File {file} has not been yeeted.")
        return
    
    original_location = yeet_json[file]["path"]
    
    if path.exists(original_location):
        print(f"File {file} already exists in its original location.")
        return
    
    move(f"{YEET_DIR}/{file}", original_location)
    
    del yeet_json[file]
    
    with open(YEETED_JSON, "w") as f:
        json.dump(yeet_json, f)
    
    print(f"Restored {file} to {original_location}")

def list_yeeted() -> None:
    print("Yeeted files:")
    
    with open(f"{YEET_DIR}/yeet.json", "r") as f:
        yeet_json = json.load(f)
        
    for file in yeet_json:
        print(f"{file} -> {yeet_json[file]}")
    else:
        print("No yeeted files.")
    
def confirm(prompt: str, callback: callable) -> None:
    print(prompt)
    response = input("y/n: ")
    
    if response == "y":
        callback()
    else:
        print("Aborted.")
        return
    
def empty() -> None:
    shutil.rmtree(YEET_DIR)
    init_yeet()
    print("Yeet bin emptied.")

def main():
    parser = ArgumentParser()
    parser.description = "A rubbish bin for Linux"
    parser.epilog = "GitHub: https://github.com/sby051/yeet"
    parser.version = "0.1"
    parser.prog = "yeet"
    parser.usage = "yeet [options] {restore | list | empty} [file]"
    
    init_yeet()    

    parser.add_argument("action", help="The action to perform", action="store", nargs="?", default="yeet", choices=["yeet", "restore", "list", "empty"])
    parser.add_argument("file", help="The file to yeet or restore", nargs="?")
    parser.add_argument("-f", "--force", help="Force the action", action="store_true")
    parser.add_argument("-v", "--version", help="Print the version and exit", action="version")   
    
    args = parser.parse_args()
    
    # if no action is specified, yeet the file
    if args.action == "restore":
        restore(args.file)
    elif args.action == "list":
        list_yeeted()
    elif args.action == "empty":
        if args.force:
            empty()
        else:
            confirm("Are you sure you want to empty the yeet bin? This cannot be undone.", empty)
    else:
        yeet(args.file)
    
    
if __name__ == '__main__':
    main()
