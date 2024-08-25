import sys
import globals


def d_doom_main() -> None:
    find_response_file()


def find_response_file() -> None:
    my_argc = globals.my_argc
    my_argv = globals.my_argv

    for i in range(1, my_argc):
        if my_argv[i].startswith("@"):
            try:
                with open(my_argv[i][1:], "r") as handle:
                    file = handle.read()
            except FileNotFoundError:
                print("\nNo such response file!", file=sys.stderr)
                sys.exit(1)

            more_args = my_argv[i + 1 :]

            first_argv = my_argv[0]

            globals.my_argv = [first_argv]

            infile_args = file.split()
            globals.my_argv.extend(infile_args)

            globals.my_argv.extend(more_args)

            globals.my_argc = len(globals.my_argv)

            print(f"{globals.my_argc} command-line args:")
            for arg in globals.my_argv:
                print(arg)
            break
