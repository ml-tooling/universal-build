from universal_build import build_utils


def main(args: dict) -> None:
    """Execute all component builds."""
    # Build react webapp
    build_utils.build("react-webapp", args)
    # Build python lib
    build_utils.build("python-lib", args)

    if args.get(build_utils.FLAG_MAKE):
        # Duplicate api docs into the mkdocs documentation
        build_utils.duplicate_folder(
            "./python-lib/docs/", "./mkdocs-docs/docs/api-docs/"
        )

    # Build mkdocs documentation
    build_utils.build("mkdocs-docs", args)


if __name__ == "__main__":
    args = build_utils.parse_arguments()

    if args.get(build_utils.FLAG_RELEASE):
        # Run main without release to see whether everthing can be built and all tests run through
        # Run args without release to see whether everthing can be built and all tests run through
        args = dict(args)
        args[build_utils.FLAG_RELEASE] = False
        main(args)
        # Run main again without building and testing the components again
        args = {
            **args,
            build_utils.FLAG_MAKE: False,
            build_utils.FLAG_CHECK: False,
            build_utils.FLAG_TEST: False,
            build_utils.FLAG_RELEASE: True,
            build_utils.FLAG_FORCE: True,
        }
    main(args)
