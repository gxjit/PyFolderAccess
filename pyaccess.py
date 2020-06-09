# Copyright (c) 2020 Gurjit Singh

# This source code is licensed under the MIT license that can be found in
# the accompanying LICENSE file or at https://opensource.org/licenses/MIT.


import argparse
import json
import os
import os.path as path
import pathlib
import subprocess
import sys


def parseArgs():
    def dirPath(pth):
        pthObj = pathlib.Path(pth)
        if pthObj.is_dir():
            return pthObj
        else:
            raise argparse.ArgumentTypeError("Invalid Directory path")

    parser = argparse.ArgumentParser(
        description="Allow/Deny access to specified directory using icacls.exe"
    )
    dirSelect = parser.add_mutually_exclusive_group(required=True)
    dirSelect.add_argument("-d", "--dir", help="Directory path", type=dirPath)
    dirSelect.add_argument(
        "-l", "--list", action="store_true", help="list remembered paths",
    )
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("-a", "--allow", action="store_true", help="Allow access")
    group.add_argument(
        "-y", "--deny", action="store_true", help="Deny access",
    )
    store = parser.add_mutually_exclusive_group(required=False)
    store.add_argument("-r", "--remember", action="store_true", help="remember path")
    store.add_argument("-f", "--forget", action="store_true", help="forget path")
    pargs = parser.parse_args()

    return pargs


def makeTargetDirs(dirPath):
    if not dirPath.exists():
        os.mkdir(dirPath)


def getConfigFile():
    configPath = pathlib.Path(path.join(path.expanduser("~"), ".config"))
    makeTargetDirs(configPath)
    configFile = configPath.joinpath("remembered")
    return configFile


def listFiles(cnf):
    if not cnf:
        print("\nNo remembered directories")
        sys.exit()

    for i, e in enumerate(cnf):
        print(f"\n{i} -> {e}")

    allow = int(input("\nSpecify index of directory to be processed\n\n> "))
    return cnf[allow]


def main(pargs):

    configFile = getConfigFile()

    if configFile.exists():
        with open(configFile, "r", encoding="utf-8") as f:
            config = json.loads(f.read())
    else:
        config = []

    if pargs.list:
        dirPath = pathlib.Path(listFiles(config))
    else:
        dirPath = pargs.dir.resolve()

    cmdIcacls = lambda cmd: ["icacls", str(dirPath), *cmd, "/c", "/l", "/q"]
    cmdAttrib = lambda cmd: ["attrib", *cmd, str(dirPath), "/D", "/l"]
    # cmdOwn = ["takeown", "/f", str(dirPath), "/r", "/d", "Y"]

    if pargs.deny:
        # subprocess.run(cmdOwn)
        subprocess.run(cmdAttrib(["-r", "-i", "+s", "+h"]))
        subprocess.run(cmdIcacls(["/deny", "EVERYONE:F"]))
        # print(cmdAttrib(["-r", "+s", "+h", "-i"]))
        # print(cmdIcacls(["/deny", "EVERYONE:F"]))

    else:
        subprocess.run(cmdIcacls(["/reset"]))
        # subprocess.run(cmdOwn)
        subprocess.run(cmdAttrib(["-s", "-h"]))
        # print(cmdIcacls(["/reset"]))

    if pargs.remember or pargs.forget:
        if str(dirPath) not in config and pargs.remember:
            config.append(str(dirPath))
        elif str(dirPath) in config and pargs.forget:
            config.remove(str(dirPath))
        with open(configFile, "w", encoding="utf-8") as f:
            json.dump(config, f)


main(parseArgs())

# TODO: force allow using takeown
