#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: Infoblox Inc.
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: dhcp_option_code_info
short_description: Retrieve an Option Code
description:
    - Manage OptionCode
version_added: 1.0.0
author: Infoblox Inc. (@infobloxopen)
options:
    id:
        description:
            - ID of the object
        type: str
        required: false
    filters:
        description:
            - Filter dict to filter objects
        type: dict
        required: false
    filter_query:
        description:
            - Filter query to filter objects
        type: str
        required: false
extends_documentation_fragment:
    - infoblox.universal_ddi.common
"""  # noqa: E501

EXAMPLES = r"""
    - name: Get Option Code by ID
      infoblox.universal_ddi.dhcp_option_code_info:
        filters:
          id: "{{ option_code.id }}"
      
    - name: Get DHCP Option Code information by filter query
      infoblox.universal_ddi.dhcp_option_code_info:
        filter_query: "name=='{{ option_code_name }}'"
        
    - name: Get Information about the DHCP Option Code by Name
      infoblox.universal_ddi.dhcp_option_code_info:
        filters:
          name: "{{ option_code_name }}"
            
"""  # noqa: E501
RETURN = r"""
id:
    description:
        - ID of the OptionCode object
    type: str
    returned: Always
objects:
    description:
        - OptionCode object
    type: list
    elements: dict
    returned: Always
    contains:
        array:
            description:
                - "Indicates whether the option value is an array of the type or not."
            type: bool
            returned: Always
        code:
            description:
                - "The option code."
            type: int
            returned: Always
        comment:
            description:
                - "The description for the option code. May contain 0 to 1024 characters. Can include UTF-8."
            type: str
            returned: Always
        created_at:
            description:
                - "Time when the object has been created."
            type: str
            returned: Always
        id:
            description:
                - "The resource identifier."
            type: str
            returned: Always
        name:
            description:
                - "The name of the option code. Must contain 1 to 256 characters. Can include UTF-8."
            type: str
            returned: Always
        option_space:
            description:
                - "The resource identifier."
            type: str
            returned: Always
        source:
            description:
                - "The source for the option code."
                - "Valid values are:"
                - "* I(dhcp_server)"
                - "* I(reserved)"
                - "* I(blox_one_ddi)"
                - "* I(customer)"
                - "Defaults to I(customer)."
            type: str
            returned: Always
        type:
            description:
                - "The option type for the option code."
                - "Valid values are:"
                - "* I(address4)"
                - "* I(address6)"
                - "* I(boolean)"
                - "* I(empty)"
                - "* I(fqdn)"
                - "* I(int8)"
                - "* I(int16)"
                - "* I(int32)"
                - "* I(text)"
                - "* I(uint8)"
                - "* I(uint16)"
                - "* I(uint32)"
            type: str
            returned: Always
        updated_at:
            description:
                - "Time when the object has been updated. Equals to I(created_at) if not updated after creation."
            type: str
            returned: Always
"""  # noqa: E501

from ansible_collections.infoblox.universal_ddi.plugins.module_utils.modules import UniversalDDIAnsibleModule

try:
    from ipam import OptionCodeApi
    from universal_ddi_client import ApiException, NotFoundException
except ImportError:
    pass  # Handled by UniversalDDIAnsibleModule


class OptionCodeInfoModule(UniversalDDIAnsibleModule):
    def __init__(self, *args, **kwargs):
        super(OptionCodeInfoModule, self).__init__(*args, **kwargs)
        self._existing = None
        self._limit = 1000

    def find_by_id(self):
        try:
            resp = OptionCodeApi(self.client).read(self.params["id"])
            return [resp.result]
        except NotFoundException as e:
            return None

    def find(self):
        if self.params["id"] is not None:
            return self.find_by_id()

        filter_str = None
        if self.params["filters"] is not None:
            filter_str = " and ".join(
                [
                    f"{k}=={v}" if isinstance(v, int) else f"{k}=='{v}'"
                    for k, v in self.params["filters"].items()
                    if v is not None
                ]
            )
        elif self.params["filter_query"] is not None:
            filter_str = self.params["filter_query"]

        all_results = []
        offset = 0

        while True:
            try:
                resp = OptionCodeApi(self.client).list(offset=offset, limit=self._limit, filter=filter_str)

                # If no results, set results to empty list
                if not resp.results:
                    resp.results = []

                all_results.extend(resp.results)

                if len(resp.results) < self._limit:
                    break
                offset += self._limit

            except ApiException as e:
                self.fail_json(msg=f"Failed to execute command: {e.status} {e.reason} {e.body}")

        return all_results

    def run_command(self):
        result = dict(objects=[])

        if self.check_mode:
            self.exit_json(**result)

        find_results = self.find()

        all_results = []
        for r in find_results:
            all_results.append(r.model_dump(by_alias=True, exclude_none=True))

        result["objects"] = all_results
        self.exit_json(**result)


def main():
    # define available arguments/parameters a user can pass to the module
    module_args = dict(
        id=dict(type="str", required=False),
        filters=dict(type="dict", required=False),
        filter_query=dict(type="str", required=False),
    )

    module = OptionCodeInfoModule(
        argument_spec=module_args,
        supports_check_mode=True,
        mutually_exclusive=[
            ["id", "filters", "filter_query"],
        ],
    )
    module.run_command()


if __name__ == "__main__":
    main()
