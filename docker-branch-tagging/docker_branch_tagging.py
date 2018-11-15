import os
import json
import sys
import re
import subprocess
from pathlib import Path
import click

TEMPLATE = """
{
    "develop": ["latest","{git_branch}"],
    "feature/(.+)": ["{git_branch}"],
    "master": ["master","{git_latest_version_tag}"]
}
"""

CIRCLECI_TEMPLATE = """
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

@cli.command()
@click.option('--circleci', default=False, is_flag=True)
def init(circleci):
    template = CIRCLECI_TEMPLATE if circleci else TEMPLATE
    Path(FILENAME).write_text(template.strip())
    click.secho('Wrote sample {FILENAME} file'.format(FILENAME=FILENAME), color="blue")


def tag_name(template, extras):
    locals().update(os.environ) # magic ;)
    locals().update(extras)
    return template.format(**locals()).replace("/", "-")


def git_branch():
    cmd = 'git rev-parse --abbrev-ref HEAD'
    return subprocess.check_output([cmd], shell=True).decode('utf-8').strip()


def git_latest_version_tag():
    try:
        cmd = 'git describe --abbrev=0 --match=[0-9]*.[0-9]*.[0-9]*'
        return subprocess.check_output([cmd], shell=True).decode('utf-8').strip()
    except:
        return 'unknown_version'


def tag_names(ctx, image_name):
    extras = {
        'git_branch': git_branch(),
        'git_latest_version_tag': git_latest_version_tag()
    }
    print(ctx.obj['git_branch'])
    for branch_name_pattern, tags in ctx.obj['config'].items():
        if re.match(branch_name_pattern, ctx.obj['git_branch']):
            return ["{image_name}:{tag_name_text}".format(image_name=image_name, tag_name_text=tag_name(template, extras)) for template in tags]


@cli.command()
@click.argument('image_name')
@click.option('--dockerfile')
@click.option('--build-arg', multiple=True)
@click.pass_context
def build(ctx, image_name, dockerfile=None, build_arg=None):
    tags = tag_names(ctx, image_name)
    if not tags:
        print("No build needed.")
        return

    if dockerfile:
        dockerfile = "-f {dockerfile}".format(dockerfile=dockerfile)
    else:
        dockerfile = ""

    tag_text = " -t ".join(tags)
    options = ["-t {tag_text}".format(tag_text=tag_text)]
    if build_arg:
        for b in build_arg:
            options.append("--build-arg {b}".format(b=b))
    cmd = 'docker build {dockerfile} {options} .'.format(dockerfile=dockerfile, options=" ".join(options))
    print(cmd)
    r = os.system(cmd)
    if r != 0:
        sys.exit(1)



@cli.command()
@click.argument('image_name')
@click.pass_context
def push(ctx, image_name):
    tags = tag_names(ctx, image_name)
    if not tags:
        print("No push needed.")
        return

    for tag in tags:
        cmd = "docker push {tag}".format(tag=tag)
        print(cmd)
        r = os.system(cmd)
        if r != 0:
            sys.exit(1)


def main():
    cli(obj={})

if __name__ == "__main__":
    main()
