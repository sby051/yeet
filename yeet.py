#!/usr/bin/python3.11
from argparse import ArgumentParser
import shutil
import json

def main():
    parser = ArgumentParser()
    parser.description = "A rubbish bin for Linux"
    parser.epilog = "GitHub: https://github.com/sby051/yeet"
    parser.version = "0.1"
    parser.prog = "yeet"
    parser.usage = "yeet [options] {path/to/file}"

    options = [
        {
            "short": "-r",
            "long": "--restore",
            "help": "Restores a yeeted file to it's original location"
        },
        {
            "short": "-l",
            "long": "--list",
            "help": "Lists all yeeted files"
        },
        {
            "short": "-e",
            "long": "--empty",
            "help": "Empties the yeet bin (located at ~/.yeet)"
        },
    ]
    
    for option in options:
        parser.add_argument(option["short"], option["long"], help=option["help"])
        
    parser.add_argument("path", help="The file path to yeet, restore etc.")
        
    args = parser.parse_args()
    
    
    
    

if __name__ == '__main__':
    main()