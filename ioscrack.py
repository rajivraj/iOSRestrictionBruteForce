#!/usr/bin/env python3
from builtins import input

from ioscrack.paths import backupPaths
from ioscrack.parse import argparse, findHashes
from ioscrack.cli import prompt
from ioscrack.crack import crackHashes


def main():
    parser = argparse()
    args = parser.parse_args()
    BACKUP_PATHS = backupPaths()
    try:
        print("\n iOSRestrictionBruteForce")
        print(" Written by thehappydinoa \n")
        if args.automatically and not args.cli:
            crackHashes(findHashes(BACKUP_PATHS))
        if args.cli:
            prompt()
        if args.backup:
            crackHashes(findHashes(args.backup))
        if not any(vars(args)[key] for key in vars(args).keys()):
            parser.print_help()
        input("Press [enter] to exit")
    except KeyboardInterrupt:
        print("Exiting...\r"),
        exit(0)


if __name__ == "__main__":
    main()
