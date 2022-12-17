# wordlesolver
## Installation
- Ensure [taskfile](https://taskfile.dev/installation/) is installed
- Ensure conda is installed ([miniforge](https://python-poetry.org/docs/#installation) is recommended)
- Clone the repo: `git clone https://github.com/mdatoo/wordlesolver.git`
- Build project: `task build`

## Development tools
- If using vscode, open workspace `.vscode/wordlesolver.code-workspace` as a file
- Run tests: `task test`
- Run pre-commit `task lint`

## Running
- Run project: `task run -- {generator} {solver}`
  > e.g. task run -- FakeGenerator MaximiseMatchesSolver
- Train solver: `task train -- {solver}`
  > e.g. task train -- PPOSolver
