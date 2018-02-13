# Readme

Generates a hashicorp vault token using a github token taken from the `GITHUB_TOKEN` environment variable.

Install via
```
pip3 install --user "git+https://github.com/Tethik/lame-cli-programs#egg=vaultauth&subdirectory=vaultauth"
```

Use via the following to set the `VAULT_TOKEN` environment variable.
```
source vaultauth
```