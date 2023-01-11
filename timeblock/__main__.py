"""Allow database argument to be passed to main() from command line."""
import sys

from . import main

rc = 1
try:
    if len(sys.argv) > 1:
        main(sys.argv[1])
    else:
        main()
    rc = 0
except Exception as e:
    print(e)
sys.exit(rc)
