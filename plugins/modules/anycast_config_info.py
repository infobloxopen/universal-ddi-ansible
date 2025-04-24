#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: Infoblox Inc.
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: anycast_config_info
short_description: Retrieves Anycast Configurations
description:
    - Retrieve all named Anycast configurations for the account.
    - Supports filtering based on account, service, and other query parameters.
version_added: 1.0.0
author: Infoblox Inc. (@infobloxopen)
options:
    id:
        description:
            - ID of the object.
        type: int
        required: false
    name: 
        description:
            - "The name of the anycast configuration."
        type: str
        required: false
    service:
        description:
            - Filter by service type.
        type: str
        choices:
            - DNS
            - DHCP
            - DFP
        required: false
    tag_filters:
        description:
            - Advanced filtering query for configurations.
            - Use the format C(key=='value') for conditions.
        type: dict
        required: false
    tag_filter_query:
        description:
            - Specify ordering of results (e.g., created_at).
        type: str
        required: false

extends_documentation_fragment:
    - infoblox.universal_ddi.common
"""  # noqa: E501

EXAMPLES = r"""
    - name: Get Information about the Anycast Configuration by ID
      infoblox.universal_ddi.anycast_config_info:
        id: "{{ ac_config.id }}"

    - name: Get Information about the Anycast Configuration by service and name
      infoblox.universal_ddi.anycast_config_info:
        service: "DNS"
        name: "ac_config_example"

    - name: Get Anycast Configuration information by tag filters
      infoblox.universal_ddi.anycast_config_info:
        tag_filters:
            location: "site-1"

    - name: Get Anycast Configuration information by tag filter query
      infoblox.universal_ddi.anycast_config_info:
        tag_filter_query: "location=='site-1'"
"""

RETURN = r"""
id:
    description:
        - ID of the Anycast Config object
    type: int
    returned: Always
objects:
    description:
        - Anycast Config object
    type: list
    elements: dict
    returned: Always
    contains:
        account_id:
            description: 
                - "The account identifier."
            type: int
            returned: Always
        anycast_ip_address:
            description: 
                - "IPv4 address of the host in string format."
            type: str
            returned: Always
        anycast_ipv6_address:
            description: 
                - "IPv6 address of the host in string format."
            type: str
            returned: Always
        created_at:
            description: 
                - "Time when the object has been created."
            type: str
            returned: Always
        description:
            description: 
                - "The description for the address object."
                - "May contain 0 to 1024 characters."
                - "Can include UTF-8."
            type: str
            returned: Always
        id:
            description: 
                - "The resource identifier."
            type: int
            returned: Always
        is_configured:
            description:
                - "Boolean value which determines if service is configured."
            type: bool
            returned: Always
        name:
            description: 
                - "The name of the anycast configuration."
            type: str
            returned: Always
        onprem_hosts:
            description: 
                - "The list of on-prem hosts associated with the anycast configuration."
                - "Struct on-prem host reference."
            type: list
            returned: Always
            elements: dict
            contains:
                id:
                    description: 
                        - "Resource Identifier of Onprem Host. It is the equivalent of Legacy ID extracted from the Onprem Host"
                    type: int
                    returned: Always
                ip_address:
                    description:
                        - "IPv4 address of the host in string format"
                        - "example: 11.83.17.55"
                    type: str
                    returned: Always
                ipv6_address:
                    description:
                        - "IPv6 address of the host in string format"
                        - "example: ::1"
                    type: str
                    returned: Always
                name:
                    description: 
                        - "A user friendly name of the host would be, example 'DNS HOST 1', 'Central Office Server'"
                    type: str
                    returned: Always
                ophid:
                    description:
                        - "Unique 32-character string identifier assigned to the host"
                        - "example: 8b9ba7b03d05fbb1b31a41d47968dd43"
                    type: str
                    returned: Always
                runtime_status:
                    description: 
                        - "The runtime status of the anycast configuration host example 'Active', 'Inactive', 'Degraded'"
                    type: str
                    returned: Always
        runtime_status:
            description: 
                - "The runtime status of the anycast configuration."
            type: str
            returned: Always
        service:
            description: 
                - "The type of the Service used in anycast configuration, supports (dns, dhcp, dfp)."
            type: str
            returned: Always
        tags:
            description: 
                - "The tags for the anycast configuration object."
            type: dict
            returned: Always
        updated_at:
            description:
                - "Time when the object has been updated. Equals to created_at if not updated after creation."
            type: str
            returned: Always
"""  # noqa: E501

from ansible_collections.infoblox.universal_ddi.plugins.module_utils.modules import UniversalDDIAnsibleModule

try:
    from anycast import OnPremAnycastManagerApi
    from universal_ddi_client import ApiException, NotFoundException
except ImportError:
    pass  # Handled by UniversalDDIAnsibleModule


class OnPremAnycastManagerInfoModule(UniversalDDIAnsibleModule):
    def __init__(self, *args, **kwargs):
        super(OnPremAnycastManagerInfoModule, self).__init__(*args, **kwargs)
        self._existing = None
        self._limit = 1000

    def find_by_id(self):
        try:
            resp = OnPremAnycastManagerApi(self.client).read_anycast_config_with_runtime_status(self.params["id"])
            return [resp.results]
        except NotFoundException as e:
            return None

    def find(self):
        if self.params["id"] is not None:
            return self.find_by_id()

        tag_filter_str = None
        if self.params["tag_filters"] is not None:
            tag_filter_str = " and ".join([f"{k}=='{v}'" for k, v in self.params["tag_filters"].items()])
        elif self.params["tag_filter_query"] is not None:
            tag_filter_str = self.params["tag_filter_query"]

        service = self.params.get("service")
        name = self.params.get("name")
        all_results = []

        try:
            # Fetch all configurations for the specified service
            resp = OnPremAnycastManagerApi(self.client).get_anycast_config_list(tfilter=tag_filter_str, service=service)

            # If no results, set results to empty list
            if not resp.results:
                resp.results = []

            all_results = resp.results

            if name:
                all_results = [config for config in all_results if config.name == self.params["name"]]

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
    # Define available arguments/parameters a user can pass to the module
    module_args = dict(
        id=dict(type="int", required=False),
        name=dict(type="str", required=False),
        service=dict(type="str", required=False, choices=["DNS", "DHCP", "DFP"]),
        tag_filters=dict(type="dict", required=False),
        tag_filter_query=dict(type="str", required=False),
    )

    # Initialize the module with updated arguments
    module = OnPremAnycastManagerInfoModule(
        argument_spec=module_args,
        supports_check_mode=True,
        mutually_exclusive=[
            ["id", "tag_filters", "tag_filter_query"],
            ["id", "name"],
            ["id", "service"],
        ],
    )
    module.run_command()


if __name__ == "__main__":
    main()
