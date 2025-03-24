#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: Infoblox Inc.
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: anycast_config
short_description: Manages Anycast Configuration.
description:
    - Manages Anycast Configuration.
    - Anycast configuration comprises common anycast configuration data that is defined in support of one service on a set of on-prem hosts.
version_added: 1.0.0
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
    anycast_ip_address:
        description: 
            - "IPv4 address of the anycast host in string format."
        type: str
    anycast_ipv6_address:
        description: 
            - "IPv6 address of the anycast host in string format."
        type: str
    description:
        description:
            - "The description for the address object."
            - "May contain 0 to 1024 characters."
            - "Can include UTF-8."
        type: str
    name:
        description: 
            - "The name of the anycast configuration."
        type: str
    onprem_hosts:
        description: 
            - "The list of on-prem hosts associated with the anycast configuration."
            - "Struct on-prem host reference."
        suboptions:
            ip_address:
                description:
                    - "IPv4 address of the host in string format"
                    - "example: 11.83.17.55"
                type: str
            ipv6_address:
                description:
                    - "IPv6 address of the host in string format"
                    - "example: ::1"
                type: str
            name:
                description:
                    - "A user friendly name of the host would be, example 'DNS HOST 1', 'Central Office Server'"
                type: str
        type: list
        elements: dict
    service:
        description: 
            - "The type of the Service used in anycast configuration, supports (dns, dhcp, dfp)."
        type: str
    tags:
        description: 
            - "The tags for the anycast configuration object."
        type: dict

extends_documentation_fragment:
    - infoblox.universal_ddi.common
"""  # noqa: E501

EXAMPLES = r"""
    - name: Create Anycast Configuration
      infoblox.universal_ddi.anycast_config:
          name: "example_anycast_config"
          anycast_ip_address: "40.0.0.0"
          service: "DNS"
          state: "present"

    - name: Create Anycast Configuration with Additional Fields
      infoblox.universal_ddi.anycast_config:
          name: "example_anycast_config"
          anycast_ip_address: "40.0.0.0"
          service: "DNS"
          description: "Anycast Configuration for DNS"
          tags:
            location: "site-1"
          state: "present"

    - name: Delete Anycast Configuration
      infoblox.universal_ddi.anycast_config:
          name: "example_anycast_config"
          anycast_ip_address: "40.0.0.0"
          service: "DNS"
          state: "absent"
"""

RETURN = r"""
id:
    description:
        - ID of the Anycast Config object
    type: str
    returned: Always
objects:
    description:
        - Anycast Config object
    type: list
    elements: dict
    returned: Always
    contains:
        account_id:
            description: 
                - "The account identifier."
            type: int
            returned: Always
        anycast_ip_address:
            description: 
                - "IPv4 address of the host in string format."
            type: str
            returned: Always
        anycast_ipv6_address:
            description: 
                - "IPv6 address of the host in string format."
            type: str
            returned: Always
        created_at:
            description: 
                - "Time when the object has been created."
            type: str
            returned: Always
        description:
            description: 
                - "The description for the address object."
                - "May contain 0 to 1024 characters."
                - "Can include UTF-8."
            type: str
            returned: Always
        fields:
            description: 
                - "Field mask represents a set of symbolic field paths"
            type: dict
            returned: Always
            contains:
                paths:
                    description:
                        - "The set of field mask paths."
                    type: list
                    returned: Always
        id:
            description: 
                - "The resource identifier."
            type: int
            returned: Always
        is_configured:
            description:
                - "Boolean value which determines if service is configured."
            type: bool
            returned: Always
        name:
            description: 
                - "The name of the anycast configuration."
            type: str
            returned: Always
        onprem_hosts:
            description: 
                - "The list of on-prem hosts associated with the anycast configuration."
                - "Struct on-prem host reference."
            type: list
            returned: Always
            elements: dict
            contains:
                id:
                    description: 
                        - "Numeric host identifier"
                    type: int
                    returned: Always
                ip_address:
                    description:
                        - "IPv4 address of the host in string format"
                        - "example: 11.83.17.55"
                    type: str
                    returned: Always
                ipv6_address:
                    description:
                        - "IPv6 address of the host in string format"
                        - "example: ::1"
                    type: str
                    returned: Always
                name:
                    description: 
                        - "A user friendly name of the host would be, example 'DNS HOST 1', 'Central Office Server'"
                    type: str
                    returned: Always
                ophid:
                    description:
                        - "Unique 32-character string identifier assigned to the host"
                        - "example: 8b9ba7b03d05fbb1b31a41d47968dd43"
                    type: str
                    returned: Always
                runtime_status:
                    description: 
                        - "The runtime status of the anycast configuration host example 'Active', 'Inactive', 'Degraded'"
                    type: str
                    returned: Always
        runtime_status:
            description: 
                - "The runtime status of the anycast configuration."
            type: str
            returned: Always
        service:
            description: 
                - "The type of the Service used in anycast configuration, supports (dns, dhcp, dfp)."
            type: str
            returned: Always
        tags:
            description: 
                - "The tags for the anycast configuration object."
            type: dict
            returned: Always
        updated_at:
            description:
                - "Time when the object has been updated. Equals to created_at if not updated after creation."
            type: str
            returned: Always
