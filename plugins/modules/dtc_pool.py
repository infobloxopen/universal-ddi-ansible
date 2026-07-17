#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: Infoblox Inc.
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: dtc_pool
short_description: Manages a DTC Pool
description:
    - Manages a DTC Pool.
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
            - "Optional. Comment for B(Pool)."
        type: str
    disabled:
        description:
            - "Optional. Flag which enables/disables B(Pool)."
            - "Defaults to I(false)."
        type: bool
        default: false
    health_checks:
        description:
            - "Optional. List of B(HealthCheck) objects IDs assigned to B(Pool)."
            - "Defaults to I(empty)."
        type: list
        elements: dict
        suboptions:
            health_check_id:
                description:
                    - "The resource identifier."
                type: str
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
                        choices:
                            - inherit
                            - override
                        default: inherit
                        type: str
    method:
        description:
            - "Load balancing method used for selecting B(Server) assigned to B(Pool)."
            - "Valid values are:"
            - "* I(round_robin) If the I(round_robin) load balancing method is selected, BloxOne DDI adjusts the response to a query in a sequential and circular manner, directing clients to pools."
            - "* I(ratio) If I(ratio) load balancing method is selected, BloxOne DDI adjusts the response to a query so that clients are directed to pool using weighted round robin, a load-balancing pattern in which requests are distributed among several resources based on weight assigned to each resource. The distribution of responses over time will be equal for all available pools but the sequence of the responses won't be guaranteed. When equal weights are assigned for resources (pools) it effectively leads to basic round robin which directs clients to pools in sequential and circular manner."
            - "* I(global_availability) If I(global_availability) load balancing method is selected clients are directed to the first server that is up in the I(servers) list."
        choices:
            - round_robin
            - ratio
            - global_availability
        type: str
        required: true
    name:
        description:
            - "Display name of B(Pool)."
        type: str
        required: true
    pool_availability:
        description:
            - "Optional. Pool Availability setting defines how B(Pool) health is calculated."
            - "Valid values are:"
            - "* I(all) If I(all) availability selected then B(Pool) is treated healthy when all pool's servers are healthy."
            - "* I(quorum) If I(quorum) availability selected then B(Pool) is treated healthy when at least N pool's servers are healthy. N is configurable via the value from I(pool_servers_quorum) setting."
            - "* I(any) If I(any) availability selected then B(Pool) is treated healthy when at least one pool's server is healthy."
        choices:
            - all
            - quorum
            - any
        default: any
        type: str
    pool_servers_quorum:
        description:
            - "Pool Servers Quorum defines a minimal number of pool's healthy servers required for treating B(Pool) as healthy when Pool Availability is set to I(quorum)."
        type: int
    server_availability:
        description:
            - "Optional. Server Availability setting defines how B(Server) health is calculated."
            - "Valid values are:"
            - "* I(all) If I(all) availability selected then B(Server) is treated healthy when all pool's health checks are positive."
            - "* I(quorum) If I(quorum) availability selected then B(Server) is treated healthy when at least N pool's health checks are positive. N is configurable via the value from I(server_health_checks_quorum) setting."
            - "* I(any) If I(any) availability selected then B(Server) is treated healthy when at least one pool's health check is positive"
        choices:
            - all
            - quorum
            - any
        type: str
        default: all
    server_health_checks_quorum:
        description:
            - "Server Health Checks Quorum defines a minimal number of pool's positive health checks required for treating B(Server) as healthy when Server Availability is set to I(quorum)."
        type: int
    servers:
        description:
            - "Optional. List of B(Server) objects assigned to B(Pool)."
            - "Defaults to I(empty)."
        type: list
        elements: dict
        suboptions:
            server_id:
                description:
                    - "The resource identifier."
                type: str
            weight:
                description:
                    - "Weight of B(Server) to be used for load balancing. Unsigned integer, min 1; max 65535."
                type: int
    tags:
        description:
            - "Optional. The tags for B(Pool) in JSON format."
        type: dict
    ttl:
        description:
            - "Optional. Time to live value (in seconds) to be used for records in DTC response. Unsigned integer, min: 0, max 2147483647 (31-bits per RFC-2181)."
        type: int

extends_documentation_fragment:
    - infoblox.universal_ddi.common
