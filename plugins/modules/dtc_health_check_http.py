#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: Infoblox Inc.
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: dtc_health_check_http
short_description: Manages a DTC HTTP Health Check
description:
    - Manages a DTC HTTP Health Check.
version_added: 1.2.0
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
    check_response_body:
        description:
            - "Optional. Flag which enables checking of the HTTP response body content. Defaults to I(false)."
        type: bool
        default: false
    check_response_body_negative:
        description:
            - "Optional. Flag which changes the meaning of the regex match result. If set to I(true), the response is valid if regular expression matches not found. Defaults to I(false)."
            - "The flag is currently not supported."
        type: bool
        default: false
    check_response_body_regex:
        description:
            - "Optional. Regular expression to search for a string in the HTTP response body. Error if empty while I(check_response_body) is I(true). Defaults to empty."
        type: str
        default: ""
    check_response_header:
        description:
            - "Optional. Flag which enables checking of the HTTP response header(s) content. Defaults to I(false)."
        type: bool
        default: false
    check_response_header_negative:
        description:
            - "Optional. Flag which changes the meaning of the header regexes match result. If set to I(true), neither expression matches must be found in their respective headers for the headers to be considered valid. Defaults to I(false)."
        type: bool
        default: false
    check_response_header_regexes:
        description:
            - "Optional. List of (header, regular expression) pairs. All expression matches must be found in their respective headers for the headers to be considered valid. Error if empty while I(check_response_header) is I(true). Defaults to empty."
        type: list
        elements: dict
        suboptions:
            header:
                description:
                    - "HTTP header name."
                type: str
            regex:
                description:
                    - "Regular expression to match against HTTP header value."
                type: str
        default: []
    codes:
        description:
            - "Optional. Response Status Codes meaning the health check is successful. If empty, any code means success. Individual codes and code ranges are supported, ex. \"102,105-107,109-110,120\"."
        type: str
    comment:
        description:
            - "Optional. Comment for B(HTTPHealthCheck)."
        type: str
    disabled:
        description:
            - "Optional. Flag which enables/disables B(HTTPHealthCheck). Defaults to I(false)."
        type: bool
        default: false
    https:
        description:
            - "Optional. Flag which enables Hypertext Transfer Protocol Secure (HTTPS) in a health check. Defaults to I(false)."
        type: bool
        default: false
    interval:
        description:
            - "Optional. Interval value in seconds. The health check runs only for the specified interval and it is measured from the beginning of the previous check cycle. Defaults to I(15)."
        type: int
        default: 15
    name:
        description:
            - "Display name of B(HTTPHealthCheck)."
        type: str
        required: true
    port:
        description:
            - "Destination TCP port of B(HTTPHealthCheck)."
        type: int
        required: true
    request:
        description:
            - "HTTP request in a text format, it consists of HTTP method, request target, HTTP headers, request body."
        type: str
        required: true
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
            - "Optional. The tags for B(HTTPHealthCheck) in JSON format."
        type: dict
    timeout:
        description:
            - "Optional. Timeout value in seconds. The health check waits for the specified number of seconds after sending a request. If it does not receive a response within the number of seconds, then the health check is considered as failed. Defaults to I(10)."
        type: int
        default: 10

extends_documentation_fragment:
    - infoblox.universal_ddi.common
"""  # noqa: E501

EXAMPLES = r"""
    - name: Create an HTTP Health Check
      infoblox.universal_ddi.dtc_health_check_http:
        name: "example_http_health_check"
        port: 80
        request: "POST / HTTP/1.1\r\nHost: localhost\r\n\r\n"
        state: "present"
      register: http_health_check

    - name: Create an HTTP Health Check with additional parameters
      infoblox.universal_ddi.dtc_health_check_http:
        name: "example_http_health_check"
        port: 8080
        request: "POST / HTTP/1.1\r\nHost: localhost\r\n\r\n"
        interval: 15
        retry_down: 2
        retry_up: 2
        timeout: 10
        disabled: false
        tags:
            location: "site-1"
        state: "present"

    - name: Delete HTTP Health Check
      infoblox.universal_ddi.dtc_health_check_http:
        name: "example_http_health_check"
        port: 80
        request: "DELETE / HTTP/1.1\r\nHost: localhost\r\n\r\n"
        state: "absent"
"""

RETURN = r"""
id:
    description:
        - ID of the HealthCheckHttp object
    type: str
    returned: Always
