# SomaFM Import

This is a simple SomaFM channel list import to use in several applications.



## Available Plugins
[**Radiola**](https://github.com/SokoloffA/radiola): A Mac simple systray stream player
* Generates a bookmark.opml to copy to your app config folder:
```bash
   python simport.py radiola
```

## Requirements
- Python 3.11+

## Development
* Create a python environment to avoid polute your system ( or docker env )
* Install poetry and pre-commit

  ```bash
     $ pip install -U poetry pre-commit
     ```

* Install the dependencies

  ```bash
     $ poetry install
     ```

* Run precommit setup

  ```bash
     $ pre-commit init
     ```

## References
* [Poetry](https://python-poetry.org/)
* [pyproject.toml](https://python-poetry.org/docs/pyproject/)
* [pre-commit](https://pre-commit.com/)