"""  # noqa: E501

from ansible_collections.infoblox.universal_ddi.plugins.module_utils.modules import UniversalDDIAnsibleModule

try:
    from anycast import AnycastConfig, OnPremAnycastManagerApi
    from universal_ddi_client import ApiException, NotFoundException
except ImportError:
    pass  # Handled by UniversalDDIAnsibleModule


class OnPremAnycastManagerModule(UniversalDDIAnsibleModule):
    def __init__(self, *args, **kwargs):
        super(OnPremAnycastManagerModule, self).__init__(*args, **kwargs)

        exclude = ["state", "csp_url", "api_key", "portal_url", "portal_key", "id"]
        self._payload_params = {k: v for k, v in self.params.items() if v is not None and k not in exclude}
        self._payload = AnycastConfig.from_dict(self._payload_params)
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
                resp = OnPremAnycastManagerApi(self.client).read_anycast_config_with_runtime_status(self.params["id"])
                return resp.result
            except NotFoundException as e:
                if self.params["state"] == "absent":
                    return None
                raise e
        else:
            # Retrieve Anycast configurations filtered by service
            resp = OnPremAnycastManagerApi(self.client).get_anycast_config_list(service=self.params["service"])

            # If no results, set results to empty list
            if not resp.results:
                resp.results = []

            # Filter in memory by name
            matching_configs = [config for config in resp.results if config.name == self.params["name"]]

            if len(matching_configs) == 1:
                return matching_configs[0]
            if len(matching_configs) > 1:
                self.fail_json(
                    msg=f"Found multiple Anycast Configurations for service '{self.params['service']}' with name '{self.params['name']}': {matching_configs}"
                )
            if len(matching_configs) == 0:
                return None

    def create(self):
        if self.check_mode:
            return None

        resp = OnPremAnycastManagerApi(self.client).create_anycast_config(body=self.payload)
        return resp.results.model_dump(by_alias=True, exclude_none=True)

    def update(self):
        if self.check_mode:
            return None

        resp = OnPremAnycastManagerApi(self.client).update_anycast_config(id=self.existing.id, body=self.payload)
        return resp.results.model_dump(by_alias=True, exclude_none=True)

    def delete(self):
        if self.check_mode:
            return

        OnPremAnycastManagerApi(self.client).delete_anycast_config(self.existing.id)

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
                result["msg"] = "Anycast configuration created"
            elif self.params["state"] == "present" and self.existing is not None:
                if self.payload_changed():
                    item = self.update()
                    result["changed"] = True
                    result["msg"] = "Anycast configuration updated"
            elif self.params["state"] == "absent" and self.existing is not None:
                self.delete()
                result["changed"] = True
                result["msg"] = "Anycast configuration deleted"

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
        anycast_ip_address=dict(type="str"),
        anycast_ipv6_address=dict(type="str"),
        description=dict(type="str"),
        name=dict(type="str"),
        onprem_hosts=dict(
            type="list",
            elements="dict",
            options=dict(
                ip_address=dict(type="str"),
                ipv6_address=dict(type="str"),
                name=dict(type="str"),
            ),
        ),
        service=dict(type="str"),
        tags=dict(type="dict"),
    )

    module = OnPremAnycastManagerModule(
        argument_spec=module_args,
        supports_check_mode=True,
        required_if=[("state", "present", ["name", "anycast_ip_address", "service"])],
    )

    module.run_command()


if __name__ == "__main__":
    main()
