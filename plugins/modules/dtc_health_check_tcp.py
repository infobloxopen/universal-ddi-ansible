#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: Infoblox Inc.
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: dtc_health_check_tcp
short_description: Manage HealthCheckTcp
description:
    - Manage HealthCheckTcp
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
            - "Optional. Comment for B(TCPHealthCheck)."
        type: str
    disabled:
        description:
            - "Optional. Flag which enables/disables B(TCPHealthCheck). Defaults to I(false)."
        type: bool
    interval:
        description:
            - "Optional. Interval value in seconds. The health check runs only for the specified interval and it is measured from the beginning of the previous check cycle. Defaults to I(15)."
        type: int
    metadata:
        description:
            - "Output only. B(TCPHealthCheck) metadata. Defaults to empty object and should be explicitly requested using field selection."
        type: dict
        suboptions:
            used_by:
                description:
                    - "List of structs representing a limited view on configuration objects that use a resource the metadata is provided for."
                type: list
                elements: dict
                suboptions:
                    details:
                        description:
                            - "Structured data consisting of additional details of the configuration resource."
                        type: dict
                    display_name:
                        description:
                            - "Display name of the configuration resource."
                        type: str
    name:
        description:
            - "Display name of B(TCPHealthCheck)."
        type: str
        required: true
    port:
        description:
            - "Destination TCP port of B(TCPHealthCheck)."
        type: int
        required: true
    retry_down:
        description:
            - "Optional. Retry down count. The value determines how many bad health checks in a row must be received by the onprem host from the DTC Server for treating the health check as failed. Defaults to I(1)."
        type: int
    retry_up:
        description:
            - "Optional. Retry up count. The value determines how many good health checks in a row must be received by the onprem host from the DTC Server for treating the health check as successful. Defaults to I(1)."
        type: int
    tags:
        description:
            - "Optional. The tags for B(TCPHealthCheck) in JSON format."
        type: dict
    timeout:
        description:
            - "Optional. Timeout value in seconds. The health check waits for the specified number of seconds after sending a request. If it does not receive a response within the number of seconds, then the health check is considered as failed. Defaults to I(10)."
        type: int

extends_documentation_fragment:
    - infoblox.universal_ddi.common
"""  # noqa: E501

EXAMPLES = r"""
    - name: Create a TCP Health Check
      infoblox.universal_ddi.dtc_health_check_tcp:
        name: "example_tcp_health_check"
        port: 80
        state: present
      register: tcp_health_check

    - name: Create a TCP Health Check with additional parameters
      infoblox.universal_ddi.dtc_health_check_tcp:
        name: "example_tcp_health_check"
        port: 8080
        interval: 15
        retry_down: 2
        retry_up: 2
        timeout: 10
        disabled: false
        tags:
          location: "site-1"
        comment: "Example TCP health check"
        state: present
    
    - name: Delete TCP Health Check
      infoblox.universal_ddi.dtc_health_check_tcp:
        name: "example_tcp_health_check"
        port: 80
        state: absent
"""  # noqa: E501

RETURN = r"""
id:
    description:
        - ID of the HealthCheckTcp object
    type: str
    returned: Always
item:
    description:
        - HealthCheckTcp object
    type: complex
    returned: Always
    contains:
        comment:
            description:
                - "Optional. Comment for B(TCPHealthCheck)."
            type: str
            returned: Always
        disabled:
            description:
                - "Optional. Flag which enables/disables B(TCPHealthCheck). Defaults to I(false)."
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
                - "Output only. B(TCPHealthCheck) metadata. Defaults to empty object and should be explicitly requested using field selection."
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
                - "Display name of B(TCPHealthCheck)."
            type: str
            returned: Always
        port:
            description:
                - "Destination TCP port of B(TCPHealthCheck)."
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
                - "Optional. The tags for B(TCPHealthCheck) in JSON format."
            type: dict
            returned: Always
        timeout:
            description:
                - "Optional. Timeout value in seconds. The health check waits for the specified number of seconds after sending a request. If it does not receive a response within the number of seconds, then the health check is considered as failed. Defaults to I(10)."
            type: int
            returned: Always
"""  # noqa: E501

from ansible_collections.infoblox.universal_ddi.plugins.module_utils.modules import UniversalDDIAnsibleModule

try:
    from dtc import HealthCheckTcpApi, TCPHealthCheck
    from universal_ddi_client import ApiException, NotFoundException
except ImportError:
    pass  # Handled by UniversalDDIAnsibleModule


class HealthCheckTcpModule(UniversalDDIAnsibleModule):
    def __init__(self, *args, **kwargs):
        super(HealthCheckTcpModule, self).__init__(*args, **kwargs)

        exclude = ["state", "csp_url", "api_key", "portal_url", "portal_key", "id"]
        self._payload_params = {k: v for k, v in self.params.items() if v is not None and k not in exclude}
        self._payload = TCPHealthCheck.from_dict(self._payload_params)
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
                resp = HealthCheckTcpApi(self.client).read(self.params["id"])
                return resp.result
            except NotFoundException as e:
                if self.params["state"] == "absent":
                    return None
                raise e
        else:
            filter = f"name=='{self.params['name']}'"
            resp = HealthCheckTcpApi(self.client).list(filter=filter)

            # If no results, set results to empty list
            if not resp.results:
                resp.results = []

            if len(resp.results) == 1:
                return resp.results[0]
            if len(resp.results) > 1:
                self.fail_json(msg=f"Found multiple HealthCheckTcp: {resp.results}")
            if len(resp.results) == 0:
                return None

    def create(self):
        if self.check_mode:
            return None

        resp = HealthCheckTcpApi(self.client).create(body=self.payload)
        return resp.result.model_dump(by_alias=True, exclude_none=True)

    def update(self):
        if self.check_mode:
            return None

        resp = HealthCheckTcpApi(self.client).update(id=self.existing.id, body=self.payload)
        return resp.result.model_dump(by_alias=True, exclude_none=True)

    def delete(self):
        if self.check_mode:
            return

        HealthCheckTcpApi(self.client).delete(self.existing.id)

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
                result["msg"] = "HealthCheckTcp created"
            elif self.params["state"] == "present" and self.existing is not None:
                if self.payload_changed():
                    item = self.update()
                    result["changed"] = True
                    result["msg"] = "HealthCheckTcp updated"
            elif self.params["state"] == "absent" and self.existing is not None:
                self.delete()
                result["changed"] = True
                result["msg"] = "HealthCheckTcp deleted"

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
        disabled=dict(type="bool"),
        interval=dict(type="int"),
        metadata=dict(
            type="dict",
            options=dict(
                used_by=dict(
                    type="list",
                    elements="dict",
                    options=dict(
                        details=dict(type="dict"),
                        display_name=dict(type="str"),
                    ),
                ),
            ),
        ),
        name=dict(type="str", required=True),
        port=dict(type="int", required=True),
        retry_down=dict(type="int"),
        retry_up=dict(type="int"),
        tags=dict(type="dict"),
        timeout=dict(type="int"),
    )

    module = HealthCheckTcpModule(
        argument_spec=module_args,
        supports_check_mode=True,
        required_if=[("state", "present", ["name", "port"])],
    )

    module.run_command()


if __name__ == "__main__":
    main()
