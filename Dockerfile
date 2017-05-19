# Dockerfile

# FROM directive instructing base image to build upon
FROM sfloresk/fedora-openshift

ADD . .

RUN yum -y install nss_wrapper gettext python-pip gcc python-devel openssl openssl-devel nss_wrapper gettext openssh-server openssh-clients openssh

RUN export USER_ID=$(id -u)
RUN export GROUP_ID=$(id -g)
RUN envsubst < /root/passwd.template > /tmp/passwd
RUN export LD_PRELOAD=libnss_wrapper.so
RUN export NSS_WRAPPER_PASSWD=/tmp/passwd
RUN export NSS_WRAPPER_GROUP=/etc/group

RUN pip install -r requirements.txt



# EXPOSE port 8024 to allow communication to/from server
EXPOSE 8025

# CMD specifcies the command to execute to start the server running.
CMD ["./web_start.sh"]
# done!
