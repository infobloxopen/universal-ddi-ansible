#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: Infoblox Inc.
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: dhcp_ha_group
short_description: Manages an HA Group.
description:
    -  Manages an HA Group.
    -  The HA Group object represents on-prem hosts that can serve the same leases for HA.
version_added: 1.1.0
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
    anycast_config_id:
        description:
            - "The resource identifier."
        type: str
    comment:
        description:
            - "The description for the HA group. May contain 0 to 1024 characters. Can include UTF-8."
        type: str
    hosts:
        description:
            - "The list of hosts."
        type: list
        elements: dict
        required: true
        suboptions:
            address:
                description:
                    - "The address on which this host listens."
                type: str
            heartbeats:
                description:
                    - "Last successful heartbeat received from its peer/s. This field is set when the I(collect_stats) is set to I(true) in the I(GET) I(/dhcp/ha_group) request."
                type: list
                elements: dict
                suboptions:
                    peer:
                        description:
                            - "The name of the peer."
                        type: str
                    successful_heartbeat:
                        description:
                            - "The timestamp as a string of the last successful heartbeat received from the peer above."
                        type: str
                    successful_heartbeat_v6:
                        description:
                            - "The timestamp as a string of the last successful DHCPv6 heartbeat received from the peer above."
                        type: str
            host:
                description:
                    - "The resource identifier."
                type: str
            role:
                description:
                    - "The role of this host in the HA relationship: I(active) or I(passive)."
                type: str
    ip_space:
        description:
            - "The resource identifier."
        type: str
    mode:
        description:
            - "The mode of the HA group."
        type: str
        choices:
            - active-active
            - active-passive
            - advanced-active-passive
            - anycast
        default: active-active
    name:
        description:
            - "The name of the HA group. Must contain 1 to 256 characters. Can include UTF-8."
        type: str
        required: true 
    status:
        description:
            - "Status of the HA group. This field is set when the I(collect_stats) is set to I(true) in the I(GET) I(/dhcp/ha_group) request."
        type: str
    status_v6:
        description:
            - "Status of the DHCPv6 HA group. This field is set when the I(collect_stats) is set to I(true) in the I(GET) I(/dhcp/ha_group) request."
        type: str
    tags:
        description:
            - "The tags for the HA group."
        type: dict

extends_documentation_fragment:
    - infoblox.universal_ddi.common
"""  # noqa: E501

EXAMPLES = r"""
    - name: Get DHCP Host 1 information by filters (required as parent)
      infoblox.universal_ddi.dhcp_host_info:
        filters:
          name: "Host1"
      register: host_1

    - name: Get DHCP Host 2 information by filters (required as parent)
      infoblox.universal_ddi.dhcp_host_info:
        filters:
          name: "Host2"
      register: host_2
      
    - name: Create DHCP HA Group
      infoblox.universal_ddi.dhcp_ha_group:
        name: "example_ha_group"
        mode: "active-active"
        hosts:
          - host: "{{ host_1.id }}"
            role: "active"
          - host: "{{ host_2.id }}"
            role: "active"
        state: present
      
    - name: "Delete DHCP HA Group"
      infoblox.universal_ddi.dhcp_ha_group:
        name: "example_ha_group"
        hosts:
          - host: "{{ host_1.id }}"
            role: "active"
          - host: "{{ host_2.id }}"
            role: "active"
        state: absent
"""  # noqa: E501

RETURN = r"""
id:
    description:
        - ID of the HA Group object
    type: str
    returned: Always
