# Dockerfile

# FROM directive instructing base image to build upon
FROM sfloresk/fed-crypto

ADD . /usr/src/app/

RUN pip install -r /usr/src/app/requirements.txt

ENV USER_ID $(id -u)
ENV GROUP_ID $(id -g)
ENV LD_PRELOAD libnss_wrapper.so
ENV NSS_WRAPPER_PASSWD /usr/src/app/web_ui/data/passwd
ENV NSS_WRAPPER_GROUP /etc/group

# EXPOSE port 8024 to allow communication to/from server
EXPOSE 8025

# CMD specifcies the command to execute to start the server running.
CMD ["/usr/src/app/web_start.sh"]
# done!
