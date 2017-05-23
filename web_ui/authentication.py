"""
   Licensed under the Apache License, Version 2.0 (the "License");
   you may not use this file except in compliance with the License.
   You may obtain a copy of the License at

       http://www.apache.org/licenses/LICENSE-2.0

   Unless required by applicable law or agreed to in writing, software
   distributed under the License is distributed on an "AS IS" BASIS,
   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
   See the License for the specific language governing permissions and
   limitations under the License.
"""
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
