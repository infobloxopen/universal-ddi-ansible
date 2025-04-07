#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: Infoblox Inc.
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: ipam_next_available_ip_info
short_description: Retrieves the Next available IP addresses
description:
    - Retrieves the next available IP addresses in the specified resource
    - The resource can be an address block, subnet or range.
version_added: 2.0.0
author: Infoblox Inc. (@infobloxopen)
options:
    id:
        description:
            - "ID of the object."
        type: str
        required: false
    contiguous:
        description:
            - "Indicates whether the IP addresses should belong to a contiguous block."
        type: bool
        default: false
        required: false
    count:
        description:
            - "The number of IP addresses requested."
            - "Value must be between 1 and 20."
        type: int
        default: 1
        required: false
    tag_filters:
        description:
            - "Filter dict to filter address blocks, subnets or ranges by tags"
        type: dict
        required: false
    resource_type:
        description:
            - "Type of resource to filter when using tag_filters. Required when tag_filters is provided."
            - "Options are 'address_block', 'subnet', or 'range'."
        type: str
        required: false
        choices:
            - address_block
            - subnet
            - range

extends_documentation_fragment:
    - infoblox.universal_ddi.common
"""  # noqa: E501

EXAMPLES = r"""
    - name: Get Information about Next Available IP in Address Block
      infoblox.universal_ddi.ipam_next_available_ip_info:
        id: "{{ _address_block.id }}"
        count: 5

    - name: Get Information about Next Available IP in Address Block Default Count
      infoblox.universal_ddi.ipam_next_available_ip_info:
        id: "{{ _address_block.id }}"

    - name: Get Information about Next Available IP in Subnet
      infoblox.universal_ddi.ipam_next_available_ip_info:
        id: "{{ _subnet.id }}"
        count: 5

    - name: Get Information about Next Available IP in Subnet Default Count
      infoblox.universal_ddi.ipam_next_available_ip_info:
        id: "{{ _subnet.id }}"
        
    - name: Get Information about Next Available IP in Range
      infoblox.universal_ddi.ipam_next_available_ip_info:
        id: "{{ _range.id }}"
        count: 5
        
    - name: Get Information about Next Available IP in Range Default Count
      infoblox.universal_ddi.ipam_next_available_ip_info:
        id: "{{ _range.id }}"
   
    - name: Get Information about Next Available IP in Address Blocks filtered by tags
      infoblox.universal_ddi.ipam_next_available_ip_info:
        tag_filters:
          environment: "production"
        resource_type: "address_block"
        count: 5
        
    - name: Get Information about Next Available IP in Subnets filtered by tags
      infoblox.universal_ddi.ipam_next_available_ip_info:
        tag_filters:
          environment: "production"
        resource_type: "subnet"
        count: 5
"""  # noqa: E501

RETURN = r"""
id:
    description:
        - ID of the Address object
    type: str
    returned: Always
objects:
    description:
        - List of next available ip addresses
    type: list
    elements: str
    returned: Always
