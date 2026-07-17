#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: Infoblox Inc.
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: dns_view_bulk_copy
short_description: Copy DNS objects from one view to another
description:
    - Copy DNS objects from one view to another
version_added: 1.1.0
author: Infoblox Inc. (@infobloxopen)
options:
    id:
        description:
            - ID of the object
        type: str
        required: false
    auth_zone_config:
        description:
            - "Optional. Authoritative zone related configuration."
        type: dict
        suboptions:
            external_primaries:
                description:
                    - "Optional. DNS primaries external to BloxOne DDI. Order is not significant."
                type: list
                elements: dict
                suboptions:
                    address:
                        description:
                            - "Optional. Required only if I(type) is I(server). IP Address of nameserver."
                        type: str
                    fqdn:
                        description:
                            - "Optional. Required only if I(type) is I(server). FQDN of nameserver."
                        type: str
                    nsg:
                        description:
                            - "The resource identifier."
                        type: str
                    tsig_enabled:
                        description:
                            - "Optional. If enabled, secondaries will use the configured TSIG key when requesting a zone transfer from this primary."
                        type: bool
                    tsig_key:
                        description:
                            - "Optional. TSIG key."
                            - "Error if empty while I(tsig_enabled) is I(true)."
                        type: dict
                        suboptions:
                            algorithm:
                                description:
                                    - "TSIG key algorithm."
                                type: str
                                choices:
                                    - "hmac_sha256"
                                    - "hmac_sha1"
                                    - "hmac_sha224"
                                    - "hmac_sha384"
                                    - "hmac_sha512"
                            comment:
                                description:
                                    - "Comment for TSIG key."
                                type: str
                            key:
                                description:
                                    - "The resource identifier."
                                type: str
                            name:
                                description:
                                    - "TSIG key name, FQDN."
                                type: str
                            secret:
                                description:
                                    - "TSIG key secret, base64 string."
                                type: str
                    type:
                        description:
                            - "Allowed values:"
                            - "* I(nsg),"
                            - "* I(primary)."
                        type: str
                        choices:
                            - nsg
                            - primary
            external_secondaries:
                description:
                    - "DNS secondaries external to BloxOne DDI. Order is not significant."
                type: list
                elements: dict
                suboptions:
                    address:
                        description:
                            - "IP Address of nameserver."
                        type: str
                    fqdn:
                        description:
                            - "FQDN of nameserver."
                        type: str
                    stealth:
                        description:
                            - "If enabled, the NS record and glue record will NOT be automatically generated according to secondaries nameserver assignment."
                            - "Default: I(false)"
                        type: bool
                    tsig_enabled:
                        description:
                            - "If enabled, secondaries will use the configured TSIG key when requesting a zone transfer."
                            - "Default: I(false)"
                        type: bool
                    tsig_key:
                        description:
                            - "TSIG key."
                            - "Error if empty while I(tsig_enabled) is I(true)."
                        type: dict
                        suboptions:
                            algorithm:
                                description:
                                    - "TSIG key algorithm."
                                type: str
                                choices:
                                    - "hmac_sha256"
                                    - "hmac_sha1"
                                    - "hmac_sha224"
                                    - "hmac_sha384"
                                    - "hmac_sha512"
                            comment:
                                description:
                                    - "Comment for TSIG key."
                                type: str
                            key:
                                description:
                                    - "The resource identifier."
                                type: str
                            name:
                                description:
                                    - "TSIG key name, FQDN."
                                type: str
                            secret:
                                description:
                                    - "TSIG key secret, base64 string."
                                type: str
            internal_secondaries:
                description:
                    - "Optional. BloxOne DDI hosts acting as internal secondaries. Order is not significant."
                type: list
                elements: dict
                suboptions:
                    host:
                        description:
                            - "The resource identifier."
                        type: str
            nsgs:
                description:
                    - "The resource identifier."
                type: list
                elements: str
    forward_zone_config:
        description:
            - "Optional. Forward zone related configuration."
        type: dict
        suboptions:
            external_forwarders:
                description:
                    - "Optional. External DNS servers to forward to. Order is not significant."
                type: list
                elements: dict
                suboptions:
                    address:
                        description:
                            - "Server IP address."
                        type: str
                    fqdn:
                        description:
                            - "Server FQDN."
                        type: str
            hosts:
                description:
                    - "The resource identifier."
                type: list
                elements: str
            internal_forwarders:
                description:
                    - "The resource identifier."
                type: list
                elements: str
            nsgs:
                description:
                    - "The resource identifier."
                type: list
                elements: str
    recursive:
        description:
            - "Indicates whether child objects should be copied or not."
            - "Defaults to I(false). Reserved for future use."
        type: bool
        default: false
    resources:
        description:
            - "The resource identifier."
        type: list
        elements: str
        required: true
    secondary_zone_config:
        description:
            - "Optional. Secondary zone related configuration."
        type: dict
        suboptions:
            external_primaries:
                description:
                    - "Optional. DNS primaries external to BloxOne DDI. Order is not significant."
                type: list
                elements: dict
                suboptions:
                    address:
                        description:
                            - "Optional. Required only if I(type) is I(server). IP Address of nameserver."
                        type: str
                    fqdn:
                        description:
                            - "Optional. Required only if I(type) is I(server). FQDN of nameserver."
                        type: str
                    nsg:
                        description:
                            - "The resource identifier."
                        type: str
                    tsig_enabled:
                        description:
                            - "Optional. If enabled, secondaries will use the configured TSIG key when requesting a zone transfer from this primary."
                        type: bool
                    tsig_key:
                        description:
                            - "Optional. TSIG key."
                            - "Error if empty while I(tsig_enabled) is I(true)."
                        type: dict
                        suboptions:
                            algorithm:
                                description:
                                    - "TSIG key algorithm."
                                type: str
                                choices:
                                    - "hmac_sha256"
                                    - "hmac_sha1"
                                    - "hmac_sha224"
                                    - "hmac_sha384"
                                    - "hmac_sha512"
                            comment:
                                description:
                                    - "Comment for TSIG key."
                                type: str
                            key:
                                description:
                                    - "The resource identifier."
                                type: str
                            name:
                                description:
                                    - "TSIG key name, FQDN."
                                type: str
                            secret:
                                description:
                                    - "TSIG key secret, base64 string."
                                type: str
                    type:
                        description:
                            - "Allowed values:"
                            - "* I(nsg),"
                            - "* I(primary)."
                        type: str
                        choices:
                            - nsg
                            - primary
            external_secondaries:
                description:
                    - "DNS secondaries external to BloxOne DDI. Order is not significant."
                type: list
                elements: dict
                suboptions:
                    address:
                        description:
                            - "IP Address of nameserver."
                        type: str
                    fqdn:
                        description:
                            - "FQDN of nameserver."
                        type: str
                    stealth:
                        description:
                            - "If enabled, the NS record and glue record will NOT be automatically generated according to secondaries nameserver assignment."
                            - "Default: I(false)"
                        type: bool
                    tsig_enabled:
                        description:
                            - "If enabled, secondaries will use the configured TSIG key when requesting a zone transfer."
                            - "Default: I(false)"
                        type: bool
                    tsig_key:
                        description:
                            - "TSIG key."
                            - "Error if empty while I(tsig_enabled) is I(true)."
                        type: dict
                        suboptions:
                            algorithm:
                                description:
                                    - "TSIG key algorithm."
                                type: str
                                choices:
                                    - "hmac_sha256"
                                    - "hmac_sha1"
                                    - "hmac_sha224"
                                    - "hmac_sha384"
                                    - "hmac_sha512"
                            comment:
                                description:
                                    - "Comment for TSIG key."
                                type: str
                            key:
                                description:
                                    - "The resource identifier."
                                type: str
                            name:
                                description:
                                    - "TSIG key name, FQDN."
                                type: str
                            secret:
                                description:
                                    - "TSIG key secret, base64 string."
                                type: str
            internal_secondaries:
                description:
                    - "Optional. BloxOne DDI hosts acting as internal secondaries. Order is not significant."
                type: list
                elements: dict
                suboptions:
                    host:
                        description:
                            - "The resource identifier."
                        type: str
            nsgs:
                description:
                    - "The resource identifier."
                type: list
                elements: str
    skip_on_error:
        description:
            - "Indicates whether copying should skip object in case of error and continue with next, or abort copying in case of error."
            - "Defaults to I(false)."
        type: bool
    target:
        description:
            - "The resource identifier."
        type: str
        required: true

