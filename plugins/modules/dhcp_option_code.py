#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: Infoblox Inc.
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: dhcp_option_code
short_description: Manage OptionCode
description:
    - Manage OptionCode
version_added: 2.0.0
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
    array:
        description:
            - "Indicates whether the option value is an array of the type or not."
        type: bool
    code:
        description:
            - "The option code."
        type: int
    comment:
        description:
            - "The description for the option code. May contain 0 to 1024 characters. Can include UTF-8."
        type: str
    name:
        description:
            - "The name of the option code. Must contain 1 to 256 characters. Can include UTF-8."
        type: str
    option_space:
        description:
            - "The resource identifier."
        type: str
    type:
        description:
            - "The option type for the option code."
            - "Valid values are:"
            - "* I(address4)"
            - "* I(address6)"
            - "* I(boolean)"
            - "* I(empty)"
            - "* I(fqdn)"
            - "* I(int8)"
            - "* I(int16)"
            - "* I(int32)"
            - "* I(text)"
            - "* I(uint8)"
            - "* I(uint16)"
            - "* I(uint32)"
        type: str

extends_documentation_fragment:
    - infoblox.universal_ddi.common
"""  # noqa: E501

EXAMPLES = r"""
    - name: Create a DHCP Option Space (Required as parent)
      infoblox.universal_ddi.dhcp_option_space:
        name: "{{ option_space_name }}"
        state: present
      check_mode: true
      register: option_space
    
    - name: Create a DHCP Option Code
      infoblox.universal_ddi.dhcp_option_code:
          name: "example_option_code_name"
          code: "145"
          option_space: "{{ option_space.id }}"
          type: "int64"
          state: present
      register: option_code
    
    - name: Delete a DHCP Option Code
      infoblox.universal_ddi.dhcp_option_code:
        id: "{{ option_code.id }}"
        state: absent
      register: option_code
"""  # noqa: E501

RETURN = r"""
id:
    description:
        - ID of the OptionCode object
    type: str
    returned: Always
item:
    description:
        - OptionCode object
    type: complex
    returned: Always
    contains:
        array:
            description:
                - "Indicates whether the option value is an array of the type or not."
            type: bool
            returned: Always
        code:
            description:
                - "The option code."
            type: int
            returned: Always
        comment:
            description:
                - "The description for the option code. May contain 0 to 1024 characters. Can include UTF-8."
            type: str
            returned: Always
        created_at:
            description:
                - "Time when the object has been created."
            type: str
            returned: Always
        id:
            description:
                - "The resource identifier."
            type: str
            returned: Always
        name:
            description:
                - "The name of the option code. Must contain 1 to 256 characters. Can include UTF-8."
            type: str
            returned: Always
        option_space:
            description:
                - "The resource identifier."
            type: str
            returned: Always
        source:
            description:
                - "The source for the option code."
                - "Valid values are:"
                - "* I(dhcp_server)"
                - "* I(reserved)"
                - "* I(blox_one_ddi)"
                - "* I(customer)"
                - "Defaults to I(customer)."
            type: str
            returned: Always
        type:
            description:
                - "The option type for the option code."
                - "Valid values are:"
                - "* I(address4)"
                - "* I(address6)"
                - "* I(boolean)"
                - "* I(empty)"
                - "* I(fqdn)"
                - "* I(int8)"
                - "* I(int16)"
                - "* I(int32)"
                - "* I(text)"
                - "* I(uint8)"
                - "* I(uint16)"
                - "* I(uint32)"
            type: str
            returned: Always
        updated_at:
            description:
                - "Time when the object has been updated. Equals to I(created_at) if not updated after creation."
            type: str
            returned: Always
"""  # noqa: E501

from ansible_collections.infoblox.universal_ddi.plugins.module_utils.modules import UniversalDDIAnsibleModule

try:
    from universal_ddi_client import ApiException, NotFoundException
    from ipam import OptionCode, OptionCodeApi
except ImportError:
    pass  # Handled by UniversalDDIAnsibleModule


class OptionCodeModule(UniversalDDIAnsibleModule):
    def __init__(self, *args, **kwargs):
        super(OptionCodeModule, self).__init__(*args, **kwargs)

        exclude = ["state", "csp_url", "api_key", "portal_url", "portal_key", "id"]
        self._payload_params = {k: v for k, v in self.params.items() if v is not None and k not in exclude}
        self._payload = OptionCode.from_dict(self._payload_params)
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
                resp = OptionCodeApi(self.client).read(self.params["id"])
                return resp.result
            except NotFoundException as e:
                if self.params["state"] == "absent":
                    return None
                raise e
        else:
            filter = f"name=='{self.params['name']}' and code== {self.params['code']} and option_space=='{self.params['option_space']}'"
            resp = OptionCodeApi(self.client).list(filter=filter)

            # If no results, set results to empty list
            if not resp.results:
                resp.results = []

            if len(resp.results) == 1:
                return resp.results[0]
            if len(resp.results) > 1:
                self.fail_json(msg=f"Found multiple OptionCode: {resp.results}")
            if len(resp.results) == 0:
                return None

    def create(self):
        if self.check_mode:
            return None

        resp = OptionCodeApi(self.client).create(body=self.payload)
        return resp.result.model_dump(by_alias=True, exclude_none=True)

    def update(self):
        if self.check_mode:
            return None

        resp = OptionCodeApi(self.client).update(id=self.existing.id, body=self.payload)
        return resp.result.model_dump(by_alias=True, exclude_none=True)

    def delete(self):
        if self.check_mode:
            return

        OptionCodeApi(self.client).delete(self.existing.id)

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
                result["msg"] = "OptionCode created"
            elif self.params["state"] == "present" and self.existing is not None:
                if self.payload_changed():
                    item = self.update()
                    result["changed"] = True
                    result["msg"] = "OptionCode updated"
            elif self.params["state"] == "absent" and self.existing is not None:
                self.delete()
                result["changed"] = True
                result["msg"] = "OptionCode deleted"

            if self.check_mode:
                # if in check mode, do not update the result or the diff, just return the changed state
                self.exit_json(**result)

            result["diff"] = dict(
                before=self.existing.model_dump(by_alias=True, exclude_none=True) if self.existing is not None else {},
                after=item,
            )
            result["object"] = item
            result["id"] = self.existing.id if self.existing is not None else item["id"] if (item and "id" in item) else None
        except ApiException as e:
            self.fail_json(msg=f"Failed to execute command: {e.status} {e.reason} {e.body}")

        self.exit_json(**result)


def main():
    module_args = dict(
        id=dict(type="str", required=False),
        state=dict(type="str", required=False, choices=["present", "absent"], default="present"),
        array=dict(type="bool"),
        code=dict(type="int"),
        comment=dict(type="str"),
        name=dict(type="str"),
        option_space=dict(type="str"),
        type=dict(type="str"),

    )

    module = OptionCodeModule(
        argument_spec=module_args,
        supports_check_mode=True,
        required_if=[("state", "present", ["name", "code", "option_space", "type"])],
    )

    module.run_command()


if __name__ == "__main__":
    main()
