import os
import json
import sys
import re
import subprocess
from pathlib import Path
import click

TEMPLATE = """
{
    "develop": ["latest","develop-{CIRCLE_BUILD_NUM}","{git_branch}"],
    "feature/(.+)": ["{git_branch}"],
    "master": ["master","master-{CIRCLE_BUILD_NUM}","{git_latest_version_tag}"]
}
"""

FILENAME = '.docker-branch-tagging'

@click.group()
@click.pass_context
def cli(ctx):
    f = Path(FILENAME)
    if not f.exists():
        init.invoke(ctx)

    ctx.obj['config'] = json.loads(f.read_text())
    ctx.obj['git_branch'] = git_branch()
    ctx.obj['git_latest_version_tag'] =  git_latest_version_tag()


@cli.command()
def init():
    Path(FILENAME).write_text(TEMPLATE.strip())
    click.secho(f'Wrote sample {FILENAME} file', color="blue")


def tag_name(template, extras):
    locals().update(os.environ) # magic ;)
    locals().update(extras)
    return template.format(**locals()).replace("/", "-")


def git_branch():
    cmd = 'git rev-parse --abbrev-ref HEAD'
    return subprocess.check_output([cmd], shell=True).decode('utf-8').strip()


def git_latest_version_tag():
    cmd = 'git describe --abbrev=0 --match=[0-9]*.[0-9]*.[0-9]*'
    return subprocess.check_output([cmd], shell=True).decode('utf-8').strip()


def tag_names(ctx, image_name):
    extras = {
        'git_branch': ctx.obj['git_branch'],
        'git_latest_version_tag': ctx.obj['git_latest_version_tag']
    }
    print(ctx.obj['git_branch'])
    for branch_name_pattern, tags in ctx.obj['config'].items():
        if re.match(branch_name_pattern, ctx.obj['git_branch']):
            return [f"{image_name}:{tag_name(template, extras)}" for template in tags]


@cli.command()
@click.argument('image_name')
@click.pass_context
def build(ctx, image_name):
    tags = tag_names(ctx, image_name)
    cmd = f'docker build -t {f" -t ".join(tags)} .'
    print(cmd)
    os.system(cmd)


@cli.command()
@click.argument('image_name')
@click.pass_context
def push(ctx, image_name):
    tags = tag_names(ctx, image_name)
    for tag in tags:
        cmd = f'docker push {tag}'
        print(cmd)
        os.system(cmd)


def main():
    cli(obj={})

if __name__ == "__main__":
    main()
