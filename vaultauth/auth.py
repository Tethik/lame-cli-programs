import os
import hvac
import sys


def main():
    xargs = {
        'verify': os.getenv('VAULT_CACERT', None),
        'url': os.getenv('VAULT_ADDR', 'http://127.0.0.1:8200'),
        'token': os.getenv('VAULT_TOKEN', None)
    }

    github_token = os.environ['GITHUB_TOKEN']

    client = hvac.Client(**xargs)
    try:
        res = client.auth_github(github_token)
        print(res['auth']['client_token'])
    except Exception as ex:
        print('Authentication failed.', file=sys.stderr)
        print(ex, file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()
