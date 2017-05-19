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

    2016 - Cisco Systems inc.
"""
from ncclient.operations.rpc import RPC


class SendCommand(RPC):
    """
    Create a new class that inherit from ncclient.operations.rpc.RPC
    """
    __author__ = 'Santiago Flores Kanter (sfloresk@cisco.com)'

    # Override request method from RPC
    def request(self, xml):

        # Send request
        return self._request(xml)
