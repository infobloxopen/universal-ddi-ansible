#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: Infoblox Inc.
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: dtc_server_info
short_description: Retrieves DTC Servers
description:
    - Retrieves information about existing DTC Servers.
version_added: 1.1.0
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
    tag_filters:
        description:
            - Filter dict to filter objects by tags
        type: dict
        required: false
    tag_filter_query:
        description:
            - Filter query to filter objects by tags
        type: str
        required: false

extends_documentation_fragment:
    - infoblox.universal_ddi.common
"""  # noqa: E501

EXAMPLES = r"""
- name: Get information about the DTC Server by ID
  infoblox.universal_ddi.dtc_server_info:
    id: "{{ dtc_server.id }}"

- name: Get information about the DTC Server by filters (Name)
  infoblox.universal_ddi.dtc_server_info:
    filters:
      name: "example_dtc_server"

- name: Get information about the DTC Server by filter query
  infoblox.universal_ddi.dtc_server_info:
    filter_query: "name=='example_dtc_server'"

- name: Get information about the DTC Server by tag filters
  infoblox.universal_ddi.dtc_server_info:
    tag_filters:
      location: "site-1"

- name: Get information about the DTC Server by tag filter query
  infoblox.universal_ddi.dtc_server_info:
    tag_filter_query: "location=='site-1'"
"""

RETURN = r"""
id:
    description:
        - ID of the Server object
    type: str
    returned: Always
objects:
    description:
        - Server object
    type: list
    elements: dict
    returned: Always
    contains:
        address:
            description:
                - "IP Address of the B(Server). Must be set to a valid IP address if B(endpoint_type) is set to B(address). Alternatively, it can be left blank."
            type: str
            returned: Always
        auto_create_response_records:
            description:
                - "Optional. If the flag is enabled, A, AAAA or CNAME B(Record) is automatically generated."
                - "Defaults to I(false)."
            type: bool
            returned: Always
        comment:
            description:
                - "Optional. Comment for B(Server)."
            type: str
            returned: Always
        disabled:
            description:
                - "Optional. Flag which enables/disables B(Server)."
                - "Defaults to I(false)."
            type: bool
            returned: Always
        endpoint_type:
            description:
                - "The endpoint type configured for the B(Server). Can be IP Address or FQDN. The values of both fields B(address) and B(fqdn) are preserved and are not mutually exclusive, and the B(endpoint_type) defines which one to use."
                - "Allowed values:"
                - "* address"
                - "* fqdn"
                - "Defaults to B(address)."
            type: str
            returned: Always
        fqdn:
            description:
                - "Fully Qualified Domain name of the B(Server). Must be set to a valid FQDN if B(endpoint_type) is set to B(fqdn). Alternatively, it can be left blank."
            type: str
            returned: Always
        id:
            description:
                - "The resource identifier."
            type: str
            returned: Always
        metadata:
            description:
                - "Output only. B(Server) metadata. Defaults to empty object and should be explicitly requested using field selection."
            type: dict
            returned: Always
            contains:
                used_by:
                    description:
                        - "List of structs representing a limited view on configuration objects that use a resource the metadata is provided for."
                    type: list
                    returned: Always
                    elements: dict
                    contains:
                        details:
                            description:
                                - "Structured data consisting of additional details of the configuration resource."
                            type: dict
                            returned: Always
                        display_name:
                            description:
                                - "Display name of the configuration resource."
                            type: str
                            returned: Always
                        id:
                            description:
                                - "The resource identifier."
                            type: str
                            returned: Always
        name:
            description:
                - "Display name of B(Server)."
            type: str
            returned: Always
        records:
            description:
                - "Optional. List of B(Records) of the B(Server)."
            type: list
            returned: Always
            elements: dict
            contains:
                dns_rdata:
                    description:
                        - "The DNS protocol textual representation of the record data."
                    type: str
                    returned: Always
                rdata:
                    description:
                        - "JSON representation of resource record data."
                    type: dict
                    returned: Always
                type:
                    description:
                        - "Resource record type."
                        - "List of supported types:"
                        - "* I(A) (I(TYPE1))"
                        - "* I(AAAA) (I(TYPE28))"
                        - "* I(CNAME) (I(TYPE5))"
                        - "* I(HTTPS) (I(TYPE65))"
                        - "* I(SRV) (I(TYPE33))"
                        - "* I(SVCB) (I(TYPE64))"
                    type: str
                    returned: Always
        tags:
            description:
                - "Optional. The tags for B(Server) in JSON format."
            type: dict
            returned: Always
"""  # noqa: E501

from ansible_collections.infoblox.universal_ddi.plugins.module_utils.modules import UniversalDDIAnsibleModule

try:
    from dtc import ServerApi
    from universal_ddi_client import ApiException, NotFoundException
except ImportError:
    pass  # Handled by UniversalDDIAnsibleModule


class ServerInfoModule(UniversalDDIAnsibleModule):
    def __init__(self, *args, **kwargs):
        super(ServerInfoModule, self).__init__(*args, **kwargs)
        self._existing = None
        self._limit = 1000

    def find_by_id(self):
        try:
            resp = ServerApi(self.client).read(self.params["id"])
            return [resp.result]
        except NotFoundException as e:
            return []

    def find(self):
        if self.params["id"] is not None:
            return self.find_by_id()

        filter_str = None
        if self.params["filters"] is not None:
            filter_str = " and ".join([f"{k}=='{v}'" for k, v in self.params["filters"].items()])
        elif self.params["filter_query"] is not None:
            filter_str = self.params["filter_query"]

        tag_filter_str = None
        if self.params["tag_filters"] is not None:
            tag_filter_str = " and ".join([f"{k}=='{v}'" for k, v in self.params["tag_filters"].items()])
        elif self.params["tag_filter_query"] is not None:
            tag_filter_str = self.params["tag_filter_query"]

        all_results = []
        offset = 0

        while True:
            try:
                resp = ServerApi(self.client).list(
                    offset=offset, limit=self._limit, filter=filter_str, tfilter=tag_filter_str
                )

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
        tag_filters=dict(type="dict", required=False),
        tag_filter_query=dict(type="str", required=False),
    )

    module = ServerInfoModule(
        argument_spec=module_args,
        supports_check_mode=True,
        mutually_exclusive=[
            ["id", "filters", "filter_query"],
            ["id", "tag_filters", "tag_filter_query"],
        ],
    )
    module.run_command()


if __name__ == "__main__":
    main()
