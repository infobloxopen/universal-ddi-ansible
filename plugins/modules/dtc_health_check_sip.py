#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: Infoblox Inc.
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: dtc_health_check_sip
short_description: Manages a DTC SIP Health Check
description:
    - Manage DTC SIP Health Check
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
            - "Optional. Comment for B(SIPHealthCheck)."
        type: str
    disabled:
        description:
            - "Optional. Flag which enables/disables B(SIPHealthCheck). Defaults to I(false)."
        type: bool
    interval:
        description:
            - "Optional. Interval value in seconds. The health check runs only for the specified interval and it is measured from the beginning of the previous check cycle. Defaults to I(15)."
        type: int
    name:
        description:
            - "Display name of B(SIPHealthCheck)."
        type: str
    port:
        description:
            - "Optional. Destination port for the SIP OPTIONS request. Defaults to I(5060) for both TCP and UDP transport."
        type: int
        default: 5060
    result_code:
        description:
            - "Optional. Expected SIP response code, used with I(CODE_IS) and I(CODE_IS_NOT) result modes. Defaults to I(200)."
        type: int
        default: 200
    result_mode:
        description:
            - "Optional. Defines how the SIP response code is evaluated. Supported values: I(ANY), I(CODE_IS), I(CODE_IS_NOT). Defaults to I(CODE_IS)."
        type: str
        choices:
            - ANY
            - CODE_IS
            - CODE_IS_NOT
        default: CODE_IS
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
            - "Optional. The tags for B(SIPHealthCheck) in JSON format."
        type: dict
    timeout:
        description:
            - "Optional. Timeout value in seconds. The health check waits for the specified number of seconds after sending a request. If it does not receive a response within the number of seconds, then the health check is considered as failed. Defaults to I(10)."
        type: int
        default: 10
    transport:
        description:
            - "Optional. Transport protocol for the SIP OPTIONS request. Supported values: I(TCP), I(UDP). Defaults to I(TCP)."
        type: str
        choices:
            - TCP
            - UDP
        default: TCP

extends_documentation_fragment:
    - infoblox.universal_ddi.common
"""  # noqa: E501

EXAMPLES = r"""
    - name: Create SIP Health Check
      infoblox.universal_ddi.dtc_health_check_sip:
        name: "example-sip-health-check"
        state: present
      register: health_check_sip

    - name: Create SIP Health Check with additional fields
      infoblox.universal_ddi.dtc_health_check_sip:
        name: "example-sip-health-check"
        comment: "Example SIP health check"
        transport: UDP
        port: 5060
        result_mode: CODE_IS
        result_code: 200
        interval: 30
        timeout: 15
        retry_up: 3
        retry_down: 2
        tags:
          environment: "production"
        state: present

    - name: Delete SIP Health Check
      infoblox.universal_ddi.dtc_health_check_sip:
        name: "example-sip-health-check"
        state: absent
"""

RETURN = r"""
id:
    description:
        - ID of the HealthCheckSip object
    type: str
    returned: Always
item:
    description:
        - HealthCheckSip object
    type: complex
    returned: Always
    contains:
        comment:
            description:
                - "Optional. Comment for B(SIPHealthCheck)."
            type: str
            returned: Always
        disabled:
            description:
                - "Optional. Flag which enables/disables B(SIPHealthCheck). Defaults to I(false)."
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
                - "Output only. B(SIPHealthCheck) metadata. Defaults to empty object and should be explicitly requested using field selection."
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
                - "Display name of B(SIPHealthCheck)."
            type: str
            returned: Always
        port:
            description:
                - "Optional. Destination port for the SIP OPTIONS request. Defaults to I(5060) for both TCP and UDP transport."
            type: int
            returned: Always
        result_code:
            description:
                - "Optional. Expected SIP response code, used with I(CODE_IS) and I(CODE_IS_NOT) result modes. Defaults to I(200)."
            type: int
            returned: Always
        result_mode:
            description:
                - "Optional. Defines how the SIP response code is evaluated. Supported values: I(ANY), I(CODE_IS), I(CODE_IS_NOT). Defaults to I(CODE_IS)."
            type: str
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
                - "Optional. The tags for B(SIPHealthCheck) in JSON format."
            type: dict
            returned: Always
        timeout:
            description:
                - "Optional. Timeout value in seconds. The health check waits for the specified number of seconds after sending a request. If it does not receive a response within the number of seconds, then the health check is considered as failed. Defaults to I(10)."
            type: int
            returned: Always
        transport:
            description:
                - "Optional. Transport protocol for the SIP OPTIONS request. Supported values: I(TCP), I(UDP). Defaults to I(TCP)."
            type: str
            returned: Always
