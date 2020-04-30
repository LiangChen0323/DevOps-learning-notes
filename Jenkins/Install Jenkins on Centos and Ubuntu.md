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
