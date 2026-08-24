#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: Infoblox Inc.
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: ipam_next_available_subnet_info
short_description: Retrieves the Next available subnet.
description:
    - Retrieves the Next Available Subnet in the specified Address Block.
version_added: 1.0.0
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
            - Number of address blocks to generate. Default 1 if not set. Maximum 20.
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

    - name: "Create an Address Block with tags (required as parent for filtering via tags)"
      infoblox.universal_ddi.ipam_address_block:
        address: "192.168.0.0/16"
        space: "{{ ip_space.id }}"
        tags:
          environment: "production"
          location: "site-1"
        state: "present"

    - name: "Get information about the Subnet"
      infoblox.universal_ddi.ipam_next_available_subnet_info:
        id: "{{ address_block.id }}"
        cidr: 24

    - name: "Get information about the Subnet with count"
      infoblox.universal_ddi.ipam_next_available_subnet_info:
        id: "{{ address_block.id }}"
        cidr: 24
        count: 5

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
    import json
    import re

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
        if (self.params["count"] is not None) and (self.params["count"] <= 0 or self.params["count"] > 20):
            self.fail_json(msg="Parameter 'count' must be between 1 and 20")

    def find_subnet(self, id=None, count=None):
        try:
            resp = AddressBlockApi(self.client).list_next_available_subnet(id=id, cidr=self.params["cidr"], count=count)
            return resp.results
        except ApiException as e:
            # If it's a "fewer than requested" error, extract available count
            if e.status == 400:
                available_count = self.extract_available_count_from_error(e.body)
                return available_count
            return None

    def extract_available_count_from_error(self, error_body):
        """
        Extract the available count from an API error message.

        This function parses the error response when the API returns an error about
        having fewer available networks than requested.

        :param error_body: The error response body from the API
        :return: The number of available networks (int), or 0 if the count couldn't be extracted
        """
        available_count = 0
        try:
            # Parse the JSON error body
            error_json = json.loads(error_body)
            if "error" in error_json and len(error_json["error"]) > 0:
                error_message = error_json["error"][0]["message"]

                # Use regex to extract the number after "The available networks are: "
                match = re.search(r"The available networks are: (\d+)", error_message)
                if match:
                    available_count = int(match.group(1))
                else:
                    # If regex fails send fail message
                    self.fail_json(msg=f"{error_message}")

        except (json.JSONDecodeError, KeyError, IndexError, ValueError) as parse_error:
            self.fail_json(msg="Failed to parse error body: {parse_error}")

        return available_count

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

        if self.params["tag_filters"]:
            address_blocks = self.find_address_blocks_by_tags(self.params["tag_filters"])
            if not address_blocks:
                self.fail_json(msg="No address block found with the given tags.")

            find_results = []
            for ab in address_blocks:
                if len(find_results) >= count:
                    break

                remaining_count = count - len(find_results)

                # Skip address blocks where parent CIDR is equal to or larger than the requested one and continue searching other valid address blocks
                if ab.cidr >= self.params["cidr"]:
                    continue

                find_result = self.find_subnet(id=ab.id, count=remaining_count)

                if isinstance(find_result, int):
                    # We got back an available count from error parsing
                    if find_result == 0:
                        # No addresses available in this block
                        continue
                    elif find_result < remaining_count:
                        # We got fewer than requested, so we need to adjust the count
                        # and try to find more subnets
                        find_results.extend(self.find_subnet(id=ab.id, count=find_result))

                elif find_result:
                    # We got the requested results
                    find_results.extend(find_result)

            if len(find_results) == 0:
                self.fail_json(msg="No subnets available with the given tags and CIDR.")
            # Add warning if we couldn't find all requested address blocks
            if len(find_results) < count:
                self.fail_json(msg=f"Requested {count} subnets but only {len(find_results)} were available")
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
