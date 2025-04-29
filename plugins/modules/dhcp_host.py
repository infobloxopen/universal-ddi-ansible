#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: Infoblox Inc.
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: dhcp_host
short_description: Manages DHCP Hosts
description:
    - Manages DHCP Hosts.
    - A DHCP Host object associates a DHCP Config Profile with an on-prem host.
    - This resource represents an existing backend object that cannot be created or deleted through API calls. Instead, it can only be updated.
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
    ip_space:
        description:
            - "The resource identifier."
        type: str
    server:
        description:
            - "The resource identifier."
        type: str
    tags:
        description:
            - "The tags of the on-prem host in JSON format."
        type: dict

extends_documentation_fragment:
    - infoblox.universal_ddi.common
"""  # noqa: E501

EXAMPLES = r"""
    - name: Retrieve Infra Host Information (required as parent)
      infoblox.universal_ddi.infra_host_info:
        filters:
          display_name: "example_infra_host"
      register: infra_host_info

    - name: Create a DHCP Server (required as parent)
      infoblox.universal_ddi.dhcp_server:
        name: "example_server"
        state: present
      register: server

    - name: Update DHCP Host
      infoblox.universal_ddi.dhcp_host:
        id: "{{ infra_host_info.objects[0].legacy_id }}"
        server: "{{ server.id }}"
        state: present

    - name: "Dissociate DHCP Host"
      infoblox.universal_ddi.dhcp_host:
        id: "{{ infra_host_info.objects[0].legacy_id }}"
        state: "absent"

    - name: Delete the DHCP Server
      infoblox.universal_ddi.dhcp_server:
        name: "example_server_name"
        state: "absent"
"""

RETURN = r"""
id:
    description:
        - ID of the DHCP Host object
    type: str
    returned: Always
item:
    description:
        - DHCP Host object
    type: complex
    returned: Always
    contains:
        address:
            description:
                - "The primary IP address of the on-prem host."
            type: str
            returned: Always
        anycast_addresses:
            description:
                - "Anycast address configured to the host. Order is not significant."
            type: list
            returned: Always
        associated_server:
            description:
                - "The DHCP Config Profile for the on-prem host."
            type: dict
            returned: Always
            contains:
                id:
                    description:
                        - "The resource identifier."
                    type: str
                    returned: Always
                name:
                    description:
                        - "The DHCP Config Profile name."
                    type: str
                    returned: Always
        comment:
            description:
                - "The description for the on-prem host."
            type: str
            returned: Always
        current_version:
            description:
                - "Current dhcp application version of the host."
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
        name:
            description:
                - "The display name of the on-prem host."
            type: str
            returned: Always
        ophid:
            description:
                - "The on-prem host ID."
            type: str
            returned: Always
        provider_id:
            description:
                - "External provider identifier."
            type: str
            returned: Always
        server:
            description:
                - "The resource identifier."
            type: str
            returned: Always
        tags:
            description:
                - "The tags of the on-prem host in JSON format."
            type: dict
            returned: Always
        type:
            description:
                - "Defines the type of host. Allowed values:"
                - "* I(bloxone_ddi): host type is BloxOne DDI,"
                - "* I(microsoft_azure): host type is Microsoft Azure,"
                - "* I(amazon_web_service): host type is Amazon Web Services."
                - "* I(microsoft_active_directory): host type is Microsoft Active Directory."
            type: str
            returned: Always
"""  # noqa: E501

from ansible_collections.infoblox.universal_ddi.plugins.module_utils.modules import UniversalDDIAnsibleModule

try:
    from ipam import DhcpHostApi, Host
    from universal_ddi_client import ApiException, NotFoundException
except ImportError:
    pass  # Handled by UniversalDDIAnsibleModule


class DhcpHostModule(UniversalDDIAnsibleModule):
    def __init__(self, *args, **kwargs):
        super(DhcpHostModule, self).__init__(*args, **kwargs)

        exclude = ["state", "csp_url", "api_key", "portal_url", "portal_key", "id"]
        self._payload_params = {k: v for k, v in self.params.items() if v is not None and k not in exclude}
        self._payload = Host.from_dict(self._payload_params)
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
                # Attempt to read the Host using the provided ID.
                # If the Host is not found and the state is "absent", return None.
                # If the Host is not found and state is not "present", raise the exception.
                resp = DhcpHostApi(self.client).read(self.params["id"])
                return resp.result
            except NotFoundException as e:
                if self.params["state"] == "absent":
                    return None
                raise e
        return None

    def update(self):
        if self.check_mode:
            return None

        resp = DhcpHostApi(self.client).update(id=self.existing.id, body=self.payload)
        return resp.result.model_dump(by_alias=True, exclude_none=True)

    def delete(self):
        if self.check_mode:
            return

        update_body = self.payload
        # Set the server to null to dissociate the host
        setattr(update_body, "server", "")

        resp = DhcpHostApi(self.client).update(id=self.existing.id, body=update_body)
        return resp.result.model_dump(by_alias=True, exclude_none=True)

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
                result["msg"] = "DHCP Host created"
            elif self.params["state"] == "present" and self.existing is not None:
                if self.payload_changed():
                    item = self.update()
                    result["changed"] = True
                    result["msg"] = "DHCP Host updated"
            elif self.params["state"] == "absent" and self.existing is not None:
                self.delete()
                result["changed"] = True
                result["msg"] = "DHCP Host deleted"

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
        ip_space=dict(type="str"),
        server=dict(type="str"),
        tags=dict(type="dict"),
    )

    module = DhcpHostModule(
        argument_spec=module_args,
        supports_check_mode=True,
        required_if=[("state", "present", ["id", "server"])],
    )

    module.run_command()


if __name__ == "__main__":
    main()
