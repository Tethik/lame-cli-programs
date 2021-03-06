# Readme

Generates Host stanzas for your ssh config for your AWS EC2 instances based on tags.

## Install
```
pip3 install -U --user "git+https://github.com/Tethik/lame-cli-programs#egg=ec2sshgen&subdirectory=ec2-ssh-generator"
```

Add the following to your `.ssh/config` file.
```
Include aws-hosts-config
```

## Usage

Configure your EC2 instances via the following tags, either via the web interface or during Terraforming:
* "Domain" should be a domain name to identify the instance. e.g. `staging.0.evilcorp.internal`
* "User" should be the user used to connect to the instance. Defaults to ec2-user.
* "Bastion" should be the bastion host used (if any) to connect to the instance on a private vpc. e.g. `bastion.evilcorp.internal`

Simply run `ec2sshgen` and your a `.ssh/aws-hosts-config` file will be created for you.

Then `ssh staging.0.evilcorp.internal`

