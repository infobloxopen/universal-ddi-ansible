#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: Infoblox Inc.
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: anycast_host_info
short_description: "Retrieves Anycast Host Information"
description:
    - "Retrieves Anycast Host Information by its ID."
version_added: 1.0.0
author: Infoblox Inc. (@infobloxopen)
options:
    id:
        description:
            - "ID of the object"
        type: int
        required: true
        
extends_documentation_fragment:
    - infoblox.universal_ddi.common
"""  # noqa: E501

EXAMPLES = r"""
    - name: Get Anycast Host Information by ID
      infoblox.universal_ddi.anycast_host_info:
        id: "{{ _infra_host_info.objects[0].legacy_id | int }}"

"""
RETURN = r"""
id:
    description:
        - "ID of the Anycast Host object"
    type: int
    returned: Always
item:
    description:
        - "Anycast Host object"
    type: complex
    returned: Always
    contains:
        anycast_config_refs:
            description: 
                - "An array of AnycastConfigRef structures; identifies the anycast configurations that this host is a member of."
            type: list
            returned: Always
            elements: dict
            contains:
                anycast_config_name:
                    description: 
                        - "Anycast configuration name."
                    type: str
                    returned: Always
                routing_protocols:
                    description:
                        - "Routing protocols enabled for this anycast configuration, on a particular host. Valid protocol names are \"BGP\", \"OSPF\"/\"OSPFv2\", \"OSPFv3\"."
                    choices:
                        - BGP
                        - OSPF
                        - OSPFv3
                    type: list
                    returned: Always
        config_bgp:
            description: 
                - "Defines the BGP configuration for one anycast-enabled on-prem host."
            type: dict
            returned: Always
            contains:
                asn:
                    description: 
                        - "The autonomous system number of this BGP- or anycast-enabled on-prem host."
                    type: int
                    returned: Always
                asn_text:
                  description:
                    - "Examples:"
                    - V(ASDOT       | ASPLAIN      | INTEGER       | VALID/INVALID)
                    - V(0.1         | 1            | 1             |     Valid)
                    - V(1           | 1            | 1             |     Valid)
                    - V(65535       | 65535        | 65535         |     Valid)
                    - V(0.65535     | 65535        | 65535         |     Valid)
                    - V(1.0         | 65536        | 65536         |     Valid)
                    - V(1.1         | 65537        | 65537         |     Valid)
                    - V(1.65535     | 131071       | 131071        |     Valid)
                    - V(65535.0     | 4294901760   | 4294901760    |     Valid)
                    - V(65535.1     | 4294901761   | 4294901761    |     Valid)
                    - V(65535.65535 | 4294967295   | 4294967295    |     Valid)
                    - V(0.65536     |              |               |   Invalid)
                    - V(65535.655536|              |               |   Invalid)
                    - V(65536.0     |              |               |   Invalid)
                    - V(65536.65535 |              |               |   Invalid)
                    - V(            | 4294967296   | 4294967296    |   Invalid)
                  type: str
                  returned: Always
                holddown_secs:
                    description: 
                        - "BGP route hold-down timer."
                    type: int
                    returned: Always
                keep_alive_secs:
                    description: 
                        - "BGP keep-alive timer."
                    type: int
                    returned: Always
                link_detect:
                    description: 
                        - "Enable/disable link detection. Example: true"
                    type: bool
                    returned: Always
                neighbors:
                    description: 
                        - "Describes one of the BGP neighbors that participate in the BGP configuration for one anycast-enabled on-prem."
                    type: list
                    returned: Always
                    elements: dict
                    contains:
                        asn:
                            description: 
                                - "The autonomous system number of this BGP neighbor."
                            type: int
                            returned: Always
                        asn_text:
                            description:
                                - "Examples:"
                                - V(ASDOT       | ASPLAIN      | INTEGER       | VALID/INVALID)
                                - V(0.1         | 1            | 1             |     Valid)
                                - V(1           | 1            | 1             |     Valid)
                                - V(65535       | 65535        | 65535         |     Valid)
                                - V(0.65535     | 65535        | 65535         |     Valid)
                                - V(1.0         | 65536        | 65536         |     Valid)
                                - V(1.1         | 65537        | 65537         |     Valid)
                                - V(1.65535     | 131071       | 131071        |     Valid)
                                - V(65535.0     | 4294901760   | 4294901760    |     Valid)
                                - V(65535.1     | 4294901761   | 4294901761    |     Valid)
                                - V(65535.65535 | 4294967295   | 4294967295    |     Valid)
                                - V(0.65536     |              |               |   Invalid)
                                - V(65535.655536|              |               |   Invalid)
                                - V(65536.0     |              |               |   Invalid)
                                - V(65536.65535 |              |               |   Invalid)
                                - V(            | 4294967296   | 4294967296    |   Invalid)
                            type: str
                            returned: Always
                        ip_address:
                            description:
                                - "IPv4 address of the BGP neighbor."
                            type: str
                            returned: Always
                        max_hop_count:
                            description: 
                                - "Max hop count, if BGP multihop is enabled."
                            type: int
                            returned: Always
                        multihop:
                            description: 
                                - "Indicates whether BGP multihop is enabled. Example: True"
                            type: bool
                            returned: Always
                        password:
                            description: 
                                - "The BGP protocol access password for this BGP neighbor; max 25 characters long."
                            type: str
                            returned: Always
                preamble:
                    description:
                        - "Any predefined BGP configuration, with embedded new lines; the preamble will be prepended to the generated BGP configuration."
                    type: str
                    returned: Always
        config_ospf:
            description: 
                - "Defines the OSPF configuration for one anycast-enabled on-prem host."
            type: dict
            returned: Always
            contains:
                area:
                    description:
                        - "OSPF area identifier; usually in the format of an IPv4 address (although not an address itself)"
                    type: str
                    returned: Always
                area_type:
                    description: 
                        - "OSPF area type."
                    choices:
                        - NSSA
                        - STANDARD
                        - STUB
                    type: str
                    returned: Always
                authentication_key:
                    description: 
                        - "OSPF authentication key."
                    type: str
                    returned: Always
                authentication_key_id:
                    description: 
                        - "Numeric OSPF authentication key identifier."
                    type: int
                    returned: Always
                authentication_type:
                    description: 
                        - "OSPF authentication type."
                    choices:
                        - Clear
                        - MD5
                    type: str
                    returned: Always
                cost:
                    description: 
                        - "The explicit link cost for the interface"
                    type: int
                    returned: Always
                dead_interval:
                    description: 
                        - "The OSPF router's dead interval timer, in seconds; must be the same for all routers on the same network."
                    type: int
                    returned: Always
                hello_interval:
                    description: 
                        - "The period, in seconds, of the OSPF Hello packet sent by the OSPF router; must be the same for all routers on the same network."
                    type: int
                    returned: Always
                interface:
                    description:
                        - "Name of the interface that is configured with external IP address of the host"
                    type: str
                    returned: Always
                preamble:
                    description:
                        - "Any predefined OSPF configuration, with embedded new lines; the preamble will be prepended to the generated BGP configuration."
                    type: str
                    returned: Always
                retransmit_interval:
                    description: 
                        - "The period, in seconds, of retransmitting for the OSPF Database Description and Link State Requests."
                    type: int
                    returned: Always
                transmit_delay:
                    description: 
                        - "The estimated time for transmitting link state advertisements."
                    type: int
                    returned: Always
        config_ospfv3:
            description: 
                - "Defines the OSPFv3 configuration for one anycast-enabled on-prem host."
            type: dict
            returned: Always
            contains:
                area:
                    description:
                        - "OSPF area identifier; usually in the format of an IPv6 address (although not an address itself)"
                    type: str
                    returned: Always
                cost:
                    description: 
                        - "The explicit link cost for the interface"
                    type: int
                    returned: Always
                dead_interval:
                    description: 
                        - "The OSPF router's dead interval timer, in seconds; must be the same for all routers on the same network."
                    type: int
                    returned: Always
                hello_interval:
                    description: 
                        - "The period, in seconds, of the OSPF Hello packet sent by the OSPF router; must be the same for all routers on the same network."
                    type: int
                    returned: Always
                interface:
                    description:
                        - "Name of the interface that is configured with external IP address of the host"
                    type: str
                    returned: Always
                retransmit_interval:
                    description: 
                        - "The period, in seconds, of retransmitting for the OSPF Database Description and Link State Requests."
                    type: int
                    returned: Always
                transmit_delay:
                    description: 
                        - "The estimated time for transmitting link state advertisements."
                    type: int
                    returned: Always
        created_at:
            description: 
                - "The date and time this host was created in the anycast service database."
            type: str
            returned: Always
        id:
            description: 
                - "Numeric host identifier."
            type: int
            returned: Always
        ip_address:
            description:
                - "IPv4 address of the on-prem host"
            type: str
            returned: Always
        ipv6_address:
            description:
                - "IPv6 address of the on-prem host"
            type: str
            returned: Always
        name:
            description: 
                - "A user-friendly name of the host. Example: 'dns-host-1', 'Central Office Server'"
            type: str
            returned: Always
        updated_at:
            description: 
                - "The date and time this host was last updated in the anycast service database."
            type: str
            returned: Always
