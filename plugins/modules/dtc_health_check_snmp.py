#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: Infoblox Inc.
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: dtc_health_check_snmp
short_description: Manages a DTC SNMP Health Check
description:
    - Manages a DTC SNMP Health Check
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
    check_list:
        description:
            - "List of specific checks for SNMP entries and their values in MIB hierarchy. Supported up to 15 checks."
        type: list
        elements: dict
        suboptions:
            comment:
                description:
                    - "Optional. Comment for B(EntryCheck)."
                type: str
            max_value:
                description:
                    - "Optional. Expected max value of an entry to check against. Used for B(in) operator only, otherwise ignored."
                type: str
            name:
                description:
                    - "Name is a dotted-decimal number that defines the location of the entry in the universal MIB tree."
                type: str
            operator:
                description:
                    - "Operator defines operation to perform on an entry value."
                    - "Allowed values:"
                    - "* any - any value must be present"
                    - "* eq  - entry value must be equal to check's B(value)."
                    - "* leq - entry value must less or equal to check's B(value)."
                    - "* geq - entry value must be great or equal to check's B(value)."
                    - "* in  - entry value must be greater or equal than B(value) and less or equal than B(max_value)."
                    - "Operator B(in) is supported only for B(integer) types."
                type: str
                choices:
                    - any
                    - eq
                    - leq
                    - geq
                    - in
            type:
                description:
                    - "Type defines type of an entry value."
                    - "Allowed values:"
                    - "* string"
                    - "* integer"
                    - "String type does not support B(in) operator."
                type: str
                choices:
                    - string
                    - integer
            value:
                description:
                    - "Optional. Expected value of an entry to check against. Ignored for B(any) operator."
                type: str
    comment:
        description:
            - "Optional. Comment for B(SNMPHealthCheck)."
        type: str
    community:
        description:
            - "SNMP community string used for authentication. Required for B(v1) and B(v2c) versions, ignored for B(v3)."
        type: str
    context_engine_id:
        description:
            - "Optional. Uniquely identifies an SNMP entity that may realize an instance of a context with a particular context name."
            - "Format is an arbitrary string that can contain from 10 to 64 hexadecimal digits (5 to 32 octet numbers)."
            - "Ignored for B(v1) and B(v2c) versions."
        type: str
    context_name:
        description:
            - "Optional. Name of administratively unique context for B(v3) version. Ignored for B(v1) and B(v2c) versions."
        type: str
    disabled:
        description:
            - "Optional. Flag which enables/disables B(SNMPHealthCheck). Defaults to I(false)."
        type: bool
    interval:
        description:
            - "Optional. Interval value in seconds. The health check runs only for the specified interval and it is measured from the beginning of the previous check cycle. Defaults to I(15)."
        type: int
        default: 15
    name:
        description:
            - "Display name of B(SNMPHealthCheck)."
        type: str
        required: true
    port:
        description:
            - "Optional. Destination UDP port of B(SNMPHealthCheck). Defaults to I(161)."
        type: int
        default: 161
    retry_down:
        description:
            - "Optional. Retry down count. The value determines how many bad health checks in a row must be received by the onprem host from the DTC Server for treating the health check as failed. Defaults to I(1)."
        type: int
        default: 1
    retry_up:
        description:
            - "Optional. Retry up count. The value determines how many good health checks in a row must be received by the onprem host from the DTC Server for treating the health check as successful. Defaults to I(1)."
        type: int
        default: 1
    tags:
        description:
            - "Optional. The tags for B(SNMPHealthCheck) in JSON format."
        type: dict
    timeout:
        description:
            - "Optional. Timeout value in seconds. The health check waits for the specified number of seconds after sending a request. If it does not receive a response within the number of seconds, then the health check is considered as failed. Defaults to I(10)."
        type: int
        default: 10
    user_security_model:
        description:
            - "Resource identifier for the User Security Model (USM) configuration. Required for B(v3) version, ignored for B(v1) and B(v2c)."
        type: str
    version:
        description:
            - "SNMP version. Required when I(state=present)."
            - "Allowed values:"
            - "* v1  - version 1"
            - "* v2c - version 2 community"
            - "* v3  - version 3"
        type: str
        choices:
          -  v1
          -  v2c
          -  v3

extends_documentation_fragment:
    - infoblox.universal_ddi.common
