variable "aws_region" {}
variable "aws_profile" {}
data "aws_availability_zones" "available" {}
variable "vpc_cidr" {}

variable "cidrs" {
  type = map(string)
}

variable "localip" {}

variable "domain_name" {}


#RDS
variable "db_instance_class" {}
variable "dbname" {}
variable "dbuser" {}
variable "dbpassword" {}

#Dev Server
variable "dev_instance_type" {}
variable "dev_ami" {}
variable "public_key_path" {}
variable "key_name" {}

#ELB
variable "elb_healthy_threshold" {}
variable "elb_unhealthy_threshold" {}
variable "elb_timeout" {}
variable "elb_interval" {}

#ASG
variable "lc_instance_type" {}
variable "asg_max" {}
variable "asg_min" {}
variable "asg_grace" {}
variable "asg_hct" {}
variable "asg_cap" {}

#Route53
variable "delegation_set" {}