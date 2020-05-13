# Deploy containerised Ghost on AWS EC2 using Ansible

## Ansible

1. Launch a Ubuntu ec2 instance Ansible Host
   1.1 Install Ansible
   ```
   sudo apt update
   sudo apt install software-properties-common
   sudo apt-add-repository --yes --update ppa:ansible/ansible
   sudo apt install ansible
   ```
2. Launch a Ubuntu ec2 instance for Ansible playbook deployment
   
3. Edit Ansible host file (inventory file)
   `vim /etc/ansible/hosts` -> add localhost and deploy server IP

4. Create an Ansible user
   'sudo adduser ansible"

   