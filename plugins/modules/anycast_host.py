#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: Infoblox Inc.
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: anycast_host
short_description: Manage Anycast Host
description:
    - Manages Anycast Host Configurations
version_added: 1.0.0
author: Infoblox Inc. (@infobloxopen)
options:
    id:
        description:
            - "ID of the object"
        type: int
        required: false
    state:
        description:
            - "Indicate desired state of the object"
        type: str
        required: false
        choices:
            - present
            - absent
        default: present
    anycast_config_refs:
        description: 
            - "An array of AnycastConfigRef structures; identifies the anycast configurations that this host is a member of."
        type: list
        elements: dict
        suboptions:
            anycast_config_name:
                description: 
                    - "Anycast configuration name."
                type: str
            routing_protocols:
                description:
                    - "Routing protocols enabled for this anycast configuration, on a particular host."
                choices:
                    - BGP
                    - OSPF
                    - OSPFv3
                type: list
                elements: str
    config_bgp:
        description: 
            - "Defines the BGP configuration for one anycast-enabled on-prem host."
        type: dict
        suboptions:
            asn:
                description: 
                    - "The autonomous system number of this BGP- or anycast-enabled on-prem host."
                type: int
                required: true
            holddown_secs:
                description: 
                    - "BGP route hold-down timer."
                type: int
                default: 90
            keep_alive_secs:
                description: 
                    - "BGP keep-alive timer."
                type: int
                default: 30
            neighbors:
                description: 
                    - "List of BGP Neighbor structs."
                type: list
                elements: dict
                suboptions:
                    asn:
                        description: 
                            - "The autonomous system number of this BGP neighbor."
                        type: int
                        required: true
                    ip_address:
                        description:
                            - "IPv4 address of the BGP neighbor."
                        type: str
                        required: true
                    max_hop_count:
                        description: 
                            - "Max hop count, if BGP multihop is enabled."
                        type: int
                    multihop:
                        description: 
                            - "Indicates whether BGP multihop is enabled @example true."
                        type: bool
                    password:
                        description: 
                            - "The BGP protocol access password for this BGP neighbor; max 25 characters long."
                        type: str
    config_ospf:
        description: 
            - "Defines the OSPF configuration for one anycast-enabled on-prem host."
        type: dict
        suboptions:
            area:
                description:
                    - "OSPF area identifier; usually in the format of an IPv4 address (although not an address itself)."
                type: str
                required: true
            area_type:
                description:
                    - "OSPF area type."
                choices:
                    - NSSA
                    - STANDARD
                    - STUB
                type: str
                required: true
            authentication_key:
                description: 
                    - "OSPF authentication key."
                type: str
            authentication_key_id:
                description: 
                    - "Numeric OSPF authentication key identifier."
                type: int
            authentication_type:
                description: 
                    - "OSPF authentication type."
                choices:
                    - Clear
                    - MD5
                type: str
                required: true
            cost:
                description: 
                    - "The explicit link cost for the interface."
                type: int
            dead_interval:
                description: 
                    - "The OSPF router's dead interval timer, in seconds; must be the same for all routers on the same network."
                default: 40
                type: int
            hello_interval:
                description: 
                    - "The period, in seconds, of the OSPF Hello packet sent by the OSPF router; must be the same for all routers on the same network."
                default: 10
                type: int
            interface:
                description:
                    - "Name of the interface that is configured with external IP address of the host. Example: 'eth0'"
                type: str
                required: true
            retransmit_interval:
                description: 
                    - "The period, in seconds, of retransmitting for the OSPF Database Description and Link State Requests."
                default: 5
                type: int
            transmit_delay:
                description:
                    - "The estimated time for transmitting link state advertisements."
                default: 1
                type: int
    config_ospfv3:
        description: 
            - "Defines the OSPFv3 configuration for one anycast-enabled on-prem host"
        type: dict
        suboptions:
            area:
                description:
                    - "OSPF area identifier; usually in the format of an IPv6 address (although not an address itself)"
                type: str
                required: true
            cost:
                description:
                    - "The explicit link cost for the interface"
                type: int
            dead_interval:
                description: 
                    - "The OSPF router's dead interval timer, in seconds; must be the same for all routers on the same network."
                default: 40
                type: int
            hello_interval:
                description: 
                    - "The period, in seconds, of the OSPF Hello packet sent by the OSPF router; must be the same for all routers on the same network."
                default: 10
                type: int
            interface:
                description:
                    - "Name of the interface that is configured with external IP address of the host. Example: 'eth0'"
                type: str
                required: true
            retransmit_interval:
                description: 
                    - "The period, in seconds, of retransmitting for the OSPF Database Description and Link State Requests."
                default: 5
                type: int
            transmit_delay:
                description: 
                    - "The estimated time for transmitting link state advertisements."
                default: 1
                type: int
    created_at:
        description: 
            - "The date and time this host was created in the anycast service database."
        type: str
    ip_address:
        description:
            - "IPv4 address of the on-prem host"
        type: str
    ipv6_address:
        description:
            - "IPv6 address of the on-prem host"
        type: str
    name:
        description: 
            - "A user-friendly name of the host. Example: 'dns-host-1', 'Central Office Server'"
        type: str
    updated_at:
        description: 
            - "The date and time this host was last updated in the anycast service database."
        type: str