"""  # noqa: E501

EXAMPLES = r"""
    - name: "Create a DTC Server (required as parent)"
      infoblox.universal_ddi.dtc_server:
        name: "example_dtc_server"
        address: "10.0.0.0"
        state: present
      register: dtc_server
      
    - name: "Create a TCP Health Check (required as parent)"
      infoblox.universal_ddi.dtc_health_check_tcp:
        name: "example_tcp_health_check"
        port: 80
        state: present
      register: health_check_tcp
    
    - name: "Create an ICMP Health Check (required as parent)"
      infoblox.universal_ddi.dtc_health_check_icmp:
        name: "example_icmp_health_check"
        state: present
      register: health_check_icmp
    
    - name: "Create a DTC Pool"
      infoblox.universal_ddi.dtc_pool:
        name: "example_dtc_pool"
        method: "round_robin"  
        state: present 
      register: dtc_pool
    
    - name: "Create a DTC Pool with Additional Fields"
      infoblox.universal_ddi.dtc_pool:
        name: "example_dtc_pool2"
        method: "ratio" 
        comment: "Example DTC Pool"
        health_checks:
          - health_check_id: "{{ health_check_tcp.id }}"
          - health_check_id: "{{ health_check_icmp.id }}"
        servers:
          - server_id: "{{ dtc_server.id }}"
            weight: 10
        pool_availability: "quorum"
        pool_servers_quorum: 1
        server_availability: "quorum"
        server_health_checks_quorum: 2
        tags:
            location: "site-1"
        ttl: 4800
        state: present
    
    - name: "Delete a DTC Pool"
      infoblox.universal_ddi.dtc_pool:
        name: "example_dtc_pool"
        method: "round_robin"
        state: absent

"""  # noqa: E501

RETURN = r"""
id:
    description:
        - ID of the Pool object
    type: str
    returned: Always
item:
    description:
        - Pool object
    type: complex
    returned: Always
    contains:
        comment:
            description:
                - "Optional. Comment for B(Pool)."
            type: str
            returned: Always
        disabled:
            description:
                - "Optional. Flag which enables/disables B(Pool)."
                - "Defaults to I(false)."
            type: bool
            returned: Always
        health_checks:
            description:
                - "Optional. List of B(HealthCheck) objects IDs assigned to B(Pool)."
                - "Defaults to I(empty)."
            type: list
            returned: Always
            elements: dict
            contains:
                health_check_id:
                    description:
                        - "The resource identifier."
                    type: str
                    returned: Always
                name:
                    description:
                        - "Display name of B(HealthCheck)."
                    type: str
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
                - "Output only. B(Pool) metadata. Defaults to empty object and should be explicitly requested using field selection."
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
                - "Load balancing method used for selecting B(Server) assigned to B(Pool)."
                - "Valid values are:"
                - "* I(round_robin) If the I(round_robin) load balancing method is selected, BloxOne DDI adjusts the response to a query in a sequential and circular manner, directing clients to pools."
                - "* I(ratio) If I(ratio) load balancing method is selected, BloxOne DDI adjusts the response to a query so that clients are directed to pool using weighted round robin, a load-balancing pattern in which requests are distributed among several resources based on weight assigned to each resource. The distribution of responses over time will be equal for all available pools but the sequence of the responses won't be guaranteed. When equal weights are assigned for resources (pools) it effectively leads to basic round robin which directs clients to pools in sequential and circular manner."
                - "* I(global_availability) If I(global_availability) load balancing method is selected clients are directed to the first server that is up in the I(servers) list."
                - "Defaults to I(round_robin)."
            type: str
            returned: Always
        name:
            description:
                - "Display name of B(Pool)."
            type: str
            returned: Always
        pool_availability:
            description:
                - "Optional. Pool Availability setting defines how B(Pool) health is calculated."
                - "Valid values are:"
                - "* I(all) If I(all) availability selected then B(Pool) is treated healthy when all pool's servers are healthy."
                - "* I(quorum) If I(quorum) availability selected then B(Pool) is treated healthy when at least N pool's servers are healthy. N is configurable via the value from I(pool_servers_quorum) setting."
                - "* I(any) If I(any) availability selected then B(Pool) is treated healthy when at least one pool's server is healthy."
                - "Defaults to I(any)."
            type: str
            returned: Always
        pool_servers_quorum:
            description:
                - "Pool Servers Quorum defines a minimal number of pool's healthy servers required for treating B(Pool) as healthy when Pool Availability is set to I(quorum)."
            type: int
            returned: Always
        server_availability:
            description:
                - "Optional. Server Availability setting defines how B(Server) health is calculated."
                - "Valid values are:"
                - "* I(all) If I(all) availability selected then B(Server) is treated healthy when all pool's health checks are positive."
                - "* I(quorum) If I(quorum) availability selected then B(Server) is treated healthy when at least N pool's health checks are positive. N is configurable via the value from I(server_health_checks_quorum) setting."
                - "* I(any) If I(any) availability selected then B(Server) is treated healthy when at least one pool's health check is positive"
                - "Defaults to I(all)."
            type: str
            returned: Always
        server_health_checks_quorum:
            description:
                - "Server Health Checks Quorum defines a minimal number of pool's positive health checks required for treating B(Server) as healthy when Server Availability is set to I(quorum)."
            type: int
            returned: Always
        servers:
            description:
                - "Optional. List of B(Server) objects assigned to B(Pool)."
                - "Defaults to I(empty)."
            type: list
            returned: Always
            elements: dict
            contains:
                name:
                    description:
                        - "Display name of B(Server)."
                    type: str
                    returned: Always
                server_id:
                    description:
                        - "The resource identifier."
                    type: str
                    returned: Always
                weight:
                    description:
                        - "Weight of B(Server) to be used for load balancing. Unsigned integer, min 1; max 65535."
                    type: int
                    returned: Always
        tags:
            description:
                - "Optional. The tags for B(Pool) in JSON format."
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
    from dtc import Pool, PoolApi
    from universal_ddi_client import ApiException, NotFoundException
