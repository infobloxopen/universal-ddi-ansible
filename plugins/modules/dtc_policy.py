#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: Infoblox Inc.
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: dtc_policy
short_description: Manages a DTC Policy
description:
    - Manages a DTC Policy
version_added: 1.2.0
author: Infoblox Inc. (@infobloxopen)
options:
    id:
        description:
            - ID of the object
        type: str
        required: false
    state:
        description:
            - Indicate desired state of the object
        type: str
        required: false
        choices:
            - present
            - absent
        default: present
    comment:
        description:
            - "Optional. Comment for B(Policy)."
        type: str
    disabled:
        description:
            - "Optional. Flag which enables/disables B(Policy)."
            - "Defaults to I(false)."
        type: bool
        default: false
    inheritance_sources:
        description:
            - "Optional. The inheritance configuration."
        type: dict
        suboptions:
            ttl:
                description: "The inheritance configuration specifies how the object inherits the ttl field."
                type: dict
                suboptions:
                    action:
                        description:
                            - "The inheritance setting for a field."
                            - "Valid values are:"
                            - "* I(inherit): Use the inherited value."
                            - "* I(override): Use the value set in the object."
                            - "Defaults to I(inherit)."
                        type: str
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
        choices:
            - round_robin
            - ratio
            - topology
            - global_availability
        required: true
    name:
        description:
            - "Display name of B(Policy)."
        type: str
        required: true
    pools:
        description:
            - "Optional. List of B(Pool) objects assigned to B(Policy)."
            - "Defaults to I(empty)."
        type: list
        elements: dict
        suboptions:
            pool_id:
                description:
                    - "The resource identifier."
                type: str
            weight:
                description:
                    - "Weight of B(Pool) to be used for load balancing. Unsigned integer, min 1; max 65535."
                type: int
    rules:
        description:
            - "Optional. List of B(TopologyRule) objects defining the resolving strategy for B(Policy)."
            - "Defaults to a list of single, default B(TopologyRule)."
        type: list
        elements: dict
        suboptions:
            code:
                description:
                    - "Optional. DNS code to return if rule matches. Must be set if I(destination) is set to I(code)."
                    - "Allowed values:"
                    - "- nodata"
                    - "- nxdomain"
                    - "Defaults to I(nodata)."
                type: str
                choices:
                    - nodata
                    - nxdomain
            destination:
                description:
                    - "Destination of B(TopologyRule)."
                    - "Allowed values:"
                    - "- code"
                    - "- pool"
                    - "Defaults to I(code)."
                type: str
                choices:
                    - code
                    - pool
            name:
                description:
                    - "Display name of B(TopologyRule)."
                type: str
            pool_id:
                description:
                    - "The resource identifier."
                type: str
            source:
                description:
                    - "Type of source."
                    - "Allowed values:"
                    - "- subnet"
                    - "- default"
                    - "Defaults to I(default)."
                type: str
                choices:
                    - subnet
                    - default
                default: default
            subnets:
                description:
                    - "Optional. List of subnets in CIDR format."
                    - "Must be set if I(source) is I(subnet), otherwise must be empty."
                type: list
                elements: str
    tags:
        description:
            - "Optional. The tags for B(Policy) in JSON format."
        type: dict
    ttl:
        description:
            - "Optional. Time to live value (in seconds) to be used for records in DTC response. Unsigned integer, min: 0, max 2147483647 (31-bits per RFC-2181)."
        type: int

extends_documentation_fragment:
    - infoblox.universal_ddi.common
"""  # noqa: E501

EXAMPLES = r"""
    - name: "Create a DTC Pool (required as parent)"
      infoblox.universal_ddi.dtc_pool:
        name: "example_dtc_pool"
        method: "round_robin"
        state: present
      register: dtc_pool

    - name: "Create a DTC Policy"
      infoblox.universal_ddi.dtc_policy:
        name: "example_dtc_policy"
        method: "ratio"
        state: present
      register: dtc_policy

    - name: "Create a DTC Policy with Additional Fields"
      infoblox.universal_ddi.dtc_policy:
        name: "example_dtc_policy"
        method: "ratio"
        ttl: 300
        pools:
            - pool_id: "{{ dtc_pool.id }}"
              weight: 10
        rules:
            - source: "subnet"
              name: "example_subnet_rule"
              code: "nxdomain"
              subnets:
                - "10.0.0.0/24"
                - "20.0.0.0/24"
        tags:
            location: "site-1"
        state: present

    - name: "Delete the DTC Policy"
      infoblox.universal_ddi.dtc_policy:
        name: "example_dtc_policy"
        method: "ratio"
        state: absent
"""

RETURN = r"""
id:
    description:
        - ID of the Policy object
    type: str
    returned: Always
item:
    description:
        - Policy object
    type: complex
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
                    description: "The inheritance configuration specifies how the object inherits the ttl field."
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
    from dtc import Policy, PolicyApi
    from universal_ddi_client import ApiException, NotFoundException
