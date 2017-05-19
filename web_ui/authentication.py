from envs import *


def log_in(username, password):
    return username == get_username() and password == get_password()


def get_token(username, password):
    """
    Get toking if user and password are correct
    Always return the same token, ideally will connect to an SSO system to get the token
    :param username:
    :param password:
    :return:
    """
    if username == get_username() and password == get_password():
        return "eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJrdWJlcm5ldGVzL3NlcnZpY2VhY2NvdW50Iiwia3ViZXJuZXRlcy"


def is_token_valid(token):
    """
        Check if token is valid. Ideally will connect to an SSO system to validate the token
        :return:
        """
    return token == "eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJrdWJlcm5ldGVzL3NlcnZpY2VhY2NvdW50Iiwia3ViZXJuZXRlcy"