item:
    description:
        - HA Group object
    type: complex
    returned: Always
    contains:
        anycast_config_id:
            description:
                - "The resource identifier."
            type: str
            returned: Always
        comment:
            description:
                - "The description for the HA group. May contain 0 to 1024 characters. Can include UTF-8."
            type: str
            returned: Always
        created_at:
            description:
                - "Time when the object has been created."
            type: str
            returned: Always
        hosts:
            description:
                - "The list of hosts."
            type: list
            returned: Always
            elements: dict
            contains:
                address:
                    description:
                        - "The address on which this host listens."
                    type: str
                    returned: Always
                heartbeats:
                    description:
                        - "Last successful heartbeat received from its peer/s. This field is set when the I(collect_stats) is set to I(true) in the I(GET) I(/dhcp/ha_group) request."
                    type: list
                    returned: Always
                    elements: dict
                    contains:
                        peer:
                            description:
                                - "The name of the peer."
                            type: str
                            returned: Always
                        successful_heartbeat:
                            description:
                                - "The timestamp as a string of the last successful heartbeat received from the peer above."
                            type: str
                            returned: Always
                        successful_heartbeat_v6:
                            description:
                                - "The timestamp as a string of the last successful DHCPv6 heartbeat received from the peer above."
                            type: str
                            returned: Always
                host:
                    description:
                        - "The resource identifier."
                    type: str
                    returned: Always
                port:
                    description:
                        - "The HA port."
                    type: int
                    returned: Always
                port_v6:
                    description:
                        - "The HA port used for IPv6 communication."
                    type: int
                    returned: Always
                role:
                    description:
                        - "The role of this host in the HA relationship: I(active) or I(passive)."
                    type: str
                    returned: Always
                state:
                    description:
                        - "The state of DHCP on the host. This field is set when the I(collect_stats) is set to I(true) in the I(GET) I(/dhcp/ha_group) request."
                    type: str
                    returned: Always
                state_v6:
                    description:
                        - "The state of DHCPv6 on the host. This field is set when the I(collect_stats) is set to I(true) in the I(GET) I(/dhcp/ha_group) request."
                    type: str
                    returned: Always
        id:
            description:
                - "The resource identifier."
            type: str
            returned: Always
        ip_space:
            description:
                - "The resource identifier."
            type: str
            returned: Always
        mode:
            description:
                - "The mode of the HA group."
            type: str
            returned: Always
        name:
            description:
                - "The name of the HA group. Must contain 1 to 256 characters. Can include UTF-8."
            type: str
            returned: Always
        status:
            description:
                - "Status of the HA group. This field is set when the I(collect_stats) is set to I(true) in the I(GET) I(/dhcp/ha_group) request."
            type: str
            returned: Always
        status_v6:
            description:
                - "Status of the DHCPv6 HA group. This field is set when the I(collect_stats) is set to I(true) in the I(GET) I(/dhcp/ha_group) request."
            type: str
            returned: Always
        tags:
            description:
                - "The tags for the HA group."
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
    from ipam import HAGroup, HaGroupApi
    from universal_ddi_client import ApiException, NotFoundException
except ImportError:
    pass  # Handled by UniversalDDIAnsibleModule


class HaGroupModule(UniversalDDIAnsibleModule):
    def __init__(self, *args, **kwargs):
        super(HaGroupModule, self).__init__(*args, **kwargs)

        exclude = ["state", "csp_url", "api_key", "portal_url", "portal_key", "id"]
        self._payload_params = {k: v for k, v in self.params.items() if v is not None and k not in exclude}
        self._payload = HAGroup.from_dict(self._payload_params)
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
                resp = HaGroupApi(self.client).read(self.params["id"])
                return resp.result
            except NotFoundException as e:
                if self.params["state"] == "absent":
                    return None
                raise e
        else:
            filter = f"name=='{self.params['name']}'"
            resp = HaGroupApi(self.client).list(filter=filter)

            # If no results, set results to empty list
            if not resp.results:
                resp.results = []

            if len(resp.results) == 1:
                return resp.results[0]
            if len(resp.results) > 1:
                self.fail_json(msg=f"Found multiple Ha Group: {resp.results}")
            if len(resp.results) == 0:
                return None

    def create(self):
        if self.check_mode:
            return None

        resp = HaGroupApi(self.client).create(body=self.payload)
        return resp.result.model_dump(by_alias=True, exclude_none=True)

    def update(self):
        if self.check_mode:
            return None

        resp = HaGroupApi(self.client).update(id=self.existing.id, body=self.payload)
        return resp.result.model_dump(by_alias=True, exclude_none=True)

    def delete(self):
        if self.check_mode:
            return

        HaGroupApi(self.client).delete(self.existing.id)

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
                result["msg"] = "Ha Group created"
            elif self.params["state"] == "present" and self.existing is not None:
                if self.payload_changed():
                    item = self.update()
                    result["changed"] = True
                    result["msg"] = "Ha Group updated"
            elif self.params["state"] == "absent" and self.existing is not None:
                self.delete()
                result["changed"] = True
                result["msg"] = "Ha Group deleted"

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
        anycast_config_id=dict(type="str"),
        comment=dict(type="str"),
        hosts=dict(
            type="list",
            elements="dict",
            required=True,
            options=dict(
                address=dict(type="str"),
                heartbeats=dict(
                    type="list",
                    elements="dict",
                    options=dict(
                        peer=dict(type="str"),
                        successful_heartbeat=dict(type="str"),
                        successful_heartbeat_v6=dict(type="str"),
                    ),
                ),
                host=dict(type="str"),
                role=dict(type="str"),
            ),
        ),
        ip_space=dict(type="str"),
        mode=dict(
            type="str",
            choices=["active-active", "active-passive", "advanced-active-passive", "anycast"],
            default="active-active",
        ),
        name=dict(type="str", required=True),
        status=dict(type="str"),
        status_v6=dict(type="str"),
        tags=dict(type="dict"),
    )

    module = HaGroupModule(
        argument_spec=module_args,
        supports_check_mode=True,
        required_if=[("state", "present", ["name", "hosts"])],
    )

    module.run_command()


if __name__ == "__main__":
    main()