extends_documentation_fragment:
    - infoblox.universal_ddi.common
"""  # noqa: E501

EXAMPLES = r"""
    - name: Retrieve Infra Host Information (required as parent)
      infoblox.universal_ddi.infra_host_info:
        filters:
            display_name: "example_infra_host"
      register: _infra_host_info

    - name: Create an Anycast Service (required as parent)
      infoblox.universal_ddi.infra_service:
        name: "example_anycast_service"
        pool_id: "{{ _infra_host_info.objects[0].pool_id }}"
        service_type: "anycast"
        state: "present"

    - name: Create an Anycast Configuration (required as parent)
      infoblox.universal_ddi.anycast_config:
        name: "example_anycast_config"
        anycast_ip_address: "10.0.0.0"
        service: "DNS"
        state: "present"

    - name: Update Anycast Host with Anycast Configuration References
      infoblox.universal_ddi.anycast_host:
        id: "{{ _infra_host_info.objects[0].legacy_id }}"
        name: "{{ _infra_host_info.objects[0].display_name }}"
        anycast_config_refs:
          - anycast_config_name: "example_anycast_config"
        state: "present"

    - name: Update Anycast Host with Routing protocols and their configurations
      infoblox.universal_ddi.anycast_host:
        id: "{{ _infra_host_info.objects[0].legacy_id }}"
        name: "{{ _infra_host_info.objects[0].display_name }}"
        anycast_config_refs:
          - anycast_config_name: "example_anycast_config"
            routing_protocols: ["OSPF", "BGP"]
        config_bgp:
          asn: 6500
          holddown_secs: 180
          neighbors:
            - asn: 6501
              ip_address: "172.28.4.198"
        config_ospf:
          area_type: "STANDARD"
          area: "10.10.0.1"
          authentication_type: "Clear"
          interface: "eth0"
          authentication_key: "YXV0aGV"
          hello_interval: 10
          dead_interval: 40
          retransmit_interval: 5
          transmit_delay: 1
        state: "present"

    - name: "Delete the Anycast Host"
      infoblox.universal_ddi.anycast_host:
        id: "{{ _infra_host_info.objects[0].legacy_id }}"
        state: "absent"

"""

RETURN = r"""
id:
    description:
        - "ID of the Anycast Host object"
    type: str
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
                        - "Routing protocols enabled for this anycast configuration, on a particular host."
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
                        - Stub
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
    from anycast import OnPremAnycastManagerApi, OnpremHost
    from infra_mgmt import HostsApi
    from universal_ddi_client import ApiException, NotFoundException

except ImportError:
    pass  # Handled by UniversalDDIAnsibleModule