item:
    description:
        - HealthCheckHttp object
    type: complex
    returned: Always
    contains:
        check_response_body:
            description:
                - "Optional. Flag which enables checking of the HTTP response body content. Defaults to I(false)."
            type: bool
            returned: Always
        check_response_body_negative:
            description:
                - "Optional. Flag which changes the meaning of the regex match result. If set to I(true), the response is valid if regular expression matches not found. Defaults to I(false)."
                - "The flag is currently not supported."
            type: bool
            returned: Always
        check_response_body_regex:
            description:
                - "Optional. Regular expression to search for a string in the HTTP response body. Error if empty while I(check_response_body) is I(true). Defaults to empty."
            type: str
            returned: Always
        check_response_header:
            description:
                - "Optional. Flag which enables checking of the HTTP response header(s) content. Defaults to I(false)."
            type: bool
            returned: Always
        check_response_header_negative:
            description:
                - "Optional. Flag which changes the meaning of the header regexes match result. If set to I(true), neither expression matches must be found in their respective headers for the headers to be considered valid. Defaults to I(false)."
            type: bool
            returned: Always
        check_response_header_regexes:
            description:
                - "Optional. List of (header, regular expression) pairs. All expression matches must be found in their respective headers for the headers to be considered valid. Error if empty while I(check_response_header) is I(true). Defaults to empty."
            type: list
            returned: Always
            elements: dict
            contains:
                header:
                    description:
                        - "HTTP header name."
                    type: str
                    returned: Always
                regex:
                    description:
                        - "Regular expression to match against HTTP header value."
                    type: str
                    returned: Always
        codes:
            description:
                - "Optional. Response Status Codes meaning the health check is successful. If empty, any code means success. Individual codes and code ranges are supported, ex. \"102,105-107,109-110,120\"."
            type: str
            returned: Always
        comment:
            description:
                - "Optional. Comment for B(HTTPHealthCheck)."
            type: str
            returned: Always
        disabled:
            description:
                - "Optional. Flag which enables/disables B(HTTPHealthCheck). Defaults to I(false)."
            type: bool
            returned: Always
        https:
            description:
                - "Optional. Flag which enables Hypertext Transfer Protocol Secure (HTTPS) in a health check. Defaults to I(false)."
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
                - "Output only. B(HTTPHealthCheck) metadata. Defaults to empty object and should be explicitly requested using field selection."
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
                - "Display name of B(HTTPHealthCheck)."
            type: str
            returned: Always
        port:
            description:
                - "Destination TCP port of B(HTTPHealthCheck)."
            type: int
            returned: Always
        request:
            description:
                - "HTTP request in a text format, it consists of HTTP method, request target, HTTP headers, request body."
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
                - "Optional. The tags for B(HTTPHealthCheck) in JSON format."
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
    from dtc import HealthCheckHttpApi, HTTPHealthCheck
    from universal_ddi_client import ApiException, NotFoundException
except ImportError:
    pass  # Handled by UniversalDDIAnsibleModule


class HealthCheckHttpModule(UniversalDDIAnsibleModule):
    def __init__(self, *args, **kwargs):
        super(HealthCheckHttpModule, self).__init__(*args, **kwargs)

        exclude = ["state", "csp_url", "api_key", "portal_url", "portal_key", "id"]
        self._payload_params = {k: v for k, v in self.params.items() if v is not None and k not in exclude}
        self._payload = HTTPHealthCheck.from_dict(self._payload_params)
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
                resp = HealthCheckHttpApi(self.client).read(self.params["id"])
                return resp.result
            except NotFoundException as e:
                if self.params["state"] == "absent":
                    return None
                raise e
        else:
            filter = f"name=='{self.params['name']}'"
            resp = HealthCheckHttpApi(self.client).list(filter=filter)

            # If no results, set results to empty list
            if not resp.results:
                resp.results = []

            if len(resp.results) == 1:
                return resp.results[0]
            if len(resp.results) > 1:
                self.fail_json(msg=f"Found multiple HealthCheckHttp: {resp.results}")
            if len(resp.results) == 0:
                return None

    def create(self):
        if self.check_mode:
            return None

        resp = HealthCheckHttpApi(self.client).create(body=self.payload)
        return resp.result.model_dump(by_alias=True, exclude_none=True)

    def update(self):
        if self.check_mode:
            return None

        resp = HealthCheckHttpApi(self.client).update(id=self.existing.id, body=self.payload)
        return resp.result.model_dump(by_alias=True, exclude_none=True)

    def delete(self):
        if self.check_mode:
            return

        HealthCheckHttpApi(self.client).delete(self.existing.id)

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
                result["msg"] = "HealthCheckHttp created"
            elif self.params["state"] == "present" and self.existing is not None:
                if self.payload_changed():
                    item = self.update()
                    result["changed"] = True
                    result["msg"] = "HealthCheckHttp updated"
            elif self.params["state"] == "absent" and self.existing is not None:
                self.delete()
                result["changed"] = True
                result["msg"] = "HealthCheckHttp deleted"

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
        check_response_body=dict(type="bool", default=False),
        check_response_body_negative=dict(type="bool", default=False),
        check_response_body_regex=dict(type="str", default=""),
        check_response_header=dict(type="bool", default=False),
        check_response_header_negative=dict(type="bool", default=False),
        check_response_header_regexes=dict(
            type="list",
            elements="dict",
            options=dict(
                header=dict(type="str"),
                regex=dict(type="str"),
            ),
            default=[],
        ),
        codes=dict(type="str"),
        comment=dict(type="str"),
        disabled=dict(type="bool", default=False),
        https=dict(type="bool", default=False),
        interval=dict(type="int", default=15),
        name=dict(type="str", required=True),
        port=dict(type="int", required=True),
        request=dict(type="str", required=True),
        retry_down=dict(type="int", default=1),
        retry_up=dict(type="int", default=1),
        tags=dict(type="dict"),
        timeout=dict(type="int", default=10),
    )

    module = HealthCheckHttpModule(
        argument_spec=module_args,
        supports_check_mode=True,
        required_if=[("state", "present", ["name", "port", "request"])],
    )

    if module.params["check_response_header"] and not module.params.get("check_response_header_regexes"):
        module.fail_json(
            msg="'check_response_header_regexes' must be provided and non-empty when 'check_response_header' is true."
        )

    if module.params["check_response_body"] and not module.params.get("check_response_body_regex"):
        module.fail_json(
            msg="'check_response_body_regex' must be provided and non-empty when 'check_response_body' is true."
        )

    module.run_command()


if __name__ == "__main__":
    main()
