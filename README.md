# wordlesolver
## Installation
- Ensure [taskfile](https://taskfile.dev/installation/) is installed
- Ensure [mamba](https://mamba.readthedocs.io/en/latest/installation.html) is installed
- Clone the repo: `git clone https://github.com/mdatoo/wordlesolver.git`
- Build project: `task build`

## Development tools
- If using vscode, open workspace `.vscode/wordlesolver.code-workspace` as a file
- Run tests: `task test`
- Run linting: `task lint`

## Running
- Run solver: `task run -- {generator} {solver}`
  > e.g. task run -- FakeGenerator MaximiseMatchesSolver
- Train solver: `task train -- {solver}`
  > e.g. task train -- PPOSolver
