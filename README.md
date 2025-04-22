This generates a list of 'inactive' repositories in the Flathub GitHub
organisation which are then excluded from the global
external-data-checker action.

A repository is considered 'inactive' if the default branch has no
commits and there are more than a specified number of open pull requests
by the 'flathubbot' user in a certain period of time. The list is
updated once a week.
