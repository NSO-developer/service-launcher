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
import xmltodict, json
from subprocess import call, Popen, PIPE
import os


def yang_to_xml(src, dest=None):
    if dest is not None:
        call(["pyang", "-f", "yin", "-o", dest, src])
    else:
        p = Popen(["pyang", "-f", "yin", src], stdin=PIPE, stdout=PIPE, stderr=PIPE)
        output, err = p.communicate()
        return str(output).replace('\n', '')


def xml_file_to_json(src, dest=None):
    with open(src, 'r') as xml_file:
        xml_data = xml_file.read().replace('\n', '')
    xml_dict = xmltodict.parse(xml_data)
    if dest is None:
        return json.dumps(xml_dict, ensure_ascii=False)
    else:
        with open(dest, 'w') as outfile:
            outfile.write(json.dumps(xml_dict, ensure_ascii=False))


def xml_to_json(xml_data, dest=None):
    xml_dict = xmltodict.parse(xml_data)
    if dest is None:
        return json.dumps(xml_dict, ensure_ascii=False)
    else:
        with open(dest, 'w') as outfile:
            outfile.write(json.dumps(xml_dict, ensure_ascii=False))


# Example of how to call these methods
if __name__ == '__main__':
    DIR_PATH = os.path.dirname(os.path.realpath(__file__))
    yang_to_xml(DIR_PATH + '/yang_templates/nso_service_templates/basic-config.yang')
    xml_file_to_json(DIR_PATH + '/yang_templates/nso_service_templates/basic-config.yang.xml')


def json_to_nso_service_xml(json_dict):
    """
    Takes the json that generates from the service xml and builds
    an xml service definition to be sent to NSO
    :param json_dict:
    :return: service_xml
    """
    # Add service definition
    result = '<services xmlns="http://tail-f.com/ns/ncs">'
    result += '<' + json_dict['module']['name'] + ' xmlns="' + json_dict['module']['namespace']['uri'] + '">'

    # Uses a recursive algorithm to get until the end of the json tree
    result += json_to_nso_variables_xml(json_dict['module']['augment']['list'])

    # Close service definition tags
    result += '</' + json_dict['module']['name'] + '>'
    result += '</services>'
    return result


def json_to_nso_variables_xml(json_dict):
    """
    Recursive method to translate service json attributes into xml string according to YANG
    DO NOT CALL IT DIRECTLY, THIS METHOD SHOULD BE CALLED FROM json_to_nso_service_xml method only
    :param json_dict:
    :return: service_xml attributes
    """
    result = ''

    # If the model has a leaf definition
    if 'leaf' in json_dict.keys():

        # If type is list, then if has more than one leaf
        if isinstance(json_dict['leaf'], type([])):
            for leaf in json_dict['leaf']:
                result += '<' + leaf['name'] + '>' + leaf['ng-value'] + '</' + leaf['name'] + '>'
        else:
            # Just one leaf, no need to loop
            result += '<' + json_dict['leaf']['name'] + '>' + json_dict['leaf']['ng-value'] + '</' + \
                      json_dict['leaf']['name'] + '>'

    # If the model has a leaf-leaf definition
    if 'leaf-list' in json_dict.keys():

        # If type is list, then if has more than one leaf-list
        if isinstance(json_dict['leaf-list'], type([])):
            for leaf_list in json_dict['leaf-list']:
                for item in leaf_list['items']:
                    result += '<' + leaf_list['name'] + '>' + item + '</' + leaf_list['name'] + '>'
        else:
            # Just one leaf-list, no need to loop
            # traverse items
            for item in json_dict['leaf-list']['items']:
                result += '<' + json_dict['leaf-list']['name'] + '>' + item + \
                          '</' + json_dict['leaf-list']['name'] + '>'

    # If the model has a list definition
    if 'list' in json_dict.keys():

        # If type is list, then if has more than one list
        if isinstance(json_dict['list'], type([])):
            for list in json_dict['list']:
                result += '<' + list['name'] + '>'
                # Call this method again to traverse the attributes of the nested list
                result += json_to_nso_variables_xml(list)
                result += '</' + list['name'] + '>'
        else:
            # Just one list, no need to loop
            result += '<' + json_dict['list']['name'] + '>'
            # Call this method again to traverse the attributes of the nested list
            result += json_to_nso_variables_xml(json_dict['list'])
            result += '</' + json_dict['list']['name'] + '>'

    return result
