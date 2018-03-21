import sys
import boto3

BOTO3_EC2_RUNNING_STATE = 16

def main():
    if len(sys.argv) < 2:
        print(f'Usage: {sys.argv[0]} <tagname>')
        sys.exit(1)

    ec2 = boto3.resource('ec2')

    for i in ec2.instances.all():
        if i.state["Code"] != BOTO3_EC2_RUNNING_STATE:
            continue

        for tag in i.tags:
            if tag['Key'] == 'Name' and tag['Value'] == sys.argv[1]:
                print(i.private_ip_address)

if __name__ == '__main__':
    main()
