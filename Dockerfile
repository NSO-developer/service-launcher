# Dockerfile

# FROM directive instructing base image to build upon
FROM sfloresk/fed-crypto

ADD . /usr/src/app/

RUN pip install -r /usr/src/app/requirements.txt



# EXPOSE port 8024 to allow communication to/from server
EXPOSE 8025

# CMD specifcies the command to execute to start the server running.
CMD ["/usr/src/app/web_start.sh"]
# done!
