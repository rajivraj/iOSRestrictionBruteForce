from __future__ import print_function
from time import time
from base64 import b64decode
from passlib.utils.pbkdf2 import pbkdf2

from ioscrack.database import addKey, keyExists

COMMON_KEYS = [
    1234, 1111, 0000, 1212, 7777, 1004, 2000, 4444, 2222, 6969, 9999, 3333,
    5555, 6666, 1122, 1313, 8888, 4321, 2001, 1010, 2580
]


def check(secret64, salt64, key):
    try:
        secret = b64decode(secret64)
        salt = b64decode(salt64)
    except TypeError as e:
        print(str(e))
        exit(1)
    out = pbkdf2(key, salt, 1000)
    status = (out == secret)
    if status:
        addKey(secret64, salt64, key)
    return status


def print_try(key):
    print("Trying: %s \r" % key, end=""),


def print_key(key, message=None, start_t=None):
    if start_t:
        str_duration = "it took %s secconds" % round(time() - start_t, 2)
    else:
        str_duration = ""
    if message:
        print("Passcode is %s (%s) %s\n" % (key, message, str_duration))
    else:
        print("Passcode is %s %s\n" % (key, str_duration))


def crack(secret64, salt64):
    secret64 = secret64.strip()
    salt64 = salt64.strip()
    inDB = keyExists(secret64, salt64)
    if inDB:
        key = inDB[0]
        print_key(key, message="in database")
        return key
    start_t = time()
    # Top 20 common pins
    key = tryPinInRange(secret64, salt64, start_t, list=COMMON_KEYS,
                        message="common year", start=1900, stop=2018)
    if key:
        return key
    # Common birth dates
    key = tryPinInRange(secret64, salt64, start_t,
                        message="common year", start=1900, stop=2018)
    if key:
        return key

    # Brute force all pins
    key = tryPinInRange(secret64, salt64, start_t,
                        message="brute force", stop=10000)
    if key:
        return key
    print("Invalid Key and/or Salt")


def tryPinInRange(secret64, salt64, start_t, message=None, list=None, start=None, stop=0):
    if start and stop:
        rangeArgs = (start, stop)
    elif stop:
        rangeArgs = (stop, )

    if list:
        for i in list:
            key = tryAndCheck(i, secret64, salt64,
                              start_t=start_t, message=message)
            if key:
                return key
    else:
        for i in range(*rangeArgs):
            key = tryAndCheck(i, secret64, salt64,
                              start_t=start_t, message=message)
            if key:
                return key


def tryAndCheck(i, secret64, salt64, start_t=None, message=None):
    key = "%04d" % (i)
    print_try(key)
    if check(secret64, salt64, key):
        print_key(key, message=message, start_t=start_t)
        return key


def crackHashes(devices):
    for device in devices:
        print("\nUDID: %s \n%s: %s running iOS %s" %
              (device.UDID, device.targetType, device.model, device.iOS))
        print("Cracking restrictions passcode for %s..." % device.name)
        device.crack()
