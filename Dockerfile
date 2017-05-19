# Dockerfile

# FROM directive instructing base image to build upon
FROM centos:7

ADD . .

# EXPOSE port 8024 to allow communication to/from server
EXPOSE 8025

# CMD specifcies the command to execute to start the server running.
CMD ["./web_start.sh"]
# done!
