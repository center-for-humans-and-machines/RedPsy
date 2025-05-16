# Red-teaming with Psychiatrists: A Multi-turn Conversation Dataset for Evaluating Conversational Agents

## Requirements

- Python 3.13 or later
- [`pre-commit`](https://pre-commit.com/) - linter orchestration

  ```sh
  brew install pre-commit
  ```

- [`pylint`](https://pylint.readthedocs.io/en/stable/) - local linter

  ```sh
  brew install pylint
  ```

- [`poetry`](https://python-poetry.org/) - package manager

  ```sh
  pipx install poetry==2.1.2
  ```

- Follow [data.qmd](./docs/data.qmd) to download the datasets

## Installation

- Install Python dependencies

  ```sh
  ./script/bootstrap
  ```

- Install Python package

  ```sh
  ./script/install
  ```

## Usage

Review [notebooks](notebooks) for data exploration. The workflow is to first try out methods in the notebooks and then move them to the [Python package](./redpsy/) for improved code reusability.

A demo of the Python package is found in [python-scripts-demo.ipynb](./notebooks/python-scripts-demo.ipynb).

### Scripts

#### Linting

- Lint the code locally

  ```sh
  ./script/lint
  ```

#### Testing

- Show help message for the test script

  ```sh
  ./script/test -h
  ```

- Run tests using `pytest` (except for regression tests)

  ```sh
  ./script/test
  ```

- Run regression tests using `pytest`

  ```sh
  ./script/test -r
  ```

## Notebooks

1. generate-dataset-2.ipynb
1. llm-rater.ipynb
1. read-batch-ratings.ipynb
1. merge_datasets.ipynb

## Docs

The documentation is built using [Quarto](https://quarto.org) and [`pdoc`](https://pdoc.dev/). The former is used for general documentation and the latter for API documentation.

- View documentation [locally](https://quarto.org/docs/websites):

  ```sh
  ./script/docs-general
  ```

- View API documentation:

  ```sh
  ./script/docs-api
  ```

The documentation is only available locally to avoid exposing sensitive information if [published](https://github.com/quarto-dev/quarto-actions/blob/main/examples/example-01-basics.md) to GitHub Pages.

## Contributing

Please read [contributing.md](contributing.md) for details on the guidelines for this project.

## Credits

- Scripts follow [rodrigobdz/styleguide-sh](https://github.com/rodrigobdz/styleguide-sh)
- Linter configuration files imported from [rodrigobdz/linters](https://github.com/rodrigobdz/linters)
- Readme is based on [rodrigobdz/minimal-readme](https://github.com/rodrigobdz/minimal-readme)

## License

[CC-BY-4.0](license)
