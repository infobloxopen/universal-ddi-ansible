#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: Infoblox Inc.
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
from __future__ import absolute_import, division, print_function

__metaclass__ = type

from pygments.lexer import default

DOCUMENTATION = r"""
---
module: dtc_server
short_description: Manages a DTC Server
description:
    - Manages a DTC Server.
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
    address:
        description:
            - "IP Address of the B(Server). Must be set to a valid IP address if B(endpoint_type) is set to B(address). Alternatively, it can be left blank."
        type: str
    auto_create_response_records:
        description:
            - "Optional. If the flag is enabled, A, AAAA or CNAME B(Record) is automatically generated."
            - "Defaults to I(false)."
        type: bool
    comment:
        description:
            - "Optional. Comment for B(Server)."
        type: str
    disabled:
        description:
            - "Optional. Flag which enables/disables B(Server)."
            - "Defaults to I(false)."
        type: bool
        default: false
    endpoint_type:
        description:
            - "The endpoint type configured for the B(Server). Can be IP Address or FQDN. The values of both fields B(address) and B(fqdn) are preserved and are not mutually exclusive, and the B(endpoint_type) defines which one to use."
            - "Allowed values:"
            - "* address"
            - "* fqdn"
            - "Defaults to B(address)."
        choices:
            - address
            - fqdn
        default: address
        type: str
    fqdn:
        description:
            - "Fully Qualified Domain name of the B(Server). Must be set to a valid FQDN if B(endpoint_type) is set to B(fqdn). Alternatively, it can be left blank."
        type: str
    name:
        description:
            - "Display name of B(Server)."
        type: str
    records:
        description:
            - "Optional. List of B(Records) of the B(Server)."
        type: list
        elements: dict
        suboptions:
            rdata:
                description:
                    - "JSON representation of resource record data."
                type: dict
            type:
                description:
                    - "Resource record type."
                    - "List of supported types:"
                    - "* I(A) (I(TYPE1))"
                    - "* I(AAAA) (I(TYPE28))"
                    - "* I(CNAME) (I(TYPE5))"
                    - "* I(HTTPS) (I(TYPE65))"
                    - "* I(SRV) (I(TYPE33))"
                    - "* I(SVCB) (I(TYPE64))"
                type: str
                choices:
                    - A
                    - AAAA
                    - CNAME
                    - HTTPS
                    - SRV
                    - SVCB
    tags:
        description:
            - "Optional. The tags for B(Server) in JSON format."
        type: dict

extends_documentation_fragment:
    - infoblox.universal_ddi.common
"""  # noqa: E501

EXAMPLES = r"""
    - name: Create a DTC Server
      infoblox.universal_ddi.dtc_server:
        name: "example_dtc_server"
        address: "10.0.0.0"
        state: "present"
      register: dtc_server

    - name: Create a DTC Server with FQDN endpoint type
      infoblox.universal_ddi.dtc_server:
        name: "example_dtc_server"
        fqdn: "dtc-server.example.com."
        endpoint_type: "fqdn"
        state: "present"

    - name: Create a DTC Server with Additional Parameters
      infoblox.universal_ddi.dtc_server:
        name: "example_dtc_server"
        address: "10.10.0.0"
        comment: "This is a DTC server"
        disabled: false
        records:
          - type: "CNAME"
            rdata:
              cname: "dtc-cname.example.com."
        tags:
          location: "site-1"
        state: "present"

    - name: Delete the DTC Server
      infoblox.universal_ddi.dtc_server:
        name: "example_dtc_server"
        state: "absent"
"""

