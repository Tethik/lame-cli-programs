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

### Examples
```sh
docker-branch-taggin build aws-blahabhla.com/example
> docker build -t aws-blahabhla.com/example:master -t aws-blahabhla.com/example:master-123 -t aws-blahabhla.com/example:0.2.1 .
```

```sh
docker-branch-tagging push aws-blahabhla.com/example
> docker push aws-blahabhla.com/example:master 
> docker push aws-blahabhla.com/example:master-123
> docker push aws-blahabhla.com/example:0.2.1
```


