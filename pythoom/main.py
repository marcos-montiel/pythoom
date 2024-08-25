import sys

import globals
from d_main import d_doom_main


def main() -> None:
    globals.my_argc = len(sys.argv)
    globals.my_argv = sys.argv

    d_doom_main()


if __name__ == "__main__":
    main()
