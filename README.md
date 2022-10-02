# wordlesolver
## Installation
- Ensure conda is installed ([miniforge](https://github.com/conda-forge/miniforge) is recommended)
- Clone the repo: `git clone https://github.com/mdatoo/wordlesolver.git`
- Create conda environment: `conda env create -f environment.yml`
- Initialise playwright: `playwright install`

## Development tools
- If using vscode, open workspace `.vscode/wordlesolver.code-workspace` as a file
- Initialise pre-commit: `pre-commit install --hook-type commit-msg`

## Running
- Run project: 
- Run tests: `python -m unittest discover -s tests/ -p "*_test.py"`
