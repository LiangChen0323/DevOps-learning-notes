# Deploy ec2 using Terraform and Ansible

## Terraform

1.  launch a Ubuntu ec2 instance

    1.1 apt-get update  
    1.2 apt install python3/python and pip3/pip  
    1.3 download terraform, unzip it and move to /bin/terraform  
    `curl -O https://releases.hashicorp.com/terraform/0.12.24/terraform_0.12.24_linux_amd64.zip`  
    `unzip terraform_0.12.24_linux_amd64.zip -d /bin/terraform/`  
    1.4 add terraform path to .bashrc  
    `export PATH="$PATH:/bin/terraform"` then `source ~/.bashrc`  
    1.5 install awscli  
    `pip3 install awscli --upgrade`  
    1.6 install ansible  
    `apt-get install software-properties-common`  
    `apt-add-repository ppa:ansible/ansible`  
    `apt-get update`  
    `apt-get install ansible`  
    1.7 create ssh key, add key to ssh agent, need to add key to ssh agent every time logout login  
    `ssh-keygen` `ssh-agent bash` `ssh-add ~/.ssh/id_rsa` `ssh-add -l`  
    1.8 disable ansible ssh key host checking  
    `vim /etc/ansible/ansible.cfg`  
    uncomment `#host_key_checking = False`

2.  AWS IAM and route 53  
    2.1 Create an user with `AdministratorAccess` policy  
    2.2 Setup hosted zone:`liangchen0323.net`  
    2.3 setup awscli  
    `aws configure --profile liangchen` use the user credential created at 2.1  
    `aws ec2 describe-instance --profile liangchen` check if the credential is working  
    2.4 create delegation  
    `aws route53 create-reusable-delegation-set --caller-reference 1224 --profile liangchen` save the output to a file => update Registered domains and host zone?

3.  Create Credentials and variables  
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