"""  # noqa: E501

EXAMPLES = r"""
    - name: Create SNMP Health Check
      infoblox.universal_ddi.dtc_health_check_snmp:
        name: "example-snmp-health-check"
        version: "v2c"
        community: "public"
        state: present
      register: health_check_snmp

    - name: Create SNMP Health Check with additional fields
      infoblox.universal_ddi.dtc_health_check_snmp:
        name: "example-snmp-health-check"
        version: "v2c"
        community: "public"
        comment: "Example SNMP health check"
        port: 161
        interval: 30
        timeout: 15
        retry_up: 3
        retry_down: 2
        tags:
          environment: "production"
        state: present

    - name: Create SNMP Health Check with check_list
      infoblox.universal_ddi.dtc_health_check_snmp:
        name: "example-snmp-health-check"
        version: "v2c"
        community: "public"
        check_list:
          - name: "1.3.6.1.2.1.1.3.0"
            type: "integer"
            operator: "geq"
            value: "100"
        state: present

    - name: Delete SNMP Health Check
      infoblox.universal_ddi.dtc_health_check_snmp:
        name: "example-snmp-health-check"
        version: "v2c"
        community: "public"
        state: absent
"""

RETURN = r"""
id:
    description:
        - ID of the HealthCheckSnmp object
    type: str
    returned: Always
item:
    description:
        - HealthCheckSnmp object
    type: complex
    returned: Always
    contains:
        check_list:
            description:
                - "List of specific checks for SNMP entries and their values in MIB hierarchy. Supported up to 15 checks."
            type: list
            returned: Always
            elements: dict
            contains:
                comment:
                    description:
                        - "Optional. Comment for B(EntryCheck)."
                    type: str
                    returned: Always
                max_value:
                    description:
                        - "Optional. Expected max value of an entry to check against. Used for B(in) operator only, otherwise ignored."
                    type: str
                    returned: Always
                name:
                    description:
                        - "Name is a dotted-decimal number that defines the location of the entry in the universal MIB tree."
                    type: str
                    returned: Always
                operator:
                    description:
                        - "Operator defines operation to perform on an entry value."
                        - "Allowed values:"
                        - "* any - any value must be present"
                        - "* eq  - entry value must be equal to check's B(value)."
                        - "* leq - entry value must less or equal to check's B(value)."
                        - "* geq - entry value must be great or equal to check's B(value)."
                        - "* in  - entry value must be greater or equal than B(value) and less or equal than B(max_value)."
                        - "Operator B(in) is supported only for B(integer) types."
                    type: str
                    returned: Always
                type:
                    description:
                        - "Type defines type of an entry value."
                        - "Allowed values:"
                        - "* string"
                        - "* integer"
                        - "String type does not support B(in) operator."
                    type: str
                    returned: Always
                value:
                    description:
                        - "Optional. Expected value of an entry to check against. Ignored for B(any) operator."
                    type: str
                    returned: Always
        comment:
            description:
                - "Optional. Comment for B(SNMPHealthCheck)."
            type: str
            returned: Always
        community:
            description:
                - "Optional. SNMP community string used for authentication. Mandatory for B(v1) and B(v2c) versions, ignored for B(v3)."
                - "Defaults to B(public)."
            type: str
            returned: Always
        context_engine_id:
            description:
                - "Optional. Uniquely identifies an SNMP entity that may realize an instance of a context with a particular context name."
                - "Format is an arbitrary string that can contain from 10 to 64 hexadecimal digits (5 to 32 octet numbers)."
                - "Ignored for B(v1) and B(v2c) versions."
            type: str
            returned: Always
        context_name:
            description:
                - "Optional. Name of administratively unique context for B(v3) version. Ignored for B(v1) and B(v2c) versions."
            type: str
            returned: Always
        disabled:
            description:
                - "Optional. Flag which enables/disables B(SNMPHealthCheck). Defaults to I(false)."
            type: bool
            returned: Always
        id:
            description:
                - "The resource identifier."
            type: str
            returned: Always
        interval:
            description:
                - "Optional. Interval value in seconds. The health check runs only for the specified interval and it is measured from the beginning of the previous check cycle. Defaults to I(15)."
            type: int
            returned: Always
        metadata:
            description:
                - "Output only. B(SNMPHealthCheck) metadata. Defaults to empty object and should be explicitly requested using field selection."
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
                - "Display name of B(SNMPHealthCheck)."
            type: str
            returned: Always
        port:
            description:
                - "Optional. Destination UDP port of B(SNMPHealthCheck). Defaults to I(161)."
            type: int
            returned: Always
        retry_down:
            description:
                - "Optional. Retry down count. The value determines how many bad health checks in a row must be received by the onprem host from the DTC Server for treating the health check as failed. Defaults to I(1)."
            type: int
            returned: Always
        retry_up:
            description:
                - "Optional. Retry up count. The value determines how many good health checks in a row must be received by the onprem host from the DTC Server for treating the health check as successful. Defaults to I(1)."
            type: int
            returned: Always
        tags:
            description:
                - "Optional. The tags for B(SNMPHealthCheck) in JSON format."
            type: dict
            returned: Always
        timeout:
            description:
                - "Optional. Timeout value in seconds. The health check waits for the specified number of seconds after sending a request. If it does not receive a response within the number of seconds, then the health check is considered as failed. Defaults to I(10)."
            type: int
            returned: Always
        user_security_model:
            description:
                - "The resource identifier."
            type: str
            returned: Always
        version:
            description:
                - "SNMP version."
                - "Allowed values:"
                - "* v1  - version 1"
                - "* v2c - version 2 community"
                - "* v3  - version 3"
            type: str
            returned: Always
