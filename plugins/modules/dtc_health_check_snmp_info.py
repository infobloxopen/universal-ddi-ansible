#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: Infoblox Inc.
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: dtc_health_check_snmp_info
short_description: Retrieve HealthCheckSnmp
description:
    - Retrieve HealthCheckSnmp
version_added: 1.0.0
author: Infoblox Inc. (@infobloxopen)
options:
    id:
        description:
            - ID of the object
        type: str
        required: false
    filters:
        description:
            - Filter dict to filter objects
        type: dict
        required: false
    filter_query:
        description:
            - Filter query to filter objects
        type: str
        required: false
    inherit:
        description:
            - Return inheritance information
        type: str
        required: false
        choices:
            - full
            - partial
            - none
        default: full
    tag_filters:
        description:
            - Filter dict to filter objects by tags
        type: dict
        required: false
    tag_filter_query:
        description:
            - Filter query to filter objects by tags
        type: str
        required: false

extends_documentation_fragment:
    - infoblox.universal_ddi.common
"""  # noqa: E501

RETURN = r"""
id:
    description:
        - ID of the HealthCheckSnmp object
    type: str
    returned: Always
objects:
    description:
        - HealthCheckSnmp object
    type: list
    elements: dict
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

EXAMPLES = r"""
    - name: Get SNMP Health Check by ID
      infoblox.universal_ddi.dtc_health_check_snmp_info:
        id: "{{ health_check_id }}"

    - name: Get SNMP Health Check by filters (name)
      infoblox.universal_ddi.dtc_health_check_snmp_info:
        filters:
          name: "example-snmp-health-check"

    - name: Get SNMP Health Check by filter query
      infoblox.universal_ddi.dtc_health_check_snmp_info:
        filter_query: "name=='example-snmp-health-check'"

    - name: Get SNMP Health Check by tag filters
      infoblox.universal_ddi.dtc_health_check_snmp_info:
        tag_filters:
          environment: "production"

    - name: Get all SNMP Health Checks
      infoblox.universal_ddi.dtc_health_check_snmp_info:
"""

from ansible_collections.infoblox.universal_ddi.plugins.module_utils.modules import UniversalDDIAnsibleModule

try:
    from dtc import HealthCheckSnmpApi
    from universal_ddi_client import ApiException, NotFoundException
except ImportError:
    pass  # Handled by UniversalDDIAnsibleModule


class HealthCheckSnmpInfoModule(UniversalDDIAnsibleModule):
    def __init__(self, *args, **kwargs):
        super(HealthCheckSnmpInfoModule, self).__init__(*args, **kwargs)
        self._existing = None
        self._limit = 1000

    def find_by_id(self):
        try:
            resp = HealthCheckSnmpApi(self.client).read(self.params["id"])
            return [resp.result]
        except NotFoundException as e:
            return None

    def find(self):
        if self.params["id"] is not None:
            return self.find_by_id()

        filter_str = None
        if self.params["filters"] is not None:
            filter_str = " and ".join([f"{k}=='{v}'" for k, v in self.params["filters"].items()])
        elif self.params["filter_query"] is not None:
            filter_str = self.params["filter_query"]

        tag_filter_str = None
        if self.params["tag_filters"] is not None:
            tag_filter_str = " and ".join([f"{k}=='{v}'" for k, v in self.params["tag_filters"].items()])
        elif self.params["tag_filter_query"] is not None:
            tag_filter_str = self.params["tag_filter_query"]

        all_results = []
        offset = 0

        while True:
            try:
                resp = HealthCheckSnmpApi(self.client).list(
                    offset=offset, limit=self._limit, filter=filter_str, tfilter=tag_filter_str
                )

                # If no results, set results to empty list
                if not resp.results:
                    resp.results = []

                all_results.extend(resp.results)

                if len(resp.results) < self._limit:
                    break
                offset += self._limit

            except ApiException as e:
                self.fail_json(msg=f"Failed to execute command: {e.status} {e.reason} {e.body}")

        return all_results

    def run_command(self):
        result = dict(objects=[])

        if self.check_mode:
            self.exit_json(**result)

        find_results = self.find()

        all_results = []
        for r in find_results:
            all_results.append(r.model_dump(by_alias=True, exclude_none=True))

        result["objects"] = all_results
        self.exit_json(**result)


def main():
    # define available arguments/parameters a user can pass to the module
    module_args = dict(
        id=dict(type="str", required=False),
        filters=dict(type="dict", required=False),
        filter_query=dict(type="str", required=False),
        inherit=dict(type="str", required=False, choices=["full", "partial", "none"], default="full"),
        tag_filters=dict(type="dict", required=False),
        tag_filter_query=dict(type="str", required=False),
    )

    module = HealthCheckSnmpInfoModule(
        argument_spec=module_args,
        supports_check_mode=True,
        mutually_exclusive=[
            ["id", "filters", "filter_query"],
            ["id", "tag_filters", "tag_filter_query"],
        ],
    )
    module.run_command()


if __name__ == "__main__":
    main()
