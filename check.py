#!/usr/bin/env python

#minified version of Michael Pound's script

import hashlib
import sys

try:
    import requests
except ModuleNotFoundError:
    print("###  pip install requests  ###")
    raise


def lookup(pwd):
    sha1pwd = hashlib.sha1(pwd.encode('utf-8')).hexdigest().upper()
    head, tail = sha1pwd[:5], sha1pwd[5:]
    url = 'https://api.pwnedpasswords.com/range/' + head
    res = requests.get(url)
    if res.status_code != 200:
        raise RuntimeError('Error fetching "{}": {}'.format(
            url, res.status_code))
    hashes = (line.split(':') for line in res.text.splitlines())
    count = next((int(count) for t, count in hashes if t == tail), 0)
    return count


def main(args):
    ec = 0
    for pwd in args:
        pwd = pwd.strip()
        try:
            count = lookup(pwd)
            if count:
                foundmsg = "{0} was found with {1} occurrences"
                print(foundmsg.format(pwd, count))
                ec = 1
            else:
                print("{} was not found".format(pwd))
        except UnicodeError:
            errormsg = sys.exc_info()[1]
            print("{0} could not be checked: {1}".format(pwd, errormsg))
            ec = 1
            continue
    return ec


if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))

