# Readme

Generates Host stanzas for your ssh config for your AWS EC2 instances based on tags.

Configure your EC2 instances via the following tags:
* "Domain" should be a domain name to identify the instance. e.g. `staging.0.evilcorp.internal`
* "User" should be the user used to connect to the instance. Defaults to ec2-user.
* "Bastion" should be the bastion host used (if any) to connect to the instance on a private vpc. e.g. `bastion.evilcorp.internal`

## Install
```
pip3 install -U --user "git+https://github.com/Tethik/lame-cli-programs#egg=ec2sshgen&subdirectory=ec2sshgen"
```

## Usage
Add the following to your `.ssh/config` file.
```
Include aws-hosts-config
```



