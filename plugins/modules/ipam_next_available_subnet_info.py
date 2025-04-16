#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: Infoblox Inc.
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: ipam_next_available_subnet_info
short_description: Retrieves the Next available subnet
description:
    - Retrieves the Next Available Subnet in the specified Address Block
version_added: 2.0.0
author: Infoblox Inc. (@infobloxopen)
options:
    id:
        description:
            - An application specific resource identity of a resource
        type: str
        required: false
    cidr:
        description:
            - The cidr value of address blocks to be created.
        type: int
        required: true
    count:
        description:
            - Number of address blocks to generate. Default 1 if not set.
        type: int
        required: false
        default: 1
    tag_filters:
        description:
            - Filter dict to filter address blocks by tags
        type: dict
        required: false

extends_documentation_fragment:
    - infoblox.universal_ddi.common
"""  # noqa: E501

EXAMPLES = r"""
    - name: "Create an IP Space (required as parent)"
      infoblox.universal_ddi.ipam_ip_space:
        name: "example-ipspace"
        state: "present"
      register: ip_space

    - name: "Create an Address Block (required as parent)"
      infoblox.universal_ddi.ipam_address_block:
        address: "10.0.0.0/16"
        space: "{{ ip_space.id }}"
        state: "present"
      register: address_block

    - name: "Get information about the Subnet"
      infoblox.universal_ddi.ipam_next_available_subnet_info:
        id: "{{ address_block.id }}"
        cidr: 24

    - name: "Get information about the Subnet with count"
      infoblox.universal_ddi.ipam_next_available_subnet_info:
        id: "{{ address_block.id }}"
        cidr: 24
        count: 5

    - name: "Create an Address Block with tags"
      infoblox.universal_ddi.ipam_address_block:
        address: "192.168.0.0/16"
        space: "{{ ip_space.id }}"
        tags:
          environment: "production"
          location: "site-1"
        state: "present"

    - name: "Get next available subnet by a single tag filter"
      infoblox.universal_ddi.ipam_next_available_subnet_info:
        tag_filters:
          environment: "production"
        cidr: 24
        count: 1

    - name: "Get next available subnet by multiple tag filters"
      infoblox.universal_ddi.ipam_next_available_subnet_info:
        tag_filters:
          environment: "production"
          location: "site-1"
        cidr: 28
        count: 5
"""

RETURN = r"""
id:
    description:
        - ID of the Subnet object
    type: str
    returned: Always
objects:
    description:
        - List of next available subnet addresses
    type: list
    elements: str
    returned: Always
"""  # noqa: E501

from ansible_collections.infoblox.universal_ddi.plugins.module_utils.modules import UniversalDDIAnsibleModule

try:
    from ipam import AddressBlockApi
    from universal_ddi_client import ApiException
except ImportError:
    pass  # Handled by UniversalDDIAnsibleModule


class NextAvailableSubnetInfoModule(UniversalDDIAnsibleModule):
    def __init__(self, *args, **kwargs):
        super(NextAvailableSubnetInfoModule, self).__init__(*args, **kwargs)
        self._existing = None
        self._limit = 1000

        # Validate count parameter if provided
        if self.params["count"] is not None and self.params["count"] > 20:
            self.fail_json(msg="Parameter 'count' cannot exceed 20")

    def find_subnet(self, id=None, count=None):
        try:
            resp = AddressBlockApi(self.client).list_next_available_subnet(id=id, cidr=self.params["cidr"], count=count)
            return resp.results
        except ApiException:
            return None

    def find_address_blocks_by_tags(self):
        tag_filter_str = None
        if self.params["tag_filters"]:
            tag_filter_str = " and ".join([f"{k}=='{v}'" for k, v in self.params["tag_filters"].items()])

        offset = 0
        all_results = []  # Initialize a list to accumulate all results

        while True:
            try:
                resp = AddressBlockApi(self.client).list(
                    offset=offset, limit=self._limit, tfilter=tag_filter_str, inherit="full"
                )

                # Accumulate results from this page
                all_results.extend(resp.results)

                if len(resp.results) < self._limit:
                    break
                offset += self._limit

            except ApiException as e:
                self.fail_json(msg=f"Failed to execute command: {e.status} {e.reason} {e.body}")

        return all_results

    def find(self):
        all_results = []
        offset = 0

        while True:
            try:
                resp = AddressBlockApi(self.client).list_next_available_subnet(
                    id=self.params["id"], cidr=self.params["cidr"], count=self.params["count"]
                )
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

        count = self.params["count"]

        # Validate count is within allowed range
        if not 1 <= count <= 20:
            self.fail_json(msg="count must be between 1 and 20.")

        if self.params["tag_filters"]:
            address_blocks = self.find_address_blocks_by_tags()
            if not address_blocks:
                self.fail_json(msg="No address block found with the given tags.")

            find_results = []
            for ab in address_blocks:

                # Check if the address block has next available subnet
                if count > 1:
                    check_result = self.find_subnet(id=ab.id, count=1)
                    if not check_result:
                        continue

                remaining_count = count - len(find_results)
                while len(find_results) < count:
                    find_result = self.find_subnet(id=ab.id, count=remaining_count)
                    if find_result:
                        find_results.extend(find_result)
                        break
                    else:
                        remaining_count -= 1
                        if not remaining_count:
                            break

            if len(find_results) < count:
                self.fail_json(msg="Not enough subnets found with the given tags.")
        else:
            find_results = self.find()

        result["objects"] = [r.address for r in find_results]
        self.exit_json(**result)


def main():
    # define available arguments/parameters a user can pass to the module
    module_args = dict(
        id=dict(type="str", required=False),
        cidr=dict(type="int", required=True),
        count=dict(type="int", required=False, default=1),
        tag_filters=dict(type="dict", required=False),
    )

    module = NextAvailableSubnetInfoModule(
        argument_spec=module_args,
        supports_check_mode=True,
        required_one_of=[["id", "tag_filters"]],
        mutually_exclusive=[["id", "tag_filters"]],
    )
    module.run_command()


if __name__ == "__main__":
    main()
