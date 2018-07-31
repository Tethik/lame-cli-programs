# Readme

Finds and stops old ecs tasks if there is a newer version available (based on docker tag). It will decide that a tag is newer
via a simple lexical comparison.

## Install
```
pip3 install -U --user "git+https://github.com/Tethik/lame-cli-programs#egg=ecs_stop_redundant_tasks&subdirectory=ecs-stop-redundant-tasks"
```

## Usage
```
ecs_stop_redundant_tasks <staging|production> [--force]
```

Without `--force` the script will prompt you for a "yes" to continue.