"""  # noqa: E501

from ansible_collections.infoblox.universal_ddi.plugins.module_utils.modules import UniversalDDIAnsibleModule

try:
    from anycast import OnPremAnycastManagerApi
    from universal_ddi_client import ApiException, NotFoundException
except ImportError:
    pass  # Handled by UniversalDDIAnsibleModule


class OnPremAnycastManagerInfoModule(UniversalDDIAnsibleModule):
    def __init__(self, *args, **kwargs):
        super(OnPremAnycastManagerInfoModule, self).__init__(*args, **kwargs)
        self._existing = None
        self._limit = 1000

    def find_by_id(self):
        try:
            resp = OnPremAnycastManagerApi(self.client).get_onprem_host(self.params["id"])
            return resp.results if resp.results else None  # Return object or None
        except NotFoundException:
            return None

    def find(self):
        if self.params["id"] is not None:
            result = self.find_by_id()
            if isinstance(result, list):
                return result
            return [result] if result else []

        try:
            resp = OnPremAnycastManagerApi(self.client).get_onprem_host(self.params["id"])

            if not resp.results:
                return []  # Return an empty list instead of None

            return [resp.results]  # Ensure result is returned inside a list

        except ApiException as e:
            self.fail_json(msg=f"Failed to execute command: {e.status} {e.reason} {e.body}")

    def run_command(self):
        result = dict(objects=[])

        if self.check_mode:
            self.exit_json(**result)

        find_results = self.find()  # Guaranteed to return a list

        all_results = []
        for r in find_results:
            if r is not None:  # Ensure no None values are processed
                all_results.append(r.model_dump(by_alias=True, exclude_none=True))

        result["objects"] = all_results
        self.exit_json(**result)


def main():
    module_args = dict(
        id=dict(type="int", required=True),
    )

    module = OnPremAnycastManagerInfoModule(
        argument_spec=module_args,
        supports_check_mode=True,
    )
    module.run_command()


if __name__ == "__main__":
    main()