"""  # noqa: E501

from ansible_collections.infoblox.universal_ddi.plugins.module_utils.modules import UniversalDDIAnsibleModule

try:
    from dtc import HealthCheckSnmpApi, SNMPHealthCheck
    from universal_ddi_client import ApiException, NotFoundException
except ImportError:
    pass  # Handled by UniversalDDIAnsibleModule


class HealthCheckSnmpModule(UniversalDDIAnsibleModule):
    def __init__(self, *args, **kwargs):
        super(HealthCheckSnmpModule, self).__init__(*args, **kwargs)

        exclude = ["state", "csp_url", "api_key", "portal_url", "portal_key", "id", "metadata"]
        self._payload_params = {k: v for k, v in self.params.items() if v is not None and k not in exclude}
        self._payload = SNMPHealthCheck.from_dict(self._payload_params)
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
                resp = HealthCheckSnmpApi(self.client).read(self.params["id"], inherit="full")
                return resp.result
            except NotFoundException as e:
                if self.params["state"] == "absent":
                    return None
                raise e
        else:
            filter = f"name=='{self.params['name']}'"
            resp = HealthCheckSnmpApi(self.client).list(filter=filter)

            # If no results, set results to empty list
            if not resp.results:
                resp.results = []

            if len(resp.results) == 1:
                return resp.results[0]
            if len(resp.results) > 1:
                self.fail_json(msg=f"Found multiple HealthCheckSnmp: {resp.results}")
            if len(resp.results) == 0:
                return None

    def create(self):
        if self.check_mode:
            return None

        resp = HealthCheckSnmpApi(self.client).create(body=self.payload)
        return resp.result.model_dump(by_alias=True, exclude_none=True)

    def update(self):
        if self.check_mode:
            return None

        resp = HealthCheckSnmpApi(self.client).update(id=self.existing.id, body=self.payload)
        return resp.result.model_dump(by_alias=True, exclude_none=True)

    def delete(self):
        if self.check_mode:
            return

        HealthCheckSnmpApi(self.client).delete(self.existing.id)

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
                result["msg"] = "HealthCheckSnmp created"
            elif self.params["state"] == "present" and self.existing is not None:
                if self.payload_changed():
                    item = self.update()
                    result["changed"] = True
                    result["msg"] = "HealthCheckSnmp updated"
            elif self.params["state"] == "absent" and self.existing is not None:
                self.delete()
                result["changed"] = True
                result["msg"] = "HealthCheckSnmp deleted"

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
        check_list=dict(
            type="list",
            elements="dict",
            options=dict(
                comment=dict(type="str"),
                max_value=dict(type="str"),
                name=dict(type="str"),
                operator=dict(type="str", choices=["any", "eq", "leq", "geq", "in"]),
                type=dict(type="str", choices=["string", "integer"]),
                value=dict(type="str"),
            ),
        ),
        comment=dict(type="str"),
        community=dict(type="str"),
        context_engine_id=dict(type="str"),
        context_name=dict(type="str"),
        disabled=dict(type="bool"),
        interval=dict(type="int", default=15),
        name=dict(type="str", required=True),
        port=dict(type="int", default=161),
        retry_down=dict(type="int", default=1),
        retry_up=dict(type="int", default=1),
        tags=dict(type="dict"),
        timeout=dict(type="int", default=10),
        user_security_model=dict(type="str"),
        version=dict(type="str", choices=["v1", "v2c", "v3"]),
    )

    module = HealthCheckSnmpModule(
        argument_spec=module_args,
        supports_check_mode=True,
        required_if=[
            ("state", "present", ["name", "version"]),
            ("version", "v1", ["community"]),
            ("version", "v2c", ["community"]),
            ("version", "v3", ["user_security_model"]),
        ],
    )

    module.run_command()


if __name__ == "__main__":
    main()
