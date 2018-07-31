import re
import sys
from os.path import expanduser
import boto3
import crayons

DOMAIN_WHITELIST = re.compile(r'[a-zA-Z0-9\-\.]+')


def main():
    if len(sys.argv) <= 1:
        print("Usage ecs_stop_redundant_tasks <staging|production> [--force]")
        sys.exit(1)

    cluster = sys.argv[1]
    if not cluster or cluster not in ["staging", "production"]:
        print("Please provide cluster staging or production", file=sys.stderr)
        sys.exit(1)

    client = boto3.client('ecs')
    latest_task = dict()
    redundant_tasks = []
    taskArns = client.list_tasks(cluster=cluster, desiredStatus="RUNNING")['taskArns']
    # print(taskArns, sep='\n')
    for task in client.describe_tasks(cluster=cluster, tasks=taskArns)['tasks']:
        image = task['taskDefinitionArn'].split('/')[1]
        # print(image)
        service_name, tag = image.split(':')
        # print(service_name, tag)
        val = (tag, task['taskArn'], service_name)
        if not service_name in latest_task:
            latest_task[service_name] = val

        if tag < latest_task[service_name][0]:
            redundant_tasks.append(val)
        elif tag > latest_task[service_name][0]:
            redundant_tasks.append(latest_task[service_name])
            latest_task[service_name] = val

    if not redundant_tasks:
        print(crayons.green('No redundant tasks found :)'))
        return

    print('The following tasks seem redundant:')
    for tag, taskArn, service_name in redundant_tasks:
        print('\t', f'{service_name}-{tag}', "because it looks older than", f'{latest_task[service_name][2]}-{latest_task[service_name][0]}')

    print()
    if "--force" in sys.argv or input("Sure you want to continue? ") != "yes":
        return

    for tag, taskArn, service_name in redundant_tasks:
        print(crayons.red(f'Stopping {service_name}-{tag}. ARN: {taskArn}'))
        client.stop_task(cluster=cluster, task=taskArn)


if __name__ == '__main__':
    main()
