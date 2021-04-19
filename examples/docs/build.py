import os

from universal_build import build_utils
from universal_build.helpers import build_mkdocs

HERE = os.path.abspath(os.path.dirname(__file__))


def main(args: dict) -> None:
    # set current path as working dir
    os.chdir(HERE)

    if args.get(build_utils.FLAG_MAKE):
        # Install pipenv dev requirements
        build_mkdocs.install_build_env(exit_on_error=True)
        # Build mkdocs documentation
        build_mkdocs.build_mkdocs(exit_on_error=True)

    if args.get(build_utils.FLAG_CHECK):
        # TODO: Markdown linting
        # build_mkdocs.lint_markdown(exit_on_error=False)
        pass

    if args.get(build_utils.FLAG_RELEASE):
        # TODO: Do not publish project-template
        # Deploy to Github pages
        # build_mkdocs.deploy_gh_pages(exit_on_error=True)
        # Lock pipenv requirements
        build_utils.run("pipenv lock", exit_on_error=False)

    if args.get(build_utils.FLAG_RUN):
        build_mkdocs.run_dev_mode(exit_on_error=True)


if __name__ == "__main__":
    args = build_utils.parse_arguments()
    main(args)
