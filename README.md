This script generates a list of 'inactive' repositories in the Flathub
GitHub organisation which are then excluded from the global
external-data-checker action.

A repository is considered 'inactive' if the default branch has no
commits and there are more than a specified number of open pull requests
by automated accounts, in a certain period of time. The list is updated
once a week. So if a repo has actual maintainer activity, for example,
new commits to the default branch or closing stale PRs, it will get
automatically removed from the list here and the global
external-data-checker action will run on it once again.

Please don't manually edit the generated lists. If they are manually
edited, it needs to be sorted with `LC_ALL=C sort -u`.

If a repo is to be excluded, it needs to be added to `exclude.txt`.

### Development

```sh
uv run ruff format
uv run ruff check --fix --exit-non-zero-on-fix
uv run mypy .
```
