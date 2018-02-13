# Readme

Generates a hashicorp vault token using a github token taken from the `GITHUB_TOKEN` environment variable.
Set this via your `.profile` or whichever you feel comfortable with (maybe for good security you don't store you tokens in a bash config.)

Install via
```
pip3 install --user "git+https://github.com/Tethik/lame-cli-programs#egg=vaultauth&subdirectory=vaultauth"
```

Use via the following to set the `VAULT_TOKEN` environment variable.
```
source vaultauth
```