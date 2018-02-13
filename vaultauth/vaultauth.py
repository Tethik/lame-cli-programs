import os
import hvac
import sys
import keyring
import getpass

def main():
    xargs = {
        'verify': os.getenv('VAULT_CACERT', None),
        'url': os.getenv('VAULT_ADDR', 'http://127.0.0.1:8200'),
        'token': os.getenv('VAULT_TOKEN', None)
    }

    github_token = keyring.get_password("vaultauth", "GITHUB_TOKEN")
    if not github_token:
        print('Found no github token in your keyring.')
        github_token = getpass.getpass('Github Token: ')
        keyring.set_password("vaultauth", "GITHUB_TOKEN", github_token)

    client = hvac.Client(**xargs)
    try:
        res = client.auth_github(github_token)
        token = res['auth']['client_token']
        print(token)
    except Exception as ex:
        print('Authentication failed.', file=sys.stderr)
        print(ex, file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    if '--debug' in [a.strip() for a in sys.argv]:
        print(str(keyring.get_keyring()))
    main()
