# Deploy ec2 using Terraform and Ansible

## Server setup

1. launch a Ubuntu ec2 instance

   1.1 apt-get update  
   1.2 apt install python3/python and pip3/pip  
   1.3 download terraform, unzip it and move to /bin/terraform  
   `curl -O https://releases.hashicorp.com/terraform/0.12.24/terraform_0.12.24_linux_amd64.zip`  
   `unzip terraform_0.12.24_linux_amd64.zip -d /bin/terraform/`  
   1.4 add terraform path to .bashrc  
   `export PATH="$PATH:/bin/terraform"` then `source ~/.bashrc`  
   1.5 install awscli  
   `pip3 install awscli --upgrade`  
   1.6 intall ansible  
   `apt-get install software-properties-common`  
   `apt-add-repository ppa:ansible/ansible`  
   `apt-get update`  
   `apt-get install ansible`  
   1.7 create ssh key, add key to ssh agent, need to add key to ssh agent every time logout login  
   `ssh-keygen` `ssh-agent bash` `ssh-add ~/.ssh/id_rsa` `ssh-add -l`  
   1.8 disable ansible ssh key host checking  
   `vim /etc/ansible/ansible.cfg`  
   uncommit `#host_key_checking = False`

2. AWS IAM and route 53  
   2.1 Create an user with `AdministratorAccess` policy  
   2.2 Setup hosted zone:`liangchen0323.net`  
   2.3 setup awscli  
   `aws configure --profile liangchen` use the user credential created at 2.1  
   `aws ec2 describe-instance --profile liangchen` check if the credential is working  
   2.4 create delegation  
   `aws route53 create-reusable-delegation-set --caller-reference 1224 --profile liangchen` save the output to a file => update Registered domains and host zone?

3. Create Credentials and variables
   3.1 create files under /home/user/terransible -> working dir
   `touch main.tf terraform.tfvars variables.tf userdata aws_hosts wordpress.yml s3update.yml`  
    3.2 set variables  
    main.tf

   ```
   provider "aws" {
     region  = var.aws_region
     profile = var.aws_profile
   }
   ```

   variables.tf

   ```
   variable "aws_region" {}
   variable "aws_profile" {}
   ```

   terraform.tfvars

   ```
   aws_profile = "liangchen"
   aws_region  = "us-east-1"
   ```

   3.4 create aws_iam_instance_profile, aws_iam_instance_profile and aws_iam_role  
    aws_iam_instance_profile consists of aws_iam_instance_profile and aws_iam_role, can be appiled to ec2 instance(iam_instance_profile)

   ```
   resource "aws_iam_instance_profile" "s3_access_profile" {
     name = "s3_access"
     role = aws_iam_role.s3_access_role.name
   }

   resource "aws_iam_role_policy" "s3_access_policy" {
     name = "s3_access_policy"
     role = aws_iam_role.s3_access_role.id

     policy = <<EOF
   {
     "Version": "2012-10-17",
     "Statement": [
       {
         "Effect": "Allow",
         "Action": "s3:*",
         "Resource": "*"
       }
     ]
   }
   EOF
   }

   resource "aws_iam_role" "s3_access_role" {
     name = "s3_access_role"

     assume_role_policy = <<EOF
   {
     "Version": "2012-10-17",
     "Statement": [
     {
         "Action": "sts:AssumeRole",
         "Principal": {
           "Service": "ec2.amazonaws.com"
     },
         "Effect": "Allow",
         "Sid": ""
         }
       ]
   }
   EOF
   }
   ```
