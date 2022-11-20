# wordlesolver
## Installation
- Ensure [taskfile](https://taskfile.dev/installation/) is installed
- Ensure [poetry](https://python-poetry.org/docs/#installation) is installed
- Clone the repo: `git clone https://github.com/mdatoo/wordlesolver.git`
- Build project: `task build`

## Development tools
- If using vscode, open workspace `.vscode/wordlesolver.code-workspace` as a file
- Run tests: `task test`
- Run pre-commit `task lint`

## Running
- Run project: `task run -- {generator} {solver}`
  > e.g. task run -- fake_generator.py maximise_matches_solver.py
- Train solver: `task train -- {solver}`
  > e.g. task train -- dqn_solver.py
