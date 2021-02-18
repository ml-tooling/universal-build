import argparse

from universal_build import build_utils

if __name__ == "__main__":

    # Custom CLI arguments
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--deployment-token", help="This is a custom token.", default=""
    )
    parser.add_argument("--my_token", help="This is a custom token.")
    parser.add_argument("--my_bool", help="This is a custom bool.", action="store_true")

    args = build_utils.parse_arguments(argument_parser=parser)

    if not args.get("deployment_token"):
        build_utils.exit_process(1)

    if not args.get("my_token"):
        build_utils.exit_process(1)

    if not args.get("my_bool"):
        build_utils.exit_process(1)
