""" __main__.py
You can start the script from the repo root by issuing `python src <devicename>`
"""

from sys import argv

script, cmd = argv

if cmd == 'releaser':
    import releaser
elif cmd == 'scanner':
    import scanner
