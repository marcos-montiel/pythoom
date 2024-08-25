import os
import sys
import globals

from i_system import i_error
from doomdef import GameMode, Languages
from m_argv import m_check_parm
from d_strings import DEVDATA, DEVMAPS


MAX_WAD_FILES: int = 20


def d_doom_main() -> None:
    find_response_file()

    identify_version()


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


def identify_version() -> None:
    doom_wad_dir = os.getenv("DOOMWADDIR")
    if not doom_wad_dir:
        doom_wad_dir = "."
    doom2_wad = f"{doom_wad_dir}/doom2.wad"
    doomu_wad = f"{doom_wad_dir}/doomu.wad"
    doom_wad = f"{doom_wad_dir}/doom.wad"
    doom1_wad = f"{doom_wad_dir}/domm1.wad"
    plutonia_wad = f"{doom_wad_dir}/plutonia.wad"
    tnt_wad = f"{doom_wad_dir}/tnt.wad"
    doom2f_wad = f"{doom_wad_dir}/doom2f.wad"

    home = os.getenv("HOME")
    if not home:
        i_error("Please set $HOME to your home directory")
    globals.base_default = f"{home}/.doomrc"

    if m_check_parm("-shdev"):
        globals.game_mode = GameMode.Shareware
        globals.dev_parm = True
        d_add_file(DEVDATA + "/doom1.wad")
        d_add_file(DEVMAPS + "/data_se/texture1.lmp")
        d_add_file(DEVMAPS + "/data_se/pnames.lmp")
        globals.base_default = DEVDATA + "/default.cfg"
        return None

    if m_check_parm("-regdev"):
        globals.game_mode = GameMode.Registered
        globals.dev_parm = True
        d_add_file(DEVDATA + "/doom.wad")
        d_add_file(DEVMAPS + "/data_se/texture1.lmp")
        d_add_file(DEVMAPS + "/data_se/texture2.lmp")
        d_add_file(DEVMAPS + "/data_se/pnames.lmp")
        globals.base_default = DEVDATA + "/default.cfg"
        return None

    if m_check_parm("-comdev"):
        globals.game_mode = GameMode.Commercial
        globals.dev_parm = True
        d_add_file(DEVDATA + "/doom2.wad")
        d_add_file(DEVMAPS + "/cdata/texture1.lmp")
        d_add_file(DEVMAPS + "/cdata/pnames.lmp")
        globals.base_default = DEVDATA + "/default.cfg"
        return None

    if os.access(doom2f_wad, os.R_OK):
        globals.game_mode = GameMode.Commercial
        globals.language = Languages.French
        print("French version")
        d_add_file(doom2f_wad)
        return None

    if os.access(doom2_wad, os.R_OK):
        globals.game_mode = GameMode.Commercial
        d_add_file(doom2_wad)
        return None

    if os.access(plutonia_wad, os.R_OK):
        globals.game_mode = GameMode.Commercial
        d_add_file(plutonia_wad)
        return None

    if os.access(tnt_wad, os.R_OK):
        globals.game_mode = GameMode.Commercial
        d_add_file(tnt_wad)
        return None

    if os.access(doomu_wad, os.R_OK):
        globals.game_mode = GameMode.Retail
        d_add_file(doomu_wad)
        return None

    if os.access(doom_wad, os.R_OK):
        globals.game_mode = GameMode.Registered
        d_add_file(doom_wad)
        return None
    if os.access(doom1_wad, os.R_OK):
        globals.game_mode = GameMode.Shareware
        d_add_file(doom1_wad)
        return None

    print("Game mode indeterminate")
    globals.game_mode = GameMode.Indetermined


def d_add_file(file: str) -> None:
    if len(globals.wad_files) > MAX_WAD_FILES:
        i_error("Maximun number of wad files reached.")
    globals.wad_files.append(file)
