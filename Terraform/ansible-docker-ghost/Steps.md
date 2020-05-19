# Deploy containerised Ghost on AWS EC2 using Ansible

## Ansible

1. Launch a Ubuntu ec2 instance Ansible Host
   1.1 Install Ansible
   ```
   sudo apt update
   sudo apt install software-properties-common
   sudo apt-add-repository --yes --update ppa:ansible/ansible
   sudo apt install ansible -y
   ```
2. Launch a Ubuntu ec2 instance for Ansible playbook deployment

3. Edit Ansible host file (inventory file)
   `vim /etc/ansible/hosts` -> add localhost and target host IP

   `add a dynamic inventory file to check EC2 instances that have tag:Ansible-server on AWS`

4. Create an Ansible user on Ansible host and target hosts
   `sudo adduser ansible`  
    use ansible user do all the ansible related work  
    `ssh-keygen` on Ansible host  
   `cat ~/.ssh/id_rsa.pub >> ~/.ssh/authorized_keys` on Ubuntu (if don't, can't copy ssh key to target hosts)  
    have a common user cross all the target hosts  
   `sudo vim /etc/sudoers` or `sudo visudo` :  
   `# User privilege specification root ALL=(ALL:ALL) ALL ansible ALL=(ALL:ALL) PASSWORD:ALL`change Ansible user privileges on Ansible hosts and target hosts  
   `sudo vim /etc/ssh/sshd_config` change `PasswordAuthentication no` to `PasswordAuthentication no` then `service sshd restart` on Ansible host and target hosts  
    `ssh-copy-id -i id_rsa.pub ansible@xxxx` copy ssh key to target hosts
   `ansible all -m ping` to check if target hosts can be reached

   for newly created Ansible host, need to create a new ssh key and pass it to target hosts