"""  # noqa: E501

from ansible_collections.infoblox.universal_ddi.plugins.module_utils.modules import UniversalDDIAnsibleModule

try:
    from ipam import AddressBlockApi, RangeApi, SubnetApi
    from universal_ddi_client import ApiException
except ImportError:
    pass  # Handled by UniversalDDIAnsibleModule


class NextAvailableIPInfoModule(UniversalDDIAnsibleModule):
    def __init__(self, *args, **kwargs):
        super(NextAvailableIPInfoModule, self).__init__(*args, **kwargs)
        self._existing = None
        self._limit = 1000

    def find(self):
        all_results = []
        offset = 0

        while True:
            try:
                id = self.params["id"]
                address_str = id.rsplit("/", 1)[0]
                if address_str == "ipam/address_block":
                    resp = AddressBlockApi(self.client).list_next_available_ip(
                        id=id, contiguous=self.params["contiguous"], count=self.params["count"]
                    )
                elif address_str == "ipam/subnet":
                    resp = SubnetApi(self.client).list_next_available_ip(
                        id=id, contiguous=self.params["contiguous"], count=self.params["count"]
                    )
                elif address_str == "ipam/range":
                    resp = RangeApi(self.client).list_next_available_ip(
                        id=id, contiguous=self.params["contiguous"], count=self.params["count"]
                    )

                all_results.extend(resp.results)

                if len(resp.results) < self._limit:
                    break
                offset += self._limit

            except ApiException as e:
                self.fail_json(msg=f"Failed to execute command: {e.status} {e.reason} {e.body}")

        return all_results

    def find_next_available_ip(self, id=None, resource_type=None, count=None):
        try:
            if resource_type == "address_block" or "ipam/address_block" in id:
                resp = AddressBlockApi(self.client).list_next_available_ip(
                    id=id, contiguous=self.params["contiguous"], count=count
                )
            elif resource_type == "subnet" or "ipam/subnet" in id:
                resp = SubnetApi(self.client).list_next_available_ip(
                    id=id, contiguous=self.params["contiguous"], count=count
                )
            elif resource_type == "range" or "ipam/range" in id:
                resp = RangeApi(self.client).list_next_available_ip(
                    id=id, contiguous=self.params["contiguous"], count=count
                )
            return resp.results
        except ApiException:
            return None

    def find_resources_by_tags(self, resource_type):
        tag_filter_str = None
        if self.params["tag_filters"]:
            tag_filter_str = " and ".join([f"{k}=='{v}'" for k, v in self.params["tag_filters"].items()])

        offset = 0
        all_resources = []

        while True:
            try:
                if resource_type == "address_block":
                    resp = AddressBlockApi(self.client).list(
                        offset=offset, limit=self._limit, tfilter=tag_filter_str, inherit="full"
                    )
                elif resource_type == "subnet":
                    resp = SubnetApi(self.client).list(
                        offset=offset, limit=self._limit, tfilter=tag_filter_str, inherit="full"
                    )
                elif resource_type == "range":
                    resp = RangeApi(self.client).list(
                        offset=offset, limit=self._limit, tfilter=tag_filter_str, inherit="full"
                    )

                all_resources.extend(resp.results)

                if len(resp.results) < self._limit:
                    break
                offset += self._limit

            except ApiException as e:
                self.fail_json(msg=f"Failed to execute command: {e.status} {e.reason} {e.body}")

        return all_resources

    def run_command(self):
        result = dict(objects=[])

        if self.check_mode:
            self.exit_json(**result)

        # Validate count is within allowed range
        if not 1 <= self.params["count"] <= 20:
            self.fail_json(msg="count must be between 1 and 20")

        if self.params["tag_filters"]:
            if not self.params["resource_type"]:
                self.fail_json(msg="resource_type is required when using tag_filters")

            resource_type = self.params["resource_type"]
            resources = self.find_resources_by_tags(resource_type)

            if not resources:
                self.fail_json(msg=f"No {resource_type}s found with the given tags.")

            find_results = []
            for ab in resources:
                remaining_count = self.params["count"] - len(find_results)

                while len(find_results) < self.params["count"]:
                    find_result = self.find_next_available_ip(
                        id=ab.id, resource_type=self.params["resource_type"], count=remaining_count
                    )

                    if find_result:
                        find_results.extend(find_result)
                        break
                    else:
                        remaining_count -= 1
                        if not remaining_count:
                            break

            if len(find_results) < self.params["count"]:
                self.fail_json(msg=f"Not enough available IPs found in {resource_type}s with the given tags.")
        else:
            find_results = self.find()

        result["objects"] = [r.address for r in find_results]
        self.exit_json(**result)


def main():
    # define available arguments/parameters a user can pass to the module
    module_args = dict(
        id=dict(type="str", required=False),
        contiguous=dict(type="bool", required=False, default=False),
        count=dict(type="int", required=False, default=1),
        tag_filters=dict(type="dict", required=False),
        resource_type=dict(type="str", required=False, choices=["address_block", "subnet", "range"]),
    )

    module = NextAvailableIPInfoModule(
        argument_spec=module_args,
        supports_check_mode=True,
        required_one_of=[["id", "tag_filters"]],
        mutually_exclusive=[["id", "tag_filters"]],
        required_by={"tag_filters": ["resource_type"]},
    )
    module.run_command()


if __name__ == "__main__":
    main()
