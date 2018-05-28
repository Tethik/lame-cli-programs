# Readme

## Install
```
pip3 install -U --user "git+https://github.com/Tethik/lame-cli-programs#egg=docker_branch_tagging&subdirectory=docker-branch-tagging"
```

## Usage

In your repo define a .docker-branch-tagging file as a json file.
```json
{
	"develop": ["latest","develop-{CIRCLE_BUILD_NUM}","{git_branch}"],
	"feature/(.+)": ["{git_branch}"],
	"master": ["master","master-{CIRCLE_BUILD_NUM}","{git_latest_version_tag}"]
}
```

Should be an object where the keys are a regex pattern for the git branch name
and the values are lists of tag templates as python format strings.

Variables are populated directly from the environment variables. There is also two special variables:
`git_branch` (the current branch) and `git_latest_version_tag` (`git describe --abbrev=0 --match=[0-9]*.[0-9]*.[0-9]*`).

```
docker-branch-tagging build <image_name>
docker-branch-tagging push <image_name>
```