4.  Create VPC, internet gateway, public and private route table(default)  
    4.1 VPC

    ```
    resource "aws_vpc" "wp_vpc" {
      cidr_block = var.vpc_cidr
      enable_dns_hostnames = true
      enable_dns_support  = true

      tags = {
        Name = "wp_vpc"
      }
    }
    ```

    4.2 Internet gateway

    ```
    resource "aws_internet_gateway" "wp_internet_gateway" {
     vpc_id = aws_vpc.wp_vpc.id
     tags = {
       Name = "wp_igw"
     }
    }
    ```

    4.3 Route tables public and private(default)

    ```
    resource "aws_route_table" "wp_public_rt" {
      vpc_id = aws_vpc.wp_vpc.id

      route {
        cidr_block = "0.0.0.0/0"
        gateway_id = aws_internet_gateway.wp_internet_gateway.id
      }

      tags = {
        Name = "wp_public"
      }
    }

    resource "aws_default_route_table" "wp_private_rt" {
      default_route_table_id = aws_vpc.wp_vpc.default_route_table_id

      tags = {
        Name = "wp_private"
      }
    }
    ```

    4.4 Subnets, 2 public 2 private 3 private for rds  
     main.tf

    ```
    resource "aws_subnet" "wp_public1_subnet" {
      vpc_id                  = aws_vpc.wp_vpc.id
      cidr_block              = var.cidrs["public1"]
      map_public_ip_on_launch = true
      availability_zone       = data.aws_availability_zones.available.names[0]

      tags = {
        Name = "wp_public1"
      }
    }

    resource "aws_subnet" "wp_public2_subnet" {
      vpc_id                  = aws_vpc.wp_vpc.id
      cidr_block              = var.cidrs["public2"]
      map_public_ip_on_launch = true
      availability_zone       = data.aws_availability_zones.available.names[1]

      tags = {
        Name = "wp_public2"
      }
    }

    resource "aws_subnet" "wp_private1_subnet" {
      vpc_id                  = aws_vpc.wp_vpc.id
      cidr_block              = var.cidrs["private1"]
      map_public_ip_on_launch = false
      availability_zone       = data.aws_availability_zones.available.names[0]

      tags = {
        Name = "wp_private1"
      }
    }

    resource "aws_subnet" "wp_private2_subnet" {
      vpc_id                  = aws_vpc.wp_vpc.id
      cidr_block              = var.cidrs["private2"]
      map_public_ip_on_launch = false
      availability_zone       = data.aws_availability_zones.available.names[1]

      tags = {
        Name = "wp_private2"
      }
    }

    resource "aws_subnet" "wp_rds1_subnet" {
      vpc_id                  = aws_vpc.wp_vpc.id
      cidr_block              = var.cidrs["rds1"]
      map_public_ip_on_launch = false
      availability_zone       = data.aws_availability_zones.available.names[0]

      tags = {
        Name = "wp_rds1"
      }
    }

    resource "aws_subnet" "wp_rds2_subnet" {
      vpc_id                  = aws_vpc.wp_vpc.id
      cidr_block              = var.cidrs["rds2"]
      map_public_ip_on_launch = false
      availability_zone       = data.aws_availability_zones.available.names[1]

      tags = {
        Name = "wp_rds2"
      }
    }

    resource "aws_subnet" "wp_rds3_subnet" {
      vpc_id                  = aws_vpc.wp_vpc.id
      cidr_block              = var.cidrs["rds3"]
      map_public_ip_on_launch = false
      availability_zone       = data.aws_availability_zones.available.names[2]

      tags = {
        Name = "wp_rds3"
      }
    }
    ```

    variable.tf

    ```
    variable "cidrs" {
      type = map(string)
    }
    ```

    terraform.tfvars

    ```
    cidrs = {
      public1  = "10.0.1.0/24"
      public2  = "10.0.2.0/24"
      private1 = "10.0.3.0/24"
      private2 = "10.0.4.0/24"
      rds1     = "10.0.5.0/24"
      rds2     = "10.0.6.0/24"
      rds3     = "10.0.7.0/24"
    }
    ```

    4.5 RDS Subnet group

    ```
    resource "aws_db_subnet_group" "wp_rds_subnetgroup" {
      name = "wp_rds_subnetgroup"

      subnet_ids = [aws_subnet.wp_rds1_subnet.id,
        aws_subnet.wp_rds2_subnet.id,
        aws_subnet.wp_rds3_subnet.id
      ]
      tags = {
        Name = "wp_rds_sng"
      }
    }
    ```

    4.6 Route associtions

    ```
    resource "aws_route_table_association" "wp_public_assoc" {
      subnet_id      = aws_subnet.wp_public1_subnet.id
      route_table_id = aws_route_table.wp_public_rt.id
    }

    resource "aws_route_table_association" "wp_public2_assoc" {
      subnet_id      = aws_subnet.wp_public2_subnet.id
      route_table_id = aws_route_table.wp_public_rt.id
    }

    resource "aws_route_table_association" "wp_private1_assoc" {
      subnet_id      = aws_subnet.wp_private1_subnet.id
      route_table_id = aws_default_route_table.wp_private_rt.id
    }

    resource "aws_route_table_association" "wp_private2_assoc" {
      subnet_id      = aws_subnet.wp_private2_subnet.id
      route_table_id = aws_default_route_table.wp_private_rt.id
    }
    ```

5.  Security groups  
    main.tf

    ```
    # Security groups for dev instance

    resource "aws_security_group" "wp_dev_sg" {
      name        = "wp_dev_sg"
      description = "Used for access to the dev instance"
      vpc_id      = aws_vpc.wp_vpc.id
      # SSH
      ingress {
        from_port   = 22
        to_port     = 22
        protocol    = "tcp"
        cidr_blocks = [var.localip]
      }

      # HTTP
      ingress {
        from_port   = 80
        to_port     = 80
        protocol    = "tcp"
        cidr_blocks = [var.localip]
      }

      egress {
        from_port   = 0
        to_port     = 0
        protocol    = "-1"
        cidr_blocks = ["0.0.0.0/0"]
      }
    }

    # Public Instance Security group
    resource "aws_security_group" "wp_public_sg" {
      name        = "wp_public_sg"
      description = "Used for the elastic load balancer for public access"
      vpc_id      = aws_vpc.wp_vpc.id

      #HTTP
      ingress {
        from_port   = 80
        to_port     = 80
        protocol    = "tcp"
        cidr_blocks = ["0.0.0.0/0"]

      }
      egress {
        from_port   = 0
        to_port     = 0
        protocol    = "-1"
        cidr_blocks = ["0.0.0.0/0"]
      }
    }

    # Private Instance Security group
    resource "aws_security_group" "wp_private_sg" {
      name        = "wp_private_sg"
      description = "Used for private instances"
      vpc_id      = aws_vpc.wp_vpc.id

      # Access from VPC
      ingress {
        from_port   = 0
        to_port     = 0
        protocol    = "-1"
        cidr_blocks = [var.vpc_cidr]
      }
      egress {
        from_port   = 0
        to_port     = 0
        protocol    = "-1"
        cidr_blocks = ["0.0.0.0/0"]
      }
    }

    # RDS Security group
    resource "aws_security_group" "wp_rds_sg" {
      name        = "wp_rds_sg"
      description = "Used for RDS instances"
      vpc_id      = aws_vpc.wp_vpc.id

      # SQL access from public/private security groups
      ingress {
        from_port = 3306
        to_port   = 3306
        protocol  = "tcp"
        security_groups = [aws_security_group.wp_dev_sg.id,
          aws_security_group.wp_public_sg.id,
        aws_security_group.wp_private_sg.id]
      }
    }
    ```

    variable.tf

    ```
    variable "localip" {}
    ```

    terraform.tfvars

    ```
    localip = "54.165.251.2/32"
    ```

