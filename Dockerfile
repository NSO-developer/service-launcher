# Dockerfile

# FROM directive instructing base image to build upon
FROM sfloresk/fedora-openshift

RUN yum -y install redhat-rpm-config nss_wrapper gettext python-pip gcc python-devel openssl openssl-devel nss_wrapper gettext ssh openssh

export USER_ID=$(id -u)
export GROUP_ID=$(id -g)
envsubst < /root/passwd.template > /tmp/passwd
export LD_PRELOAD=libnss_wrapper.so
export NSS_WRAPPER_PASSWD=/tmp/passwd
export NSS_WRAPPER_GROUP=/etc/group

RUN pip install -r requirements.txt



# EXPOSE port 8024 to allow communication to/from server
EXPOSE 8025

# CMD specifcies the command to execute to start the server running.
CMD ["./web_start.sh"]
# done!
