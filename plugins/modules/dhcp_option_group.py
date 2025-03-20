#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: Infoblox Inc.
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: dhcp_option_group
short_description: Manage Option Group
description:
    - Manage Option Group
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
    comment:
        description:
            - "The description for the option group. May contain 0 to 1024 characters. Can include UTF-8."
        type: str
    dhcp_options:
        description:
            - "The list of DHCP options for the option group. May be either a specific option or a group of options."
        type: list
        elements: dict
        suboptions:
            group:
                description:
                    - "The resource identifier."
                type: str
            option_code:
                description:
                    - "The resource identifier."
                type: str
            option_value:
                description:
                    - "The option value."
                type: str
            type:
                description:
                    - "The type of item."
                type: str
                choices:
                    - group
                    - option
    name:
        description:
            - "The name of the option group. Must contain 1 to 256 characters. Can include UTF-8."
        type: str
        required: true
    protocol:
        description:
            - "The type of protocol (I(ip4) or I(ip6))."
        type: str
        choices:
            - ip4
            - ip6
    tags:
        description:
            - "The tags for the option group in JSON format."
        type: dict

extends_documentation_fragment:
    - infoblox.universal_ddi.common
"""  # noqa: E501

EXAMPLES = r"""
    - name: Create a DHCP Option Group
      infoblox.universal_ddi.dhcp_option_group:
        name: "option_group_name"
        state: "present"
      
    - name: Create a DHCP Option Group with additional parameters
      infoblox.universal_ddi.dhcp_option_group:
        name: "option_group_name"
        comment: "This is a  DHCP Option Group"
        dhcp_options:
            - type: "option"
              option_code: 234
              option_value: "False"
        state: "present"
    
    - name: Delete the DHCP Option Group
      infoblox.universal_ddi.dhcp_option_group:
          name: "option_group_name"
          state: "absent"
"""  # noqa: E501

RETURN = r"""
id:
    description:
        - ID of the Option Group object
    type: str
    returned: Always
item:
    description:
        - Option Group object
    type: complex
    returned: Always
    contains:
        comment:
            description:
                - "The description for the option group. May contain 0 to 1024 characters. Can include UTF-8."
            type: str
            returned: Always
        created_at:
            description:
                - "Time when the object has been created."
            type: str
            returned: Always
        dhcp_options:
            description:
                - "The list of DHCP options for the option group. May be either a specific option or a group of options."
            type: list
            returned: Always
            elements: dict
            contains:
                group:
                    description:
                        - "The resource identifier."
                    type: str
                    returned: Always
                option_code:
                    description:
                        - "The resource identifier."
                    type: str
                    returned: Always
                option_value:
                    description:
                        - "The option value."
                    type: str
                    returned: Always
                type:
                    description:
                        - "The type of item."
                        - "Valid values are:"
                        - "* I(group)"
                        - "* I(option)"
                    type: str
                    returned: Always
        id:
            description:
                - "The resource identifier."
            type: str
            returned: Always
        name:
            description:
                - "The name of the option group. Must contain 1 to 256 characters. Can include UTF-8."
            type: str
            returned: Always
        protocol:
            description:
                - "The type of protocol (I(ip4) or I(ip6))."
            type: str
            returned: Always
        tags:
            description:
                - "The tags for the option group in JSON format."
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
    from ipam import OptionGroup, OptionGroupApi
    from universal_ddi_client import ApiException, NotFoundException
except ImportError:
    pass  # Handled by UniversalDDIAnsibleModule


class OptionGroupModule(UniversalDDIAnsibleModule):
    def __init__(self, *args, **kwargs):
        super(OptionGroupModule, self).__init__(*args, **kwargs)

        exclude = ["state", "csp_url", "api_key", "portal_url", "portal_key", "id"]
        self._payload_params = {k: v for k, v in self.params.items() if v is not None and k not in exclude}
        self._payload = OptionGroup.from_dict(self._payload_params)
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
                resp = OptionGroupApi(self.client).read(self.params["id"])
                return resp.result
            except NotFoundException as e:
                if self.params["state"] == "absent":
                    return None
                raise e
        else:
            filter = f"name=='{self.params['name']}'"
            resp = OptionGroupApi(self.client).list(filter=filter)

            # If no results, set results to empty list
            if not resp.results:
                resp.results = []

            if len(resp.results) == 1:
                return resp.results[0]
            if len(resp.results) > 1:
                self.fail_json(msg=f"Found multiple Option Group: {resp.results}")
            if len(resp.results) == 0:
                return None

    def create(self):
        if self.check_mode:
            return None

        resp = OptionGroupApi(self.client).create(body=self.payload)
        return resp.result.model_dump(by_alias=True, exclude_none=True)

    def update(self):
        if self.check_mode:
            return None

        resp = OptionGroupApi(self.client).update(id=self.existing.id, body=self.payload)
        return resp.result.model_dump(by_alias=True, exclude_none=True)

    def delete(self):
        if self.check_mode:
            return

        OptionGroupApi(self.client).delete(self.existing.id)

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
                result["msg"] = "Option Group created"
            elif self.params["state"] == "present" and self.existing is not None:
                if self.payload_changed():
                    item = self.update()
                    result["changed"] = True
                    result["msg"] = "Option Group updated"
            elif self.params["state"] == "absent" and self.existing is not None:
                self.delete()
                result["changed"] = True
                result["msg"] = "Option Group deleted"

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
        dhcp_options=dict(
            type="list",
            elements="dict",
            options=dict(
                group=dict(type="str"),
                option_code=dict(type="str"),
                option_value=dict(type="str"),
                type=dict(type="str", choices=["group", "option"]),
            ),
        ),
        name=dict(type="str", required=True),
        protocol=dict(type="str", choices=["ip4", "ip6"]),
        tags=dict(type="dict"),
    )

    module = OptionGroupModule(
        argument_spec=module_args,
        supports_check_mode=True,
        required_if=[("state", "present", ["name"])],
    )

    module.run_command()


if __name__ == "__main__":
    main()