"""  # noqa: E501

from ansible_collections.infoblox.universal_ddi.plugins.module_utils.modules import UniversalDDIAnsibleModule

try:
    from dtc import SIPHealthCheck, HealthCheckSipApi
    from universal_ddi_client import ApiException, NotFoundException
except ImportError:
    pass  # Handled by UniversalDDIAnsibleModule


class HealthCheckSipModule(UniversalDDIAnsibleModule):
    def __init__(self, *args, **kwargs):
        super(HealthCheckSipModule, self).__init__(*args, **kwargs)

        exclude = ["state", "csp_url", "api_key", "portal_url", "portal_key", "id"]
        self._payload_params = {k: v for k, v in self.params.items() if v is not None and k not in exclude}
        self._payload = SIPHealthCheck.from_dict(self._payload_params)
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
                resp = HealthCheckSipApi(self.client).read(self.params["id"])
                return resp.result
            except NotFoundException as e:
                if self.params["state"] == "absent":
                    return None
                raise e
        else:
            filter = f"name=='{self.params['name']}'"
            resp = HealthCheckSipApi(self.client).list(filter=filter)

            # If no results, set results to empty list
            if not resp.results:
                resp.results = []

            if len(resp.results) == 1:
                return resp.results[0]
            if len(resp.results) > 1:
                self.fail_json(msg=f"Found multiple HealthCheckSip: {resp.results}")
            if len(resp.results) == 0:
                return None

    def create(self):
        if self.check_mode:
            return None

        resp = HealthCheckSipApi(self.client).create(body=self.payload)
        return resp.result.model_dump(by_alias=True, exclude_none=True)

    def update(self):
        if self.check_mode:
            return None

        resp = HealthCheckSipApi(self.client).update(id=self.existing.id, body=self.payload)
        return resp.result.model_dump(by_alias=True, exclude_none=True)

    def delete(self):
        if self.check_mode:
            return

        HealthCheckSipApi(self.client).delete(self.existing.id)

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
                result["msg"] = "HealthCheckSip created"
            elif self.params["state"] == "present" and self.existing is not None:
                if self.payload_changed():
                    item = self.update()
                    result["changed"] = True
                    result["msg"] = "HealthCheckSip updated"
            elif self.params["state"] == "absent" and self.existing is not None:
                self.delete()
                result["changed"] = True
                result["msg"] = "HealthCheckSip deleted"

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
        comment=dict(type="str"),
        disabled=dict(type="bool"),
        interval=dict(type="int"),
        name=dict(type="str"),
        port=dict(type="int", default=5060),
        result_code=dict(type="int", default=200),
        result_mode=dict(type="str", choices=["ANY", "CODE_IS", "CODE_IS_NOT"], default="CODE_IS"),
        retry_down=dict(type="int", default=1),
        retry_up=dict(type="int", default=1),
        tags=dict(type="dict"),
        timeout=dict(type="int", default=10),
        transport=dict(type="str", choices=["TCP", "UDP"], default="TCP"),
    )

    module = HealthCheckSipModule(
        argument_spec=module_args,
        supports_check_mode=True,
        required_if=[("state", "present", ["name"])],
    )

    module.run_command()


if __name__ == "__main__":
    main()
