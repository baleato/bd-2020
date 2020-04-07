# Amazon aws-cli

## Find the current Amazon Linux 2 AMI

```bash
$ aws ec2 describe-images --owners amazon --filters 'Name=name,Values=amzn2-ami-hvm-2.0.????????.?-x86_64-gp2' 'Name=state,Values=available' --query 'reverse(sort_by(Images, &CreationDate))[:1].ImageId' --output text
```

## Create machine

- Run instance r5a.8xlarge (256G / 32 cores) - https://aws.amazon.com/ec2/pricing/on-demand/
```
$ aws ec2 run-instances --image-id ami-0ec1ba09723e5bfac --count 1 --instance-type r5a.8xlarge --key-name ec2key
```
- Get public DNS
```
aws ec2 describe-instances | grep PublicDns
```

- SSH machine, install, copy and run scripts
```bash
$ chmod 400 ec2key.pem
$ scp -i "ec2key.pem" run.* ec2-user@ec2-18-194-234-40.eu-central-1.compute.amazonaws.com:/home/ec2-user
$ ssh -i "ec2key.pem" ec2-user@ec2-18-194-234-40.eu-central-1.compute.amazonaws.com
$ sudo yum groupinstall 'Development Tools' -y
$ sudo yum install python3 python3-devel.x86_64 -y
$ sudo pip3 install -U memory_profiler surprise
$ bash run.sh
```

- TODO: For DSSTNE we need GPU (g2.8xlarge) and specific image using nvidia-docker
