# Centos / AWS Linux

```
yum remove java-1.7*
yum install java-1.8*
find /usr/lib/jvm/java-1.8* | head -n 3
vim ~/.bash_profile -> add java path
java -version -> java-1.8+
sudo wget -O /etc/yum.repos.d/jenkins.repo https://pkg.jenkins.io/redhat-stable/jenkins.repo
sudo rpm --import https://pkg.jenkins.io/redhat-stable/jenkins.io.key
yum install jenkins
service jenkins start
chkconfig jenkins on
cat /var/lib/jenkins/secrets/initialAdminPassword
```

# Ubuntu

```
apt-get update && apt-get upgrade
apt-get install default-jdk -> install java-1.11+
find /usr/lib/jvm/java-1.11* | head -n 3
vim ~/.bashrc -> add java path
wget -q -O - https://pkg.jenkins.io/debian-stable/jenkins.io.key | sudo apt-key add -
deb https://pkg.jenkins.io/debian-stable binary/
cat deb https://pkg.jenkins.io/debian-stable binary/
>> /etc/apt/sources.list
sudo apt-get install jenkins
```

```
systemctl start jenkins.service
systemctl stop jenkins.service
systemctl restart jenkins.service

service jenkins restart
service jenkins stop
service jenkins start
service jenkins status
```

# Jenkins environment variables

```
environment variables from system:
jenkinsIpAddress:8080/env-vars.html/

can also define in Jenkinsfile:
    environment {
        TEST_PREFIX = "test-IMAGE"
        TEST_IMAGE = "${env.TEST_PREFIX}:${env.BUILD_NUMBER}" //env.BUILD_NUMBER is environment variable from system(jenkinsIpAddress:8080/env-vars.html/)
        TEST_CONTAINER = "${env.TEST_PREFIX}-${env.BUILD_NUMBER}"
        REGISTRY_ADDRESS = "my.registry.address.com"

        SLACK_CHANNEL = "#deployment-notifications"
        SLACK_TEAM_DOMAIN = "MY-SLACK-TEAM"
        SLACK_TOKEN = credentials("slack_token")
        DEPLOY_URL = "https://deployment.example.com/"

        COMPOSE_FILE = "docker-compose.yml"
        REGISTRY_AUTH = credentials("docker-registry")
        STACK_PREFIX = "my-project-stack-name"
    }


```