extends_documentation_fragment:
    - infoblox.universal_ddi.common
"""  # noqa: E501

EXAMPLES = r"""
- name: Create a Source View
  infoblox.universal_ddi.dns_view:
    name: "example_source_view"
    state: present
  register: view_source

- name: Create a destination View
  infoblox.universal_ddi.dns_view:
    name: "example_dest_view"
    state: present
  register: view_dest

- name: Create an Auth Zone in a view
  infoblox.universal_ddi.dns_auth_zone:
    fqdn: "example.com."
    view:  "{{ view_source.id }}"
    primary_type: cloud
    state: present
  register: auth_zone

- name: Create a DNS Bulk Copy Job.
  infoblox.universal_ddi.dns_view_bulk_copy:
    resources:
      - "{{ auth_zone.id }}"
    target: "{{ view_dest.id }}"

- name: Create a DNS Bulk Copy Job  with additional fields.
  infoblox.universal_ddi.dns_view_bulk_copy:
    resources:
      - "{{ auth_zone.id }}"
    target: "{{ view_dest.id }}"
    recursive: true
    skip_on_error: true
    auth_zone_config:
      external_primaries:
        - type: "primary"
          fqdn: "test"
          address: "1.1.1.1"
"""

RETURN = r"""
id:
    description:
        - ID of the View object
    type: str
    returned: Always