class OnPremAnycastManagerModule(UniversalDDIAnsibleModule):
    def __init__(self, *args, **kwargs):
        super(OnPremAnycastManagerModule, self).__init__(*args, **kwargs)

        exclude = ["state", "csp_url", "api_key", "portal_url", "portal_key", "id"]
        self._payload_params = {k: v for k, v in self.params.items() if v is not None and k not in exclude}
        self._payload = OnpremHost.from_dict(self._payload_params)
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
                resp = OnPremAnycastManagerApi(self.client).get_onprem_host(self.params["id"])
                return resp.results

            except NotFoundException as e:
                if self.params["state"] == "present":
                    return None
                self.fail_json(msg=str(e))

            except ApiException as e:
                self.fail_json(msg=str(e))

        return None

    def create(self):
        """Retrieve the infra host using legacy ID (string) and update it with the Anycast service."""
        if self.check_mode:
            return None

        try:
            legacy_id = str(self.params["id"])

            # Retrieve the infra host using the legacy ID if the host exists
            filter_query = f"legacy_id=='{legacy_id}'"
            infra_host_resp = HostsApi(self.client).list(filter=filter_query)

            if not hasattr(infra_host_resp, "results") or infra_host_resp.results is None:
                infra_host_resp.results = []
            if not infra_host_resp.results:
                self.fail_json(msg=f"No Infra Host found with Legacy ID {legacy_id}.")

            infra_host = infra_host_resp.results[0]

            ip_address = infra_host.ip_address

            anycast_host_id = int(infra_host.legacy_id)

            # Update the payload with the retrieved IP address
            update_payload = OnpremHost(
                ip_address=ip_address,
                **self.payload_params,
            )

            # Update the Anycast host with the retrieved infra host data
            anycast_resp = OnPremAnycastManagerApi(self.client).update_onprem_host(
                id=anycast_host_id, body=update_payload
            )

            return anycast_resp.results.model_dump(by_alias=True, exclude_none=True)

        except ApiException as e:
            self.fail_json(
                msg=f"Error in creating Anycast Manager: {e.status} {e.reason}", details=f"Response Body: {e.body}"
            )

    def update(self):
        if self.check_mode:
            return None

        resp = OnPremAnycastManagerApi(self.client).update_onprem_host(id=self.existing.id, body=self.payload)
        return resp.results.model_dump(by_alias=True, exclude_none=True)

    def delete(self):
        if self.check_mode:
            return

        OnPremAnycastManagerApi(self.client).delete_onprem_host(self.existing.id)

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
                result["msg"] = "Anycast Host created"
            elif self.params["state"] == "present" and self.existing is not None:
                if self.payload_changed():
                    item = self.update()
                    result["changed"] = True
                    result["msg"] = "Anycast Host updated"
            elif self.params["state"] == "absent" and self.existing is not None:
                self.delete()
                result["changed"] = True
                result["msg"] = "Anycast Host deleted"

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
        id=dict(type="int", required=False),
        state=dict(type="str", required=False, choices=["present", "absent"], default="present"),
        anycast_config_refs=dict(
            type="list",
            elements="dict",
            options=dict(
                anycast_config_name=dict(type="str"),
                routing_protocols=dict(type="list", elements="str", choices=["BGP", "OSPF", "OSPFv3"]),
            ),
        ),
        config_bgp=dict(
            type="dict",
            options=dict(
                asn=dict(type="int", required=True),
                holddown_secs=dict(type="int", default=90),
                keep_alive_secs=dict(type="int", default=30),
                neighbors=dict(
                    type="list",
                    elements="dict",
                    options=dict(
                        asn=dict(type="int", required=True),
                        ip_address=dict(type="str", required=True),
                        max_hop_count=dict(type="int"),
                        multihop=dict(type="bool"),
                        password=dict(type="str", no_log=True),
                    ),
                ),
            ),
        ),
        config_ospf=dict(
            type="dict",
            options=dict(
                area=dict(type="str", required=True),
                area_type=dict(type="str", required=True, choices=["STANDARD", "STUB", "NSSA"]),
                authentication_key=dict(type="str", no_log=True),
                authentication_key_id=dict(type="int"),
                authentication_type=dict(type="str", required=True, choices=["Clear", "MD5"]),
                cost=dict(type="int"),
                dead_interval=dict(type="int", default=40),
                hello_interval=dict(type="int", default=10),
                interface=dict(type="str", required=True),
                retransmit_interval=dict(type="int", default=5),
                transmit_delay=dict(type="int", default=1),
            ),
        ),
        config_ospfv3=dict(
            type="dict",
            options=dict(
                area=dict(type="str", required=True),
                cost=dict(type="int"),
                dead_interval=dict(type="int", default=40),
                hello_interval=dict(type="int", default=10),
                interface=dict(type="str", required=True),
                retransmit_interval=dict(type="int", default=5),
                transmit_delay=dict(type="int", default=1),
            ),
        ),
        ip_address=dict(type="str"),
        ipv6_address=dict(type="str"),
        name=dict(type="str"),
    )

    module = OnPremAnycastManagerModule(
        argument_spec=module_args,
        supports_check_mode=True,
        required_if=[("state", "present", ["id"])],
    )

    module.run_command()


if __name__ == "__main__":
    main()
