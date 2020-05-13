# Jenkins

## Setup Jenkins CICD with Ansible and kubernetes

### work flow:

1. `CI 1`: Developers commit code to Github, Github triggers Jenkins job
2. `CI 2`: Jenkins send war file to Ansible server, Ansible server then builds new docker image by using ansible-playbook (it uses Dockerfile inside ansible-playbook), pushes the image to Dockerhub
3. `CD`: Jenkins notifys Ansible server to trigger K8s deployment and service which pulls new image from Dockerhub and deploy new deployment and service

1 Jenkins server  
1 Ansible server  
1 K8s Management server (kops)  
1 K8s Master node  
2 K8s Worker nodes

Jenkins plugins:
publish over ssh, Deploy to container plugin, Github plugin, Maven Invoker plugin, SCM API plugin

No Jenkinsfile used in this project.
