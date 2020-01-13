# Readme

Calculates and displayes summary of total memory and CPU requirements set on your currently running Nomad jobs.

Output looks something like this:
```
tethik@tethik-XPS-13-9370:~$ nomad-summary --filter=production

+Resource Usages----------------+-----------+-------------+
| Job Name                      | CPU (mhz) | Memory (MB) |
+-------------------------------+-----------+-------------+
| production-b2b-backend        | 100       | 512         |
| production-muv-app            | 100       | 256         |
| production-laskar             | 100       | 256         |
| production-auth               | 100       | 128         |
| production-b2b-admin          | 500       | 64          |
| production-b2b-calendar-admin | 100       | 64          |
| production-worker             | 100       | 64          |
+-------------------------------+-----------+-------------+

+Total Usage--------+
| Memory | 1344 MB  |
| CPU    | 1100 Mhz |
+--------+----------+
```

Install via
```
pip3 install -U --user "git+https://github.com/Tethik/lame-cli-programs#egg=nomad-summary&subdirectory=nomad-summary"
```

## Usage
```
Usage: nomad-summary [OPTIONS]

Options:
  --filter TEXT  Filter for jobnames (e.g. "production"). Accepts a regex
                 pattern.
  --help         Show this message and exit.
```

For now, expects Nomad to be accessible on localhost.