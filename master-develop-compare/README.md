# Readme

Tool to compare repository master and develop branches for changes using the github api in bulk.

Install via
```
pip3 install -U --user "git+https://github.com/Tethik/lame-cli-programs#egg=master-develop-compare&subdirectory=master-develop-compare"
```

## Usage
```
Usage: master-develop-compare.py [OPTIONS] MATCH_FILTER

  Compares develop and master branches for github repositories to detect
  where a new release is needed.

  MATCH_FILTER is a glob-like filter that decides which repositories should
  be included for the report. Repositories are listed by owner/name. E.g.
  wellnow-group/documentation. So to match on all wellnow-group repos,
  simply use the "wellnow*" pattern.

Options:
  --reset-token        Flag to reset the github token stored in the keyring
  --threshold INTEGER  Threshold amount of commits to display the repo in the
                       list.
  --help               Show this message and exit.
```