import argparse
import os

from universal_build import build_utils

HERE = os.path.abspath(os.path.dirname(__file__))
os.chdir(HERE)

if __name__ == "__main__":

    # Custom CLI arguments
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--deployment-token", help="This is a custom token.", default=""
    )
    parser.add_argument("--my_token", help="This is a custom token.", default="")
    parser.add_argument("--my_bool", help="This is a custom bool.", action="store_true")

    args = build_utils.parse_arguments(argument_parser=parser)

    build_utils.build("submodule", args)