6.  S3 end point

    ```
    resource "aws_vpc_endpoint" "wp_private-s3_endpoint" {
      vpc_id       = aws_vpc.wp_vpc.id
      service_name = "com.amazonaws.${var.aws_region}.s3"
      route_table_ids = [aws_vpc.wp_vpc.main_route_table_id,
        aws_route_table.wp_public_rt.id
      ]
      policy = <<POLICY
    {
        "Statement": [
            {
                "Action": "*",
                "Effect": "Allow",
                "Resource": "*",
                "Principal": "*"
            }
        ]
    }
    POLICY
    }
    ```

7.  S3 bucket  
    main.tf  
    need to apply "terraform init" to add provider.random module

    ```
    resource "random_id" "wp_code_bucket" {
      byte_length = 2
    }
    resource "aws_s3_bucket" "code" {
      bucket        = "${var.domain_name}-${random_id.wp_code_bucket.dec}"
      acl           = "private"
      force_destroy = true
      tags = {
        Name = "code bucket"
      }
    }
    ```

    variable.tf

    ```
    variable "domain_name" {}
    ```

    terraform.tfvars

    ```
    domain_name = "liangchen0323"
    ```

8.  RDS  
    main.tf

    ```
    resource "aws_db_instance" "wp_db" {
      allocated_storage      = 10
      engine                 = "mysql"
      engine_version         = "5.6.27"
      instance_class         = var.db_instance_class
      name                   = var.dbname
      username               = var.dbuser
      password               = var.dbpassword
      db_subnet_group_name   = aws_db_subnet_group.wp_rds_subnetgroup.name
      vpc_security_group_ids = [aws_security_group.wp_rds_sg.id]
      skip_final_snapshot    = true
    }
    ```

    variable.tf

    ```
    variable "db_instance_class" {}
    variable "dbname" {}
    variable "dbuser" {}
    variable "dbpassword" {}
    ```

    terraform.tfvars

    ```
    db_instance_class = "db.t2.micro"
    dbname            = "wp_database"
    dbuser            = "admin"
    dbpassword        = "Password123"
    ```

9.  Dev Server  
    main.tf

    ```
    #key pair
    resource "aws_key_pair" "wp_auth" {
    key_name   = var.key_name
    public_key = file(var.public_key_path)
    }

    #dev server
    resource "aws_instance" "wp_dev" {
    instance_type = var.dev_instance_type
    ami           = var.dev_ami
    tags = {
     Name = "wp_dev"
    }
    key_name               = aws_key_pair.wp_auth.id
    vpc_security_group_ids = [aws_security_group.wp_dev_sg.id]
    iam_instance_profile   = aws_iam_instance_profile.s3_access_profile.id
    subnet_id              = aws_subnet.wp_public1_subnet.id

    provisioner "local-exec" {
    command = <<EOD
    cat <<EOF > aws_hosts
    [dev]
    ${aws_instance.wp_dev.public_ip}
    [dev:vars]
    s3code=${aws_s3_bucket.code.bucket}
    domain=${var.domain_name}
    EOF
    EOD
      }
      provisioner "local-exec" {
        command = "aws ec2 wait instance-status-ok --instance-ids ${aws_instance.wp_dev.id} --profile     liangchen && ansible-playbook -i aws_hosts wordpress.yml"
    }
    }
    ```

    variable.tf

    ```
    #Dev Server
    variable "dev_instance_type" {}
    variable "dev_ami" {}
    variable "public_key_path" {}
    variable "key_name" {}
    ```

    terraform.tfvars

    ```
    #Dev Server
    dev_instance_type = "t2.micro"
    dev_ami           = "ami-0915e09cc7ceee3ab"
    public_key_path   = "/root/.ssh/id_rsa.pub"
    key_name          = "id_rsa"
    ```

