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
"""
Initial config for the application

"""

import db_controller
from api_controller import ApiPackagesNSO
import envs


def sync():
    print "Getting package definitions from NSO:"
    nso_packages_controller = ApiPackagesNSO(envs.get_nso_server_user(), envs.get_nso_server_password(),
                                             envs.get_nso_ip())

    for ned in db_controller.get_neds():
        ned.delete()

    data = nso_packages_controller.get_packages()

    print "Services loaded:"
    print data
