#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: Infoblox Inc.
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: ipam_federated_block_info
short_description: Retrieves information about existing Federated Blocks.
description:
    - The Federated Block object allows a uniform representation of the address space segmentation, supporting functions such as administrative grouping, routing aggregation, delegation etc.
version_added: 2.0.0
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
  - name: Get Federated Block information by ID
    infoblox.universal_ddi.ipam_federated_block_info:
      filters:
        id: "{{ federated_block_id }}"

  - name: Get Federated Block information by filters 
    infoblox.universal_ddi.ipam_federated_block_info:
      filters:
        address: "45.85.0.0/16"
        #federated_realm: "{{ _federated_realm_id }}"

  - name: Get Federated Block information by raw filter query
    infoblox.universal_ddi.ipam_federated_block_info:
      #filter_query: "address=='45.85.0.0/16' and federated_realm=='{{ _federated_realm_id }}'" 
      filter_query: "address=='45.85.0.0/16'"
        
  - name: Get Federated Block information by tag filters
    infoblox.universal_ddi.ipam_federated_block_info:
      tag_filters:
        location: "site-1"
"""  # noqa: E501

RETURN = r"""
id:
    description:
        - ID of the FederatedBlock object
    type: str
    returned: Always
objects:
    description:
        - FederatedBlock object
    type: list
    elements: dict
    returned: Always
    contains:
        address:
            description:
                - "The address field in form \"a.b.c.d/n\" where the \"/n\" may be omitted. In this case, the CIDR value must be defined in the I(cidr) field. When reading, the I(address) field is always in the form \"a.b.c.d\"."
            type: str
            returned: Always
        allocation_v4:
            description:
                - "The percentage of the Federated Block's total address space that is consumed by Leaf Terminals."
            type: dict
            returned: Always
            contains:
                allocated:
                    description:
                        - "Percent of total space allocated."
                    type: int
                    returned: Always
                delegated:
                    description:
                        - "Percent of total space delegated."
                    type: int
                    returned: Always
                overlapping:
                    description:
                        - "Percent of total space in overlapping blocks."
                    type: int
                    returned: Always
                reserved:
                    description:
                        - "Percent of total space reserved."
                    type: int
                    returned: Always
        cidr:
            description:
                - "The CIDR of the federated block. This is required, if I(address) does not specify it in its input."
            type: int
            returned: Always
        comment:
            description:
                - "The description for the federated block. May contain 0 to 1024 characters. Can include UTF-8."
            type: str
            returned: Always
        created_at:
            description:
                - "Time when the object has been created."
            type: str
            returned: Always
        federated_realm:
            description:
                - "The resource identifier."
            type: str
            returned: Always
        id:
            description:
                - "The resource identifier."
            type: str
            returned: Always
        name:
            description:
                - "The name of the federated block. May contain 1 to 256 characters. Can include UTF-8."
            type: str
            returned: Always
        parent:
            description:
                - "The resource identifier."
            type: str
            returned: Always
        protocol:
            description:
                - "The type of protocol of federated block (I(ip4) or I(ip6))."
            type: str
            returned: Always
        tags:
            description:
                - "The tags for the federated block in JSON format."
            type: dict
            returned: Always
        updated_at:
            description:
                - "Time when the object has been updated. Equals to I(created_at) if not updated after creation."
            type: str
            returned: Always
"""  # noqa: E501

from ansible_collections.infoblox.universal_ddi.plugins.module_utils.modules import UniversalDDIAnsibleModule

try:
    from ipam_federation import FederatedBlockApi
    from universal_ddi_client import ApiException, NotFoundException
except ImportError:
    pass  # Handled by UniversalDDIAnsibleModule


class FederatedBlockInfoModule(UniversalDDIAnsibleModule):
    def __init__(self, *args, **kwargs):
        super(FederatedBlockInfoModule, self).__init__(*args, **kwargs)
        self._existing = None
        self._limit = 1000

    def find_by_id(self):
        try:
            resp = FederatedBlockApi(self.client).read(self.params["id"])
            return [resp.result]
        except NotFoundException as e:
            return None

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
                resp = FederatedBlockApi(self.client).list(
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

    module = FederatedBlockInfoModule(
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