item:
    description:
        - View object
    type: complex
    returned: Always
    contains:
        auth_zone_config:
            description:
                - "Optional. Authoritative zone related configuration."
            type: dict
            returned: Always
            contains:
                external_primaries:
                    description:
                        - "Optional. DNS primaries external to BloxOne DDI. Order is not significant."
                    type: list
                    returned: Always
                    elements: dict
                    contains:
                        address:
                            description:
                                - "Optional. Required only if I(type) is I(server). IP Address of nameserver."
                            type: str
                            returned: Always
                        fqdn:
                            description:
                                - "Optional. Required only if I(type) is I(server). FQDN of nameserver."
                            type: str
                            returned: Always
                        nsg:
                            description:
                                - "The resource identifier."
                            type: str
                            returned: Always
                        protocol_fqdn:
                            description:
                                - "FQDN of nameserver in punycode."
                            type: str
                            returned: Always
                        tsig_enabled:
                            description:
                                - "Optional. If enabled, secondaries will use the configured TSIG key when requesting a zone transfer from this primary."
                            type: bool
                            returned: Always
                        tsig_key:
                            description:
                                - "Optional. TSIG key."
                                - "Error if empty while I(tsig_enabled) is I(true)."
                            type: dict
                            returned: Always
                            contains:
                                algorithm:
                                    description:
                                        - "TSIG key algorithm."
                                        - "Possible values:"
                                        - "* I(hmac_sha256),"
                                        - "* I(hmac_sha1),"
                                        - "* I(hmac_sha224),"
                                        - "* I(hmac_sha384),"
                                        - "* I(hmac_sha512)."
                                    type: str
                                    returned: Always
                                comment:
                                    description:
                                        - "Comment for TSIG key."
                                    type: str
                                    returned: Always
                                key:
                                    description:
                                        - "The resource identifier."
                                    type: str
                                    returned: Always
                                name:
                                    description:
                                        - "TSIG key name, FQDN."
                                    type: str
                                    returned: Always
                                protocol_name:
                                    description:
                                        - "TSIG key name in punycode."
                                    type: str
                                    returned: Always
                                secret:
                                    description:
                                        - "TSIG key secret, base64 string."
                                    type: str
                                    returned: Always
                        type:
                            description:
                                - "Allowed values:"
                                - "* I(nsg),"
                                - "* I(primary)."
                            type: str
                            returned: Always
                external_secondaries:
                    description:
                        - "DNS secondaries external to BloxOne DDI. Order is not significant."
                    type: list
                    returned: Always
                    elements: dict
                    contains:
                        address:
                            description:
                                - "IP Address of nameserver."
                            type: str
                            returned: Always
                        fqdn:
                            description:
                                - "FQDN of nameserver."
                            type: str
                            returned: Always
                        protocol_fqdn:
                            description:
                                - "FQDN of nameserver in punycode."
                            type: str
                            returned: Always
                        stealth:
                            description:
                                - "If enabled, the NS record and glue record will NOT be automatically generated according to secondaries nameserver assignment."
                                - "Default: I(false)"
                            type: bool
                            returned: Always
                        tsig_enabled:
                            description:
                                - "If enabled, secondaries will use the configured TSIG key when requesting a zone transfer."
                                - "Default: I(false)"
                            type: bool
                            returned: Always
                        tsig_key:
                            description:
                                - "TSIG key."
                                - "Error if empty while I(tsig_enabled) is I(true)."
                            type: dict
                            returned: Always
                            contains:
                                algorithm:
                                    description:
                                        - "TSIG key algorithm."
                                        - "Possible values:"
                                        - "* I(hmac_sha256),"
                                        - "* I(hmac_sha1),"
                                        - "* I(hmac_sha224),"
                                        - "* I(hmac_sha384),"
                                        - "* I(hmac_sha512)."
                                    type: str
                                    returned: Always
                                comment:
                                    description:
                                        - "Comment for TSIG key."
                                    type: str
                                    returned: Always
                                key:
                                    description:
                                        - "The resource identifier."
                                    type: str
                                    returned: Always
                                name:
                                    description:
                                        - "TSIG key name, FQDN."
                                    type: str
                                    returned: Always
                                protocol_name:
                                    description:
                                        - "TSIG key name in punycode."
                                    type: str
                                    returned: Always
                                secret:
                                    description:
                                        - "TSIG key secret, base64 string."
                                    type: str
                                    returned: Always
                internal_secondaries:
                    description:
                        - "Optional. BloxOne DDI hosts acting as internal secondaries. Order is not significant."
                    type: list
                    returned: Always
                    elements: dict
                    contains:
                        host:
                            description:
                                - "The resource identifier."
                            type: str
                            returned: Always
                nsgs:
                    description:
                        - "The resource identifier."
                    type: list
                    returned: Always
        forward_zone_config:
            description:
                - "Optional. Forward zone related configuration."
            type: dict
            returned: Always
            contains:
                external_forwarders:
                    description:
                        - "Optional. External DNS servers to forward to. Order is not significant."
                    type: list
                    returned: Always
                    elements: dict
                    contains:
                        address:
                            description:
                                - "Server IP address."
                            type: str
                            returned: Always
                        fqdn:
                            description:
                                - "Server FQDN."
                            type: str
                            returned: Always
                        protocol_fqdn:
                            description:
                                - "Server FQDN in punycode."
                            type: str
                            returned: Always
                hosts:
                    description:
                        - "The resource identifier."
                    type: list
                    returned: Always
                internal_forwarders:
                    description:
                        - "The resource identifier."
                    type: list
                    returned: Always
                nsgs:
                    description:
                        - "The resource identifier."
                    type: list
                    returned: Always
        recursive:
            description:
                - "Indicates whether child objects should be copied or not."
                - "Defaults to I(false). Reserved for future use."
            type: bool
            returned: Always
        resources:
            description:
                - "The resource identifier."
            type: list
            returned: Always
        secondary_zone_config:
            description:
                - "Optional. Secondary zone related configuration."
            type: dict
            returned: Always
            contains:
                external_primaries:
                    description:
                        - "Optional. DNS primaries external to BloxOne DDI. Order is not significant."
                    type: list
                    returned: Always
                    elements: dict
                    contains:
                        address:
                            description:
                                - "Optional. Required only if I(type) is I(server). IP Address of nameserver."
                            type: str
                            returned: Always
                        fqdn:
                            description:
                                - "Optional. Required only if I(type) is I(server). FQDN of nameserver."
                            type: str
                            returned: Always
                        nsg:
                            description:
                                - "The resource identifier."
                            type: str
                            returned: Always
                        protocol_fqdn:
                            description:
                                - "FQDN of nameserver in punycode."
                            type: str
                            returned: Always
                        tsig_enabled:
                            description:
                                - "Optional. If enabled, secondaries will use the configured TSIG key when requesting a zone transfer from this primary."
                            type: bool
                            returned: Always
                        tsig_key:
                            description:
                                - "Optional. TSIG key."
                                - "Error if empty while I(tsig_enabled) is I(true)."
                            type: dict
                            returned: Always
                            contains:
                                algorithm:
                                    description:
                                        - "TSIG key algorithm."
                                        - "Possible values:"
                                        - "* I(hmac_sha256),"
                                        - "* I(hmac_sha1),"
                                        - "* I(hmac_sha224),"
                                        - "* I(hmac_sha384),"
                                        - "* I(hmac_sha512)."
                                    type: str
                                    returned: Always
                                comment:
                                    description:
                                        - "Comment for TSIG key."
                                    type: str
                                    returned: Always
                                key:
                                    description:
                                        - "The resource identifier."
                                    type: str
                                    returned: Always
                                name:
                                    description:
                                        - "TSIG key name, FQDN."
                                    type: str
                                    returned: Always
                                protocol_name:
                                    description:
                                        - "TSIG key name in punycode."
                                    type: str
                                    returned: Always
                                secret:
                                    description:
                                        - "TSIG key secret, base64 string."
                                    type: str
                                    returned: Always
                        type:
                            description:
                                - "Allowed values:"
                                - "* I(nsg),"
                                - "* I(primary)."
                            type: str
                            returned: Always
                external_secondaries:
                    description:
                        - "DNS secondaries external to BloxOne DDI. Order is not significant."
                    type: list
                    returned: Always
                    elements: dict
                    contains:
                        address:
                            description:
                                - "IP Address of nameserver."
                            type: str
                            returned: Always
                        fqdn:
                            description:
                                - "FQDN of nameserver."
                            type: str
                            returned: Always
                        protocol_fqdn:
                            description:
                                - "FQDN of nameserver in punycode."
                            type: str
                            returned: Always
                        stealth:
                            description:
                                - "If enabled, the NS record and glue record will NOT be automatically generated according to secondaries nameserver assignment."
                                - "Default: I(false)"
                            type: bool
                            returned: Always
                        tsig_enabled:
                            description:
                                - "If enabled, secondaries will use the configured TSIG key when requesting a zone transfer."
                                - "Default: I(false)"
                            type: bool
                            returned: Always
                        tsig_key:
                            description:
                                - "TSIG key."
                                - "Error if empty while I(tsig_enabled) is I(true)."
                            type: dict
                            returned: Always
                            contains:
                                algorithm:
                                    description:
                                        - "TSIG key algorithm."
                                        - "Possible values:"
                                        - "* I(hmac_sha256),"
                                        - "* I(hmac_sha1),"
                                        - "* I(hmac_sha224),"
                                        - "* I(hmac_sha384),"
                                        - "* I(hmac_sha512)."
                                    type: str
                                    returned: Always
                                comment:
                                    description:
                                        - "Comment for TSIG key."
                                    type: str
                                    returned: Always
                                key:
                                    description:
                                        - "The resource identifier."
                                    type: str
                                    returned: Always
                                name:
                                    description:
                                        - "TSIG key name, FQDN."
                                    type: str
                                    returned: Always
                                protocol_name:
                                    description:
                                        - "TSIG key name in punycode."
                                    type: str
                                    returned: Always
                                secret:
                                    description:
                                        - "TSIG key secret, base64 string."
                                    type: str
                                    returned: Always
                internal_secondaries:
                    description:
                        - "Optional. BloxOne DDI hosts acting as internal secondaries. Order is not significant."
                    type: list
                    returned: Always
                    elements: dict
                    contains:
                        host:
                            description:
                                - "The resource identifier."
                            type: str
                            returned: Always
                nsgs:
                    description:
                        - "The resource identifier."
                    type: list
                    returned: Always
        skip_on_error:
            description:
                - "Indicates whether copying should skip object in case of error and continue with next, or abort copying in case of error."
                - "Defaults to I(false)."
            type: bool
            returned: Always
        target:
            description:
                - "The resource identifier."
            type: str
            returned: Always