except ImportError:
    pass  # Handled by UniversalDDIAnsibleModule


class PoolModule(UniversalDDIAnsibleModule):
    def __init__(self, *args, **kwargs):
        super(PoolModule, self).__init__(*args, **kwargs)

        exclude = ["state", "csp_url", "api_key", "portal_url", "portal_key", "id"]
        self._payload_params = {k: v for k, v in self.params.items() if v is not None and k not in exclude}
        self._payload = Pool.from_dict(self._payload_params)
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
                resp = PoolApi(self.client).read(self.params["id"], inherit="full")
                return resp.result
            except NotFoundException as e:
                if self.params["state"] == "absent":
                    return None
                raise e
        else:
            filter = f"name=='{self.params['name']}'"
            resp = PoolApi(self.client).list(filter=filter, inherit="full")

            # If no results, set results to empty list
            if not resp.results:
                resp.results = []

            if len(resp.results) == 1:
                return resp.results[0]
            if len(resp.results) > 1:
                self.fail_json(msg=f"Found multiple Pool: {resp.results}")
            if len(resp.results) == 0:
                return None

    def create(self):
        if self.check_mode:
            return None

        resp = PoolApi(self.client).create(body=self.payload, inherit="full")
        return resp.result.model_dump(by_alias=True, exclude_none=True)

    def update(self):
        if self.check_mode:
            return None

        resp = PoolApi(self.client).update(id=self.existing.id, body=self.payload, inherit="full")
        return resp.result.model_dump(by_alias=True, exclude_none=True)

    def delete(self):
        if self.check_mode:
            return

        PoolApi(self.client).delete(self.existing.id)

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
                result["msg"] = "Pool created"
            elif self.params["state"] == "present" and self.existing is not None:
                if self.payload_changed():
                    item = self.update()
                    result["changed"] = True
                    result["msg"] = "Pool updated"
            elif self.params["state"] == "absent" and self.existing is not None:
                self.delete()
                result["changed"] = True
                result["msg"] = "Pool deleted"

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
        health_checks=dict(
            type="list",
            elements="dict",
            options=dict(
                health_check_id=dict(type="str"),
            ),
        ),
        inheritance_sources=dict(
            type="dict",
            options=dict(
                ttl=dict(
                    type="dict",
                    options=dict(
                        action=dict(type="str", choices=["inherit", "override"], default="inherit"),
                    ),
                ),
            ),
        ),
        method=dict(type="str", required=True, choices=["round_robin", "ratio", "global_availability"]),
        name=dict(type="str", required=True),
        pool_availability=dict(type="str", choices=["all", "quorum", "any"], default="any"),
        pool_servers_quorum=dict(type="int"),
        server_availability=dict(type="str", choices=["all", "quorum", "any"], default="all"),
        server_health_checks_quorum=dict(type="int"),
        servers=dict(
            type="list",
            elements="dict",
            options=dict(
                server_id=dict(type="str"),
                weight=dict(type="int"),
            ),
        ),
        tags=dict(type="dict"),
        ttl=dict(type="int"),
    )

    module = PoolModule(
        argument_spec=module_args,
        supports_check_mode=True,
        required_if=[("state", "present", ["name", "method"])],
    )

    module.run_command()


if __name__ == "__main__":
    main()
