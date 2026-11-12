#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: Infoblox Inc.
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: ipam_federation_overlapping_block_info
short_description: Retrieves Overlapping Blocks
description:
    - Retrieves information about existing Overlapping Blocks.
    - The Overlapping Block object is a set of contiguous IP addresses with no gap, expressed as a CIDR block. It is explicitly associated with a Federated Realm, and implicitly with a Federated Block parent. An Overlapping Block in a given realm is the child of the closest enclosing parent, and indicates an address range that may be managed independently by all participating IPAM services.
version_added: 1.3.0
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
  - name: Get Overlapping Block information by ID
    infoblox.universal_ddi.ipam_federation_overlapping_block_info:
      filters:
        id: "{{ overlapping_block_id }}"

  - name: Get Overlapping Block information by filters
    infoblox.universal_ddi.ipam_federation_overlapping_block_info:
      filters:
        address: "45.85.1.0/24"

  - name: Get Overlapping Block information by raw filter query
    infoblox.universal_ddi.ipam_federation_overlapping_block_info:
      filter_query: "address=='45.85.1.0/24'"

  - name: Get Overlapping Block information by tag filters
    infoblox.universal_ddi.ipam_federation_overlapping_block_info:
      tag_filters:
        location: "site-1"

  - name: Get Overlapping Block information by tag filter query
    infoblox.universal_ddi.ipam_federation_overlapping_block_info:
      tag_filter_query: "location=='site-1'"
"""  # noqa: E501

RETURN = r"""
id:
    description:
        - ID of the OverlappingBlock object
    type: str
    returned: Always
objects:
    description:
        - OverlappingBlock object
    type: list
    elements: dict
    returned: Always
    contains:
        address:
            description:
                - "The address field in form \"a.b.c.d/n\" where the \"/n\" may be omitted. In this case, the CIDR value must be defined in the I(cidr) field. When reading, the I(address) field is always in the form \"a.b.c.d\"."
            type: str
            returned: Always
        cidr:
            description:
                - "The CIDR of the overlapping block. This is required, if I(address) does not specify it in its input."
            type: int
            returned: Always
        comment:
            description:
                - "The description for the overlapping block. May contain 0 to 1024 characters. Can include UTF-8."
            type: str
            returned: Always
        created_at:
            description:
                - "Time when the object has been created."
            type: str
            returned: Always
        federated_pool_id:
            description:
                - "The resource identifier."
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
                - "The name of the overlapping block. May contain 1 to 256 characters. Can include UTF-8."
            type: str
            returned: Always
        network_compliant:
            description:
                - "The compliance status of the overlapping block, as determined by the federation service."
            type: bool
            returned: Always
        parent:
            description:
                - "The resource identifier."
            type: str
            returned: Always
        protocol:
            description:
                - "The type of protocol of overlapping block (I(ip4) or I(ip6))."
            type: str
            returned: Always
        tags:
            description:
                - "The tags for the overlapping block in JSON format."
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
    from ipam_federation import OverlappingBlockApi
    from universal_ddi_client import ApiException, NotFoundException
except ImportError:
    pass  # Handled by UniversalDDIAnsibleModule


class OverlappingBlockInfoModule(UniversalDDIAnsibleModule):
    def __init__(self, *args, **kwargs):
        super(OverlappingBlockInfoModule, self).__init__(*args, **kwargs)
        self._existing = None
        self._limit = 1000

    def find_by_id(self):
        try:
            resp = OverlappingBlockApi(self.client).read(self.params["id"])
            return [resp.result]
        except NotFoundException as e:
            return []
        except ApiException as e:
            # A malformed id (not just one that no longer exists) is rejected by the API with a
            # 400, not a 404/NotFoundException -- surface it as a clean failure instead of letting
            # the exception propagate as a raw traceback.
            self.fail_json(msg=f"Failed to execute command: {e.status} {e.reason} {e.body}")

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
                resp = OverlappingBlockApi(self.client).list(
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

    module = OverlappingBlockInfoModule(
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
