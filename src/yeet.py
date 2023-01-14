#!/usr/bin/python3
from argparse import ArgumentParser
from shutil import move
from os import getcwd, mkdir, path, chdir, system
from time import time
import datetime
import json
import shutil

# Constants
CWD = getcwd()
USER_DIR = path.expanduser("~")
YEET_DIR = f"{USER_DIR}/.yeet"
YEETED_JSON = f"{YEET_DIR}/yeeted.json"
YEET_EXPIRY_SECONDS = 60 * 60 * 24 * 7 # 7 days
CURRENT_TIME = time()
PARSER_OPTIONS = [
    {
        "short": "r",
        "long": "restore",
        "help": "Restore a file from the yeet bin",
        "action": "store_true"
    },
    {
        "short": "l",
        "long": "list",
        "help": "List all yeeted files",
        "action": "store_true"
    },
    {
        "short": "e",
        "long": "empty",
        "help": "Empty the yeet bin",
        "action": "store_true"
    },
    {
        "short": "y",
        "long": "yes",
        "help": "Automatically confirm all prompts",
        "action": "store_true"
    },
    {
        "short": "v",
        "long": "version",
        "help": "Print the version and exit",
        "action": "version"
    },
    {
        "short": "U",
        "long": "uninstall",
        "help": "Uninstall yeet",
        "action": "store_true",
    },
    {
        "short": "u",
        "long": "update",
        "help": "Update yeet",
        "action": "store_true"
    }
]

PARSER_DETAILS = {
    "description": "Yeet files to the _yeet bin and restore them later.",
    "epilog": "GitHub: https://github.com/sby051/yeet",
    "version": "1.0.0",
    "usage": "yeet {options} [file]",
    "prog": "yeet",
}

def _init_yeet() -> None:
    if not path.exists(YEET_DIR):
        mkdir(YEET_DIR)
    
    if not path.exists(YEETED_JSON):
        with open(YEETED_JSON, "w") as f:
            f.write("{}")
            
def _get_parser() -> ArgumentParser:
    parser = ArgumentParser()
    
    for detail in PARSER_DETAILS:
        parser.__setattr__(detail, PARSER_DETAILS[detail])
    
    parser.add_argument("file", help="The file to _yeet or _restore", nargs="?")
    
    for option in PARSER_OPTIONS:
        parser.add_argument(
            f"-{option['short']}",
            f"--{option['long']}",
            help=option["help"],
            action=option["action"]
        )

    return parser
            
def _yeet(file: str) -> None:
    absolute_path = f"{CWD}/{file}"
    
    if not path.exists(absolute_path):
        print(f"File {absolute_path} does not exist, and is therefore unyeetable.")
        return
    
    if path.exists(f"{YEET_DIR}/{file}"):
        print(f"File {file} has already been yeeted.")
        return
    
    # Move the file to the _yeet directory
    move(absolute_path, YEET_DIR)
    
    # Add the file to the _yeet.json file
    with open(YEETED_JSON, "r") as f:
        yeeted_json = json.load(f)
        
    yeeted_json[file] = {
        "path": absolute_path,
        "expires": CURRENT_TIME + YEET_EXPIRY_SECONDS,
    }
    
    with open(YEETED_JSON, "w") as f:
        json.dump(yeeted_json, f)
    
    print(f"Yeeted {file} to {YEET_DIR}")
    
def _restore(file: str) -> None:
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
    
def _update_yeet() -> None:
    # pull latest binary from github and replace the current one
    system("curl -s https://raw.githubusercontent.com/sby051/yeet/main/bin/yeet > /opt/yeet/bin/yeet")
    print("Yeet has been updated.")
    
def _time_to_date(timestamp: float) -> str:
    x = datetime.datetime(1970, 1, 1) + datetime.timedelta(seconds=timestamp)
    return x.strftime("%d/%m/%Y at %H:%M:%S")

def _uninstall_yeet() -> None:
    shutil.rmtree(YEET_DIR)
    shutil.rmtree("/opt/yeet")
    with open(f"{USER_DIR}/.bashrc", "r") as f:
        bashrc = f.read()
        # remove the path from the bashrc
        bashrc = bashrc.replace("export PATH=$PATH:/opt/yeet/bin", "")
        
    with open(f"{USER_DIR}/.bashrc", "w") as f:
        f.write(bashrc)
        
    with open(f"{USER_DIR}/.zshrc", "r") as f:
        zshrc = f.read()
        # remove the path from the zshrc
        zshrc = zshrc.replace("export PATH=$PATH:/opt/yeet/bin", "")
        
    with open(f"{USER_DIR}/.zshrc", "w") as f:
        f.write(zshrc)
        
    with open(f"{USER_DIR}/.config/fish/config.fish", "r") as f:
        fishrc = f.read()
        fishrc = fishrc.replace("set PATH $PATH /opt/yeet/bin", "")
        
    with open(f"{USER_DIR}/.config/fish/config.fish", "w") as f:
        f.write(fishrc)
        
    print("Yeet uninstalled successfully.")

def _list_yeeted() -> None:
    
    with open(f"{YEETED_JSON}", "r") as f:
        yeet_json = json.load(f)
        
    if not yeet_json:
        print("No yeeted files (yet). Try yeeting some files!")
        return
    
    print("Yeeted files:")
    for file in yeet_json:
        print(f"""{file}:
  Expiry: {_time_to_date(yeet_json[file]['expires'])}
  Original Path: {yeet_json[file]['path']}
    """)
    
def _confirm(prompt: str, callback: callable) -> None:
    print(prompt)
    response = input("y/n: ")
    
    if response == "y":
        callback()
    else:
        print("Aborted.")
        return
    
def _empty() -> None:
    shutil.rmtree(YEET_DIR)
    _init_yeet()
    print("Yeet bin emptied.")
    
def _check_expiry() -> None:
    with open(YEETED_JSON, "r") as f:
        yeet_json = json.load(f)
        
    new_yeet_json = {}
        
    for file in yeet_json:
        if CURRENT_TIME >= yeet_json[file]["expires"]:
            system(f"rm -rf {YEET_DIR}/{file}")
            print(f"[!] File '{file}' has expired and has been deleted.")
        else:
            new_yeet_json[file] = yeet_json[file]
            
            
    with open(YEETED_JSON, "w") as f:
        json.dump(new_yeet_json, f)

def main():
    parser = _get_parser()
    _init_yeet()
    _check_expiry()
    
    args = parser.parse_args()
        
    if args.restore:
        if not args.file:
            print("Please specify a file to restore.")
            return
        
        if args.yes:
            _restore(args.file)
        else:
            _confirm(f"Are you sure you want to restore {args.file}?", lambda: _restore(args.file))
        
    if args.list:
        _list_yeeted()
        
    if args.empty:
        if args.yes:
            _empty()
        else:
            _confirm("Are you sure you want to empty the yeet bin?", _empty)
            
    if args.uninstall:
        _confirm("Are you sure you want to uninstall yeet?", _uninstall_yeet)
        
    if args.update:
        _update_yeet()

    if not args.restore and not args.list and not args.empty:
        if not args.file:
            print("Please specify a file to yeet.")
            return
        _yeet(args.file)
    
if __name__ == '__main__':
    main()
