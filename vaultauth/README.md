# Readme

Generates a hashicorp vault token using a github token. The script attempts to use your OS' keyring.

Install via
```
pip3 install -U --user "git+https://github.com/Tethik/lame-cli-programs#egg=vaultauth&subdirectory=vaultauth"
```

Use via the following to set the `VAULT_TOKEN` environment variable.
```
source vaultauth
```