except ImportError:
    pass  # Handled by UniversalDDIAnsibleModule


class PolicyModule(UniversalDDIAnsibleModule):
    def __init__(self, *args, **kwargs):
        super(PolicyModule, self).__init__(*args, **kwargs)

        exclude = ["state", "csp_url", "api_key", "portal_url", "portal_key", "id"]
        self._payload_params = {k: v for k, v in self.params.items() if v is not None and k not in exclude}
        self._payload = Policy.from_dict(self._payload_params)
        self._existing = None

    @property
    def existing(self):
        return self._existing

    @existing.setter
    def existing(self, value):
        self._existing = value

    @property
    def payload_params(self):
        return self._payload_params

    @property
    def payload(self):
        return self._payload

    def payload_changed(self):
        if self.existing is None:
            # if existing is None, then it is a create operation
            return True

        return self.is_changed(self.existing.model_dump(by_alias=True, exclude_none=True), self.payload_params)

    def find(self):
        if self.params["id"] is not None:
            try:
                resp = PolicyApi(self.client).read(self.params["id"], inherit="full")
                return resp.result
            except NotFoundException as e:
                if self.params["state"] == "absent":
                    return None
                raise e
        else:
            filter = f"name=='{self.params['name']}'"
            resp = PolicyApi(self.client).list(filter=filter, inherit="full")

            # If no results, set results to empty list
            if not resp.results:
                resp.results = []

            if len(resp.results) == 1:
                return resp.results[0]
            if len(resp.results) > 1:
                self.fail_json(msg=f"Found multiple Policy: {resp.results}")
            if len(resp.results) == 0:
                return None

    def create(self):
        if self.check_mode:
            return None

        resp = PolicyApi(self.client).create(body=self.payload, inherit="full")
        return resp.result.model_dump(by_alias=True, exclude_none=True)

    def update(self):
        if self.check_mode:
            return None

        resp = PolicyApi(self.client).update(id=self.existing.id, body=self.payload, inherit="full")
        return resp.result.model_dump(by_alias=True, exclude_none=True)

    def delete(self):
        if self.check_mode:
            return

        PolicyApi(self.client).delete(self.existing.id)

    def run_command(self):
        result = dict(changed=False, object={}, id=None)

        # based on the state that is passed in, we will execute the appropriate
        # functions
        try:
            self.existing = self.find()
            item = {}
            if self.params["state"] == "present" and self.existing is None:
                item = self.create()
                result["changed"] = True
                result["msg"] = "Policy created"
            elif self.params["state"] == "present" and self.existing is not None:
                if self.payload_changed():
                    item = self.update()
                    result["changed"] = True
                    result["msg"] = "Policy updated"
            elif self.params["state"] == "absent" and self.existing is not None:
                self.delete()
                result["changed"] = True
                result["msg"] = "Policy deleted"

            if self.check_mode:
                # if in check mode, do not update the result or the diff, just return the changed state
                self.exit_json(**result)

            result["diff"] = dict(
                before=self.existing.model_dump(by_alias=True, exclude_none=True) if self.existing is not None else {},
                after=item,
            )
            result["object"] = item
            result["id"] = (
                self.existing.id if self.existing is not None else item["id"] if (item and "id" in item) else None
            )
        except ApiException as e:
            self.fail_json(msg=f"Failed to execute command: {e.status} {e.reason} {e.body}")

        self.exit_json(**result)


def main():
    module_args = dict(
        id=dict(type="str", required=False),
        state=dict(type="str", required=False, choices=["present", "absent"], default="present"),
        comment=dict(type="str"),
        disabled=dict(type="bool", default=False),
        inheritance_sources=dict(
            type="dict",
            options=dict(
                ttl=dict(
                    type="dict",
                    options=dict(
                        action=dict(type="str"),
                    ),
                ),
            ),
        ),
        method=dict(type="str", required=True, choices=["round_robin", "ratio", "topology", "global_availability"]),
        name=dict(type="str", required=True),
        pools=dict(
            type="list",
            elements="dict",
            options=dict(
                pool_id=dict(type="str"),
                weight=dict(type="int"),
            ),
        ),
        rules=dict(
            type="list",
            elements="dict",
            options=dict(
                code=dict(type="str", choices=["nodata", "nxdomain"]),
                destination=dict(type="str", choices=["code", "pool"]),
                name=dict(type="str"),
                pool_id=dict(type="str"),
                source=dict(type="str", choices=["subnet", "default"], default="default"),
                subnets=dict(type="list", elements="str"),
            ),
        ),
        tags=dict(type="dict"),
        ttl=dict(type="int"),
    )

    module = PolicyModule(
        argument_spec=module_args,
        supports_check_mode=True,
        required_if=[
            ("state", "present", ["name", "method"]),
        ],
    )

    module.run_command()


if __name__ == "__main__":
    main()