10. Load balancer  
     main.tf

    ```
    resource "aws_elb" "wp_elb" {
      name = "${var.domain_name}-elb"

      subnets = [aws_subnet.wp_public1_subnet.id,
        aws_subnet.wp_public2_subnet.id,
      ]

      security_groups = [aws_security_group.wp_public_sg.id]

      listener {
        instance_port     = 80
        instance_protocol = "http"
        lb_port           = 80
        lb_protocol       = "http"
      }

      health_check {
        healthy_threshold   = var.elb_healthy_threshold
        unhealthy_threshold = var.elb_unhealthy_threshold
        timeout             = var.elb_timeout
        target              = "TCP:80"
        interval            = var.elb_interval
      }

      cross_zone_load_balancing   = true
      idle_timeout                = 400
      connection_draining         = true
      connection_draining_timeout = 400

      tags = {
        Name = "wp_${var.domain_name}-elb"
      }
    }
    ```

    variable.tf

    ```

     variable "elb_healthy_threshold" {}
     variable "elb_unhealthy_threshold" {}
     variable "elb_timeout" {}
     variable "elb_interval" {}
    ```

    terraform.tfvars

    ```
     elb_healthy_threshold = "2"
     elb_unhealthy_threshold = "2"
     elb_timeout = "3"
     elb_interval = "30"

    ```

11. Gold AMI  
    main.tf

    ```
     resource "random_id" "golden_ami" {
       byte_length = 8
     }

     resource "aws_ami_from_instance" "wp_golden"{
       name               = "wp_ami-${random_id.golden_ami.b64}"
       source_instance_id = aws_instance.wp_dev.id
       provisioner "local-exec" {
         command = <<EOT
     cat <<EOF > userdata
     #!/bin/bash
     /usr/bin/aws s3 sync s3://${aws_s3_bucket.code.bucket} /var/www/html/
     /bin/touch /var/spool/cron/root
     sudo /bin/echo '*/5 * * * * aws s3 sync s3://${aws_s3_bucket.code.bucket} /    var/www/html/' >> /var/spool/cron/root
     EOF
     EOT
       }
     }
    ```

12. ASG and Launch configuration  
    main.tf

    ```
    #----- Launch configuration -----
    resource "aws_launch_configuration" "wp_lc" {
      name_prefix          = "wp_lc-"
      image_id             = aws_ami_from_instance.wp_golden.id
      instance_type        = var.lc_instance_type
      security_groups      = [aws_security_group.wp_private_sg.id]
      iam_instance_profile = aws_iam_instance_profile.s3_access_profile.id
      key_name             = aws_key_pair.wp_auth.id
      user_data            = file("userdata")
      lifecycle {
        create_before_destroy = true
      }
    }
    #----- ASG -----
    resource "aws_autoscaling_group" "wp_asg" {
      name                      = "asg-${aws_launch_configuration.wp_lc.id}"
      max_size                  = var.asg_max
      min_size                  = var.asg_min
      health_check_grace_period = var.asg_grace
      health_check_type         = var.asg_hct
      desired_capacity          = var.asg_cap
      force_delete              = true
      load_balancers            = [aws_elb.wp_elb.id]

      vpc_zone_identifier = [aws_subnet.wp_private1_subnet.id, aws_subnet.wp_private2_subnet.id]

      launch_configuration = aws_launch_configuration.wp_lc.name
      # tags = {
      #   key                 = "Name"
      #   value               = "wp_asg-instance"
      #   propagate_at_launch = true
      # }
      lifecycle {
        create_before_destroy = true
      }
    }
    ```

    variable.tf

    ```
    #ASG
    variable "lc_instance_type" {}
    variable "asg_max" {}
    variable "asg_min" {}
    variable "asg_grace" {}
    variable "asg_hct" {}
    variable "asg_cap" {}
    ```

    terraform.tfvar

    ```
    #ASG
    lc_instance_type = "t2.micro"
    asg_max          = "2"
    asg_min          = "1"
    asg_grace        = "300"
    asg_hct          = "EC2"
    asg_cap          = "2"
        asg_cap          = "2"
                asg_cap          = "2"
    ```
