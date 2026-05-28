#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: Infoblox Inc.
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: dtc_policy_info
short_description: Manage Policy
description:
    - Manage Policy
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
    inherit:
        description:
            - Return inheritance information
        type: str
        required: false
        choices:
            - full
            - partial
            - none
        default: full
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
    - name: Get DTC Policy information by ID
      infoblox.universal_ddi.dtc_policy_info:
        id: "{{ dtc_policy.id }}"

    - name: Get DTC Policy information by filters
      infoblox.universal_ddi.dtc_policy_info:
        filters:
          name: "example-dtc-policy"

    - name: Get DTC Policy information by filter query
      infoblox.universal_ddi.dtc_policy_info:
        filter_query: "name=='example-dtc-policy'"

    - name: Get DTC Policy information by tag filters
      infoblox.universal_ddi.dtc_policy_info:
        tag_filters:
          location: "site-1"

    - name: Get DTC Policy information by tag filter query
      infoblox.universal_ddi.dtc_policy_info:
        tag_filter_query: "location=='site-1'"
"""

RETURN = r"""
id:
    description:
        - ID of the Policy object
    type: str
    returned: Always
objects:
    description:
        - Policy object
    type: list
    elements: dict
    returned: Always
    contains:
        comment:
            description:
                - "Optional. Comment for B(Policy)."
            type: str
            returned: Always
        disabled:
            description:
                - "Optional. Flag which enables/disables B(Policy)."
                - "Defaults to I(false)."
            type: bool
            returned: Always
        id:
            description:
                - "The resource identifier."
            type: str
            returned: Always
        inheritance_sources:
            description:
                - "Optional. The inheritance configuration."
            type: dict
            returned: Always
            contains:
                ttl:
                    description: ""
                    type: dict
                    returned: Always
                    contains:
                        action:
                            description:
                                - "The inheritance setting for a field."
                                - "Valid values are:"
                                - "* I(inherit): Use the inherited value."
                                - "* I(override): Use the value set in the object."
                                - "Defaults to I(inherit)."
                            type: str
                            returned: Always
                        display_name:
                            description:
                                - "The human-readable display name for the object referred to by I(source)."
                            type: str
                            returned: Always
                        source:
                            description:
                                - "The resource identifier."
                            type: str
                            returned: Always
                        value:
                            description:
                                - "The inherited value."
                            type: int
                            returned: Always
        metadata:
            description:
                - "Output only. B(Policy) metadata. Defaults to empty object and should be explicitly requested using field selection."
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
        method:
            description:
                - "Load balancing method used for selecting B(Pool) assigned to B(Policy)."
                - "Valid values are:"
                - "* I(round_robin) If the I(round_robin) load balancing method is selected, BloxOne DDI adjusts the response to a query in a sequential and circular manner, directing clients to pools."
                - "* I(ratio) If I(ratio) load balancing method is selected, BloxOne DDI adjusts the response to a query so that clients are directed to pool using weighted round robin, a load-balancing pattern in which requests are distributed among several resources based on weight assigned to each resource. The distribution of responses over time will be equal for all available pools but the sequence of the responses won't be guaranteed. When equal weights are assigned for resources (pools) it effectively leads to basic round robin configuration which directs clients to pools in a sequential and circular manner."
                - "* I(topology) If I(topology) load balancing method is selected the pools configured for the policy are ignored and topology rules are used instead."
                - "* I(global_availability) If I(global_availability) load balancing method is selected clients are directed to the first pool that is up in the I(pools) list."
                - "Defaults to I(round_robin)."
            type: str
            returned: Always
        name:
            description:
                - "Display name of B(Policy)."
            type: str
            returned: Always
        pools:
            description:
                - "Optional. List of B(Pool) objects assigned to B(Policy)."
                - "Defaults to I(empty)."
            type: list
            returned: Always
            elements: dict
            contains:
                name:
                    description:
                        - "Display name of B(Pool)."
                    type: str
                    returned: Always
                pool_id:
                    description:
                        - "The resource identifier."
                    type: str
                    returned: Always
                weight:
                    description:
                        - "Weight of B(Pool) to be used for load balancing. Unsigned integer, min 1; max 65535."
                    type: int
                    returned: Always
        rules:
            description:
                - "Optional. List of B(TopologyRule) objects defining the resolving strategy for B(Policy)."
                - "Defaults to a list of single, default B(TopologyRule)."
            type: list
            returned: Always
            elements: dict
            contains:
                code:
                    description:
                        - "Optional. DNS code to return if rule matches. Must be set if I(destination) is set to I(code)."
                        - "Allowed values:"
                        - "- nodata"
                        - "- nxdomain"
                        - "Defaults to I(nodata)."
                    type: str
                    returned: Always
                destination:
                    description:
                        - "Destination of B(TopologyRule)."
                        - "Allowed values:"
                        - "- code"
                        - "- pool"
                        - "Defaults to I(code)."
                    type: str
                    returned: Always
                name:
                    description:
                        - "Display name of B(TopologyRule)."
                    type: str
                    returned: Always
                pool_id:
                    description:
                        - "The resource identifier."
                    type: str
                    returned: Always
                source:
                    description:
                        - "Type of source."
                        - "Allowed values:"
                        - "- subnet"
                        - "- default"
                        - "Defaults to I(default)."
                    type: str
                    returned: Always
                subnets:
                    description:
                        - "Optional. List of subnets in CIDR format."
                        - "Must be set if I(source) is I(subnet), otherwise must be empty."
                    type: list
                    returned: Always
        tags:
            description:
                - "Optional. The tags for B(Policy) in JSON format."
            type: dict
            returned: Always
        ttl:
            description:
                - "Optional. Time to live value (in seconds) to be used for records in DTC response. Unsigned integer, min: 0, max 2147483647 (31-bits per RFC-2181)."
            type: int
            returned: Always
"""  # noqa: E501

from ansible_collections.infoblox.universal_ddi.plugins.module_utils.modules import UniversalDDIAnsibleModule

try:
    from dtc import PolicyApi
    from universal_ddi_client import ApiException, NotFoundException
except ImportError:
    pass  # Handled by UniversalDDIAnsibleModule


class PolicyInfoModule(UniversalDDIAnsibleModule):
    def __init__(self, *args, **kwargs):
        super(PolicyInfoModule, self).__init__(*args, **kwargs)
        self._existing = None
        self._limit = 1000

    def find_by_id(self):
        try:
            resp = PolicyApi(self.client).read(self.params["id"], inherit="full")
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
                resp = PolicyApi(self.client).list(
                    offset=offset, limit=self._limit, filter=filter_str, tfilter=tag_filter_str, inherit="full"
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
        inherit=dict(type="str", required=False, choices=["full", "partial", "none"], default="full"),
        tag_filters=dict(type="dict", required=False),
        tag_filter_query=dict(type="str", required=False),
    )

    module = PolicyInfoModule(
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