RETURN = r"""
id:
    description:
        - ID of the Server object
    type: str
    returned: Always
item:
    description:
        - Server object
    type: complex
    returned: Always
    contains:
        address:
            description:
                - "IP Address of the B(Server). Must be set to a valid IP address if B(endpoint_type) is set to B(address). Alternatively, it can be left blank."
            type: str
            returned: Always
        auto_create_response_records:
            description:
                - "Optional. If the flag is enabled, A, AAAA or CNAME B(Record) is automatically generated."
                - "Defaults to I(false)."
            type: bool
            returned: Always
        comment:
            description:
                - "Optional. Comment for B(Server)."
            type: str
            returned: Always
        disabled:
            description:
                - "Optional. Flag which enables/disables B(Server)."
                - "Defaults to I(false)."
            type: bool
            returned: Always
        endpoint_type:
            description:
                - "The endpoint type configured for the B(Server). Can be IP Address or FQDN. The values of both fields B(address) and B(fqdn) are preserved and are not mutually exclusive, and the B(endpoint_type) defines which one to use."
                - "Allowed values:"
                - "* address"
                - "* fqdn"
                - "Defaults to B(address)."
            choices:
                - address
                - fqdn
            type: str
            returned: Always
        fqdn:
            description:
                - "Fully Qualified Domain name of the B(Server). Must be set to a valid FQDN if B(endpoint_type) is set to B(fqdn). Alternatively, it can be left blank."
            type: str
            returned: Always
        id:
            description:
                - "The resource identifier."
            type: str
            returned: Always
        metadata:
            description:
                - "Output only. B(Server) metadata. Defaults to empty object and should be explicitly requested using field selection."
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
        name:
            description:
                - "Display name of B(Server)."
            type: str
            returned: Always
        records:
            description:
                - "Optional. List of B(Records) of the B(Server)."
            type: list
            returned: Always
            elements: dict
            contains:
                dns_rdata:
                    description:
                        - "The DNS protocol textual representation of the record data."
                    type: str
                    returned: Always
                rdata:
                    description:
                        - "JSON representation of resource record data."
                    type: dict
                    returned: Always
                type:
                    description:
                        - "Resource record type."
                        - "List of supported types:"
                        - "* I(A) (I(TYPE1))"
                        - "* I(AAAA) (I(TYPE28))"
                        - "* I(CNAME) (I(TYPE5))"
                        - "* I(HTTPS) (I(TYPE65))"
                        - "* I(SRV) (I(TYPE33))"
                        - "* I(SVCB) (I(TYPE64))"
                    choices:
                        - A
                        - AAAA
                        - CNAME
                        - HTTPS
                        - SRV
                        - SVCB
                    type: str
                    returned: Always
        tags:
            description:
                - "Optional. The tags for B(Server) in JSON format."
            type: dict
            returned: Always
"""  # noqa: E501

from ansible_collections.infoblox.universal_ddi.plugins.module_utils.modules import UniversalDDIAnsibleModule

try:
    from dtc import Server, ServerApi
    from universal_ddi_client import ApiException, NotFoundException
except ImportError:
    pass  # Handled by UniversalDDIAnsibleModule


class ServerModule(UniversalDDIAnsibleModule):
    def __init__(self, *args, **kwargs):
        super(ServerModule, self).__init__(*args, **kwargs)

        exclude = ["state", "csp_url", "api_key", "portal_url", "portal_key", "id"]
        self._payload_params = {k: v for k, v in self.params.items() if v is not None and k not in exclude}
        self._payload = Server.from_dict(self._payload_params)
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
                resp = ServerApi(self.client).read(self.params["id"])
                return resp.result
            except NotFoundException as e:
                if self.params["state"] == "absent":
                    return None
                raise e
        else:
            filter = f"name=='{self.params['name']}'"
            resp = ServerApi(self.client).list(filter=filter)

            # If no results, set results to empty list
            if not resp.results:
                resp.results = []

            if len(resp.results) == 1:
                return resp.results[0]
            if len(resp.results) > 1:
                self.fail_json(msg=f"Found multiple Server: {resp.results}")
            if len(resp.results) == 0:
                return None

    def create(self):
        if self.check_mode:
            return None

        resp = ServerApi(self.client).create(body=self.payload)
        return resp.result.model_dump(by_alias=True, exclude_none=True)

    def update(self):
        if self.check_mode:
            return None

        resp = ServerApi(self.client).update(id=self.existing.id, body=self.payload)
        return resp.result.model_dump(by_alias=True, exclude_none=True)

    def delete(self):
        if self.check_mode:
            return

        ServerApi(self.client).delete(self.existing.id)

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
                result["msg"] = "Server created"
            elif self.params["state"] == "present" and self.existing is not None:
                if self.payload_changed():
                    item = self.update()
                    result["changed"] = True
                    result["msg"] = "Server updated"
            elif self.params["state"] == "absent" and self.existing is not None:
                self.delete()
                result["changed"] = True
                result["msg"] = "Server deleted"

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
        address=dict(type="str"),
        auto_create_response_records=dict(type="bool"),
        comment=dict(type="str"),
        disabled=dict(type="bool", default=False),
        endpoint_type=dict(type="str", choices=["address", "fqdn"], default="address"),
        fqdn=dict(type="str"),
        name=dict(type="str"),
        records=dict(
            type="list",
            elements="dict",
            options=dict(
                rdata=dict(type="dict"),
                type=dict(type="str", choices=["A", "AAAA", "CNAME", "HTTPS", "SRV", "SVCB"]),
            ),
        ),
        tags=dict(type="dict"),
    )

    module = ServerModule(
        argument_spec=module_args,
        supports_check_mode=True,
        required_if=[("state", "present", ["name"])],
    )

    module.run_command()


if __name__ == "__main__":
    main()
