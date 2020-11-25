# Documentation

This documentation is based on [mkdocs](https://www.mkdocs.org/) and the [mkdocs-material](http://squidfunk.github.io/mkdocs-material/specimen) theme. It also makes use of [pymdown markdown extensions](https://facelessuser.github.io/pymdown-extensions/). You can find all activated extensions and configurations in the [mkdocs.yml](./mkdocs.yml) file. For basic help on the markdown syntax, refer to [this awesome cheatsheet](https://github.com/adam-p/markdown-here/wiki/Markdown-Cheatsheet).

## Update documentation

If you want to make changes to the documentation, just clone the repository, implement your changes, test the documentation as explained in the following sections, and push your changes back to the repository as explained in our [contribution guidelines](../CONTRIBUTING.md#contributing-to-the-code-base).

### Development requirements

- Python, pip + dependencies:

```bash
pip install mkdocs mkdocs-material pygments pymdown-extensions markdown-include
```

### Test changes locally

Execute this command in the documentation folder to build and run the documentation locally:

```bash
python build.py --make --run
```

This command will start a development server for the documentation on [http://localhost:8001](http://localhost:8001) which will automatically reload on changes.

### Release changes on Github Pages

The recommended way to release the documentation is by executing the release for all components as explained in our [contribution documentation](../CONTRIBUTING.md#development-instructions). In case you only want to deploy documentation changes to Github Pages without upgrading the project version, execute:

```bash
python build.py --make --check --release --version=<MAJOR.MINOR.PATCH>
```
