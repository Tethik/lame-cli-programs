import re
import sys
from os.path import expanduser
import boto3
import crayons


TEMPLATE = """
Host {domain}
    HostName {ip}
    User {user}
    {bastion}

"""

DOMAIN_WHITELIST = re.compile(r'[a-zA-Z0-9\-\.]+')
BOTO3_EC2_RUNNING_STATE = 16

def get_tag_val(instance, key):
    try:
        res = filter(lambda t: t['Key'] == key, instance.tags)
        return next(res)['Value']
    except:
        return None



def get_domain(instance):
    val = get_tag_val(instance, 'Domain')
    if val:
        if not re.fullmatch(DOMAIN_WHITELIST, val):
            print(crayons.red(f'Instance {instance.id} had a weird domain name that did not follow conventions: {val}.'))
            return None
        return val
    return None


def get_bastion(instance):
    val = get_tag_val(instance, 'Bastion')
    if val:
        return f"ProxyJump {val}"
    return None


def main():
    ec2 = boto3.resource('ec2')

    with open(expanduser('~/.ssh/aws-hosts-config'), 'w') as file:
        for i in ec2.instances.all():
            if i.state["Code"] != BOTO3_EC2_RUNNING_STATE:
                print(crayons.blue(f'Skipping instance {i.id} because it is not running.'))
                continue

            domain = get_domain(i)
            if not domain:
                print(crayons.yellow(f'Skipping instance {i.id} because it had an empty or no Domain tag.'))
                continue

            bastion = get_bastion(i)
            if bastion:
                ip = i.private_ip_address
            else:
                ip = i.public_ip_address

            if not ip:
                print(crayons.yellow(f'Skipping {domain} because it had no ip to connect to.'))
                continue

            user = get_tag_val(i, 'User') or 'ec2-user'

            print(TEMPLATE.format(domain=domain,ip=ip,user=user,bastion=bastion), file=file)
            print(crayons.green(f'Added {user}@{domain}'))
    print(crayons.green('Succesfully updated ~/.ssh/aws-hosts-config'))

if __name__ == '__main__':
    main()