"""  # noqa: E501

from ansible_collections.infoblox.universal_ddi.plugins.module_utils.modules import UniversalDDIAnsibleModule

try:
    from dns_config import BulkCopyView, ViewApi
    from universal_ddi_client import ApiException
except ImportError:
    pass  # Handled by UniversalDDIAnsibleModule


class ViewModule(UniversalDDIAnsibleModule):
    def __init__(self, *args, **kwargs):
        super(ViewModule, self).__init__(*args, **kwargs)

        exclude = ["csp_url", "api_key", "portal_url", "portal_key", "id"]
        self._payload_params = {k: v for k, v in self.params.items() if v is not None and k not in exclude}
        self._payload = BulkCopyView.from_dict(self._payload_params)
        self._existing = None

    @property
    def payload_params(self):
        return self._payload_params

    @property
    def payload(self):
        return self._payload

    def create(self):
        if self.check_mode:
            return None

        resp = ViewApi(self.client).bulk_copy(body=self.payload)

        return resp.model_dump(by_alias=True, exclude_none=True)

    def run_command(self):
        result = dict(changed=False, object={}, id=None)

        try:
            item = {}
            if self.check_mode:
                self.exit_json(**result)
            else:
                item = self.create()
                result["changed"] = True
                result["msg"] = "Bulk Copy started"

            result["diff"] = dict(
                before={},
                after=item,
            )
            result["object"] = item
            result["id"] = item["id"] if (item and "id" in item) else None
        except ApiException as e:
            self.fail_json(msg=f"Failed to execute command: {e.status} {e.reason} {e.body}")

        self.exit_json(**result)


def main():
    module_args = dict(
        id=dict(type="str", required=False),
        auth_zone_config=dict(
            type="dict",
            options=dict(
                external_primaries=dict(
                    type="list",
                    elements="dict",
                    options=dict(
                        address=dict(type="str"),
                        fqdn=dict(type="str"),
                        nsg=dict(type="str"),
                        tsig_enabled=dict(type="bool"),
                        tsig_key=dict(
                            type="dict",
                            options=dict(
                                algorithm=dict(
                                    type="str",
                                    choices=["hmac_sha256", "hmac_sha1", "hmac_sha224", "hmac_sha384", "hmac_sha512"],
                                ),
                                comment=dict(type="str"),
                                key=dict(type="str", no_log=True),
                                name=dict(type="str"),
                                secret=dict(type="str", no_log=True),
                            ),
                            no_log=True,
                        ),
                        type=dict(type="str", choices=["nsg", "primary"]),
                    ),
                ),
                external_secondaries=dict(
                    type="list",
                    elements="dict",
                    options=dict(
                        address=dict(type="str"),
                        fqdn=dict(type="str"),
                        stealth=dict(type="bool"),
                        tsig_enabled=dict(type="bool"),
                        tsig_key=dict(
                            type="dict",
                            options=dict(
                                algorithm=dict(
                                    type="str",
                                    choices=["hmac_sha256", "hmac_sha1", "hmac_sha224", "hmac_sha384", "hmac_sha512"],
                                ),
                                comment=dict(type="str"),
                                key=dict(type="str", no_log=True),
                                name=dict(type="str"),
                                secret=dict(type="str", no_log=True),
                            ),
                            no_log=True,
                        ),
                    ),
                ),
                internal_secondaries=dict(
                    type="list",
                    elements="dict",
                    options=dict(
                        host=dict(type="str"),
                    ),
                ),
                nsgs=dict(type="list", elements="str"),
            ),
        ),
        forward_zone_config=dict(
            type="dict",
            options=dict(
                external_forwarders=dict(
                    type="list",
                    elements="dict",
                    options=dict(
                        address=dict(type="str"),
                        fqdn=dict(type="str"),
                    ),
                ),
                hosts=dict(type="list", elements="str"),
                internal_forwarders=dict(type="list", elements="str"),
                nsgs=dict(type="list", elements="str"),
            ),
        ),
        recursive=dict(type="bool", default=False),
        resources=dict(type="list", elements="str", required=True),
        secondary_zone_config=dict(
            type="dict",
            options=dict(
                external_primaries=dict(
                    type="list",
                    elements="dict",
                    options=dict(
                        address=dict(type="str"),
                        fqdn=dict(type="str"),
                        nsg=dict(type="str"),
                        tsig_enabled=dict(type="bool"),
                        tsig_key=dict(
                            type="dict",
                            options=dict(
                                algorithm=dict(
                                    type="str",
                                    choices=["hmac_sha256", "hmac_sha1", "hmac_sha224", "hmac_sha384", "hmac_sha512"],
                                ),
                                comment=dict(type="str"),
                                key=dict(type="str", no_log=True),
                                name=dict(type="str"),
                                secret=dict(type="str", no_log=True),
                            ),
                            no_log=True,
                        ),
                        type=dict(type="str", choices=["nsg", "primary"]),
                    ),
                ),
                external_secondaries=dict(
                    type="list",
                    elements="dict",
                    options=dict(
                        address=dict(type="str"),
                        fqdn=dict(type="str"),
                        stealth=dict(type="bool"),
                        tsig_enabled=dict(type="bool"),
                        tsig_key=dict(
                            type="dict",
                            options=dict(
                                algorithm=dict(
                                    type="str",
                                    choices=["hmac_sha256", "hmac_sha1", "hmac_sha224", "hmac_sha384", "hmac_sha512"],
                                ),
                                comment=dict(type="str"),
                                key=dict(type="str", no_log=True),
                                name=dict(type="str"),
                                secret=dict(type="str", no_log=True),
                            ),
                            no_log=True,
                        ),
                    ),
                ),
                internal_secondaries=dict(
                    type="list",
                    elements="dict",
                    options=dict(
                        host=dict(type="str"),
                    ),
                ),
                nsgs=dict(type="list", elements="str"),
            ),
        ),
        skip_on_error=dict(type="bool"),
        target=dict(type="str", required=True),
    )

    module = ViewModule(
        argument_spec=module_args,
        supports_check_mode=True,
    )

    module.run_command()


if __name__ == "__main__":
    main()
