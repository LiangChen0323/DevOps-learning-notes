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

5. apt/yum modules  
   `ansible remote -b -m apt -a "name=elinks state=present"` install elinks  
   use -b to become default sudo user on remote host  
   -m module  
   -a arguments

6. modules
   `acl` – Set and retrieve file ACL information  
   `archive` – Creates a compressed archive of one or more files or trees  
   `assemble` – Assemble configuration files from fragments  
   `blockinfile` – Insert/update/remove a text block surrounded by marker lines  
   `copy` – Copy files to remote locations  
   `fetch` – Fetch files from remote nodes  
   `file` – Manage files and file properties  
   `find` – Return a list of files based on specific criteria  
   `ini_file` – Tweak settings in INI files  
   `iso_extract` – Extract files from an ISO image  
   `lineinfile` – Manage lines in text files  
   `patch` – Apply patch files using the GNU patch tool  
   `read_csv` – Read a CSV file  
   `replace` – Replace all instances of a particular string in a file using a back-referenced regular expression  
   `stat` – Retrieve file or file system status  
   `synchronize` – A wrapper around rsync to make common tasks in your playbooks quick and easy  
   `tempfile` – Creates temporary files and directories  
   `template` – Template a file out to a remote server  
   `unarchive` – Unpacks an archive after (optionally) copying it from the local machine  
   `xattr` – Manage user defined extended attributes  
   `xml` – Manage bits and pieces of XML files or strings
   `get_url` – Downloads files from HTTP, HTTPS, or FTP to node
   `user` – Manage user accounts  
   `group` – Add or remove groups  
   `package` – Generic OS package manager  
   `service` – Manage services (Controls services on remote hosts. Supported init systems include BSD init, OpenRC, SysV, Solaris SMF, systemd, upstart.)  
   `git` – Manage git checkouts of repositories to deploy files or software.

   `user`: remove user and its related files(home directory)

   ```
   ansible remote -b -m user -a "name=xxx state=absent remove=yes"
   ```

   -B: timeout
   -P: set interval to check the command

7. Ansible Playbook
   ```
   ansible-playbook -i inv playbook.yml
   ```
   -C check mode, dry run

   variable file
   ```
   ansible-playbook xxx.yml -e @vars.yml
   ```