#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: Infoblox Inc.
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: dtc_snmp_user_security_model
short_description: Manages SNMP User Security
description:
    - Manages SNMP User Security
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
    auth_passphrase:
        description:
            - "User passphrase for authentication. Ignored for B(NoAuth), otherwise mandatory."
        type: str
    auth_protocol:
        description:
            - "Authentication protocol."
            - "Allowed values:"
            - "* NoAuth"
            - "* MD5"
            - "* SHA"
            - "Defaults to B(NoAuth)."
        type: str
    privacy_passphrase:
        description:
            - "User passphrase for privacy. Ignored for B(NoPrivacy), otherwise mandatory."
        type: str
    privacy_protocol:
        description:
            - "Privacy protocol. Must be B(NoPrivacy) if auth_protocol set to B(NoAuth)."
            - "Allowed values:"
            - "* NoPrivacy"
            - "* DES"
            - "* AES"
            - "Defaults to B(NoPrivacy)."
        type: str
    username:
        description:
            - "User name with which to associate security information."
        type: str

extends_documentation_fragment:
    - infoblox.universal_ddi.common
"""  # noqa: E501

EXAMPLES = r"""
    - name: Create SNMP User Security Model with NoAuth/NoPrivacy
      infoblox.universal_ddi.dtc_snmp_user_security_model:
        username: "snmp_user"
        auth_protocol: "NoAuth"
        privacy_protocol: "NoPrivacy"
        state: present
      register: usm

    - name: Create SNMP User Security Model with MD5 authentication
      infoblox.universal_ddi.dtc_snmp_user_security_model:
        username: "snmp_auth_user"
        auth_protocol: "MD5"
        auth_passphrase: "my_auth_password"
        privacy_protocol: "NoPrivacy"
        state: present

    - name: Create SNMP User Security Model with SHA auth and AES privacy
      infoblox.universal_ddi.dtc_snmp_user_security_model:
        username: "snmp_priv_user"
        auth_protocol: "SHA"
        auth_passphrase: "my_auth_password"
        privacy_protocol: "AES"
        privacy_passphrase: "my_priv_password"
        state: present

    - name: Delete SNMP User Security Model
      infoblox.universal_ddi.dtc_snmp_user_security_model:
        username: "snmp_user"
        state: absent
"""

RETURN = r"""
id:
    description:
        - ID of the SnmpUserSecurity object
    type: str
    returned: Always
item:
    description:
        - SnmpUserSecurity object
    type: complex
    returned: Always
    contains:
        auth_passphrase:
            description:
                - "User passphrase for authentication. Ignored for B(NoAuth), otherwise mandatory."
            type: str
            returned: Always
        auth_protocol:
            description:
                - "Authentication protocol."
                - "Allowed values:"
                - "* NoAuth"
                - "* MD5"
                - "* SHA"
                - "Defaults to B(NoAuth)."
            type: str
            returned: Always
        id:
            description:
                - "The resource identifier."
            type: str
            returned: Always
        privacy_passphrase:
            description:
                - "User passphrase for privacy. Ignored for B(NoPrivacy), otherwise mandatory."
            type: str
            returned: Always
        privacy_protocol:
            description:
                - "Privacy protocol. Must be B(NoPrivacy) if auth_protocol set to B(NoAuth)."
                - "Allowed values:"
                - "* NoPrivacy"
                - "* DES"
                - "* AES"
                - "Defaults to B(NoPrivacy)."
            type: str
            returned: Always
        username:
            description:
                - "User name with which to associate security information."
            type: str
            returned: Always
"""  # noqa: E501

from ansible_collections.infoblox.universal_ddi.plugins.module_utils.modules import UniversalDDIAnsibleModule

try:
    from dtc import SnmpUserSecurityApi, SNMPUserSecurityModel
    from universal_ddi_client import ApiException, NotFoundException
except ImportError:
    pass  # Handled by UniversalDDIAnsibleModule


class SnmpUserSecurityModule(UniversalDDIAnsibleModule):
    def __init__(self, *args, **kwargs):
        super(SnmpUserSecurityModule, self).__init__(*args, **kwargs)

        exclude = ["state", "csp_url", "api_key", "portal_url", "portal_key", "id"]
        self._payload_params = {k: v for k, v in self.params.items() if v is not None and k not in exclude}
        self._payload = SNMPUserSecurityModel.from_dict(self._payload_params)
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
                resp = SnmpUserSecurityApi(self.client).read(self.params["id"])
                return resp.result
            except NotFoundException as e:
                if self.params["state"] == "absent":
                    return None
                raise e
        else:
            filter = f"username=='{self.params['username']}'"
            resp = SnmpUserSecurityApi(self.client).list(filter=filter)

            # If no results, set results to empty list
            if not resp.results:
                resp.results = []

            if len(resp.results) == 1:
                return resp.results[0]
            if len(resp.results) > 1:
                self.fail_json(msg=f"Found multiple SnmpUserSecurity: {resp.results}")
            if len(resp.results) == 0:
                return None

    def create(self):
        if self.check_mode:
            return None

        resp = SnmpUserSecurityApi(self.client).create(body=self.payload)
        return resp.result.model_dump(by_alias=True, exclude_none=True)

    def update(self):
        if self.check_mode:
            return None

        resp = SnmpUserSecurityApi(self.client).update(id=self.existing.id, body=self.payload)
        return resp.result.model_dump(by_alias=True, exclude_none=True)

    def delete(self):
        if self.check_mode:
            return

        SnmpUserSecurityApi(self.client).delete(self.existing.id)

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
                result["msg"] = "SnmpUserSecurity created"
            elif self.params["state"] == "present" and self.existing is not None:
                if self.payload_changed():
                    item = self.update()
                    result["changed"] = True
                    result["msg"] = "SnmpUserSecurity updated"
            elif self.params["state"] == "absent" and self.existing is not None:
                self.delete()
                result["changed"] = True
                result["msg"] = "SnmpUserSecurity deleted"

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
        auth_passphrase=dict(type="str", no_log=True),
        auth_protocol=dict(type="str", default="NoAuth"),
        privacy_passphrase=dict(type="str", no_log=True),
        privacy_protocol=dict(type="str", default="NoPrivacy"),
        username=dict(type="str"),
    )

    module = SnmpUserSecurityModule(
        argument_spec=module_args,
        supports_check_mode=True,
        required_if=[("state", "present", ["username"])],
    )

    module.run_command()


if __name__ == "__main__":
    main()
