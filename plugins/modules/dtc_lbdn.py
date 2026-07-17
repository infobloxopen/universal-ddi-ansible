#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: Infoblox Inc.
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: dtc_lbdn
short_description: Manages a DTC LBDN
description:
    - Manages a DTC LBDN
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
    comment:
        description:
            - "Optional. Comment for B(LBDN)."
        type: str
    disabled:
        description:
            - "Optional. I(true) to disable object. A disabled object is effectively non-existent when generating configuration."
        type: bool
        default: false
    dtc_policy:
        description:
            - "Optional. B(DTC Policy) information."
        type: dict
        suboptions:
            policy_id:
                description:
                    - "The resource identifier."
                type: str
    inheritance_sources:
        description:
            - "Optional. The inheritance configuration."
        type: dict
        suboptions:
            ttl:
                description: "The inheritance configuration specifies how the object inherits the ttl field."
                type: dict
                suboptions:
                    action:
                        description:
                            - "The inheritance setting for a field."
                            - "Valid values are:"
                            - "* I(inherit): Use the inherited value."
                            - "* I(override): Use the value set in the object."
                            - "Defaults to I(inherit)."
                        type: str
    name:
        description:
            - "Name of B(LBDN)."
        type: str
        required: true
    precedence:
        description:
            - "Optional. Precedence."
        type: int
    tags:
        description:
            - "Optional. The tags for B(LBDN) in JSON format."
        type: dict
    ttl:
        description:
            - "Optional. Time to live value (in seconds) to be used for records in DTC response. Unsigned integer, min:0, max 2147483647(31-bits per RFC-2181)."
        type: int
    view:
        description:
            - "The resource identifier."
        type: str
        required: true

extends_documentation_fragment:
    - infoblox.universal_ddi.common
"""  # noqa: E501

EXAMPLES = r"""
    - name: Create a DNS View (required as parent)
      infoblox.universal_ddi.dns_view:
        name: "example_dns_view"
        state: "present"
      register: view

    - name: Create a DTC LBDN
      infoblox.universal_ddi.dtc_lbdn:
        name: "example_dtc_lbdn"
        view: "{{ view.id }}"
        state: "present"
      register: dtc_lbdn

    - name: Create a DTC LBDN with Additional Parameters
      infoblox.universal_ddi.dtc_lbdn:
        name: "example_dtc_lbdn"
        view: "{{ view.id }}"
        comment: "This is a DTC LBDN"
        disabled: false
        ttl: 300
        precedence: 10
        state: "present"
        tags:
          location: "site-1"

    - name: Delete the DTC LBDN
      infoblox.universal_ddi.dtc_lbdn:
        name: "example_dtc_lbdn"
        view: "{{ view.id }}"
        state: "absent"
"""

RETURN = r"""
id:
    description:
        - ID of the Lbdn object
    type: str
    returned: Always
item:
    description:
        - Lbdn object
    type: complex
    returned: Always
    contains:
        comment:
            description:
                - "Optional. Comment for B(LBDN)."
            type: str
            returned: Always
        disabled:
            description:
                - "Optional. I(true) to disable object. A disabled object is effectively non-existent when generating configuration."
            type: bool
            returned: Always
        dtc_policy:
            description:
                - "Optional. B(DTC Policy) information."
            type: dict
            returned: Always
            contains:
                name:
                    description:
                        - "B(DTC Policy) display name."
                    type: str
                    returned: Always
                policy_id:
                    description:
                        - "The resource identifier."
                    type: str
                    returned: Always
        id:
            description:
                - "The resource identifier."
            type: str
            returned: Always
        inheritance_sources:
            description:
                - "Optional. The inheritance configuration."
            type: dict
            returned: Always
            contains:
                ttl:
                    description: "The inheritance configuration specifies how the object inherits the ttl field."
                    type: dict
                    returned: Always
                    contains:
                        action:
                            description:
                                - "The inheritance setting for a field."
                                - "Valid values are:"
                                - "* I(inherit): Use the inherited value."
                                - "* I(override): Use the value set in the object."
                                - "Defaults to I(inherit)."
                            type: str
                            returned: Always
                        display_name:
                            description:
                                - "The human-readable display name for the object referred to by I(source)."
                            type: str
                            returned: Always
                        source:
                            description:
                                - "The resource identifier."
                            type: str
                            returned: Always
                        value:
                            description:
                                - "The inherited value."
                            type: int
                            returned: Always
        name:
            description:
                - "Name of B(LBDN)."
            type: str
            returned: Always
        precedence:
            description:
                - "Optional. Precedence."
            type: int
            returned: Always
        tags:
            description:
                - "Optional. The tags for B(LBDN) in JSON format."
            type: dict
            returned: Always
        ttl:
            description:
                - "Optional. Time to live value (in seconds) to be used for records in DTC response. Unsigned integer, min: 0, max 2147483647 (31-bits per RFC-2181)."
            type: int
            returned: Always
        view:
            description:
                - "The resource identifier."
            type: str
            returned: Always
"""  # noqa: E501

from ansible_collections.infoblox.universal_ddi.plugins.module_utils.modules import UniversalDDIAnsibleModule

try:
    from dns_config import LBDN, LbdnApi
    from universal_ddi_client import ApiException, NotFoundException
except ImportError:
    pass  # Handled by UniversalDDIAnsibleModule


class LbdnModule(UniversalDDIAnsibleModule):
    def __init__(self, *args, **kwargs):
        super(LbdnModule, self).__init__(*args, **kwargs)

        exclude = ["state", "csp_url", "api_key", "portal_url", "portal_key", "id"]
        self._payload_params = {k: v for k, v in self.params.items() if v is not None and k not in exclude}
        self._payload = LBDN.from_dict(self._payload_params)
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
                resp = LbdnApi(self.client).read(self.params["id"], inherit="full")
                return resp.result
            except NotFoundException as e:
                if self.params["state"] == "absent":
                    return None
                raise e
        else:
            view = self.params.get("view")
            if view and "/" in view:
                view = view.split("/")[-1]

            filter_str = f"name=='{self.params['name']}' and view=='{view}'"

            resp = LbdnApi(self.client).list(filter=filter_str, inherit="full")

            # If no results, set results to empty list
            if not resp.results:
                resp.results = []

            if len(resp.results) == 1:
                return resp.results[0]
            if len(resp.results) > 1:
                self.fail_json(msg=f"Found multiple Lbdn: {resp.results}")
            if len(resp.results) == 0:
                return None

    def create(self):
        if self.check_mode:
            return None

        resp = LbdnApi(self.client).create(body=self.payload, inherit="full")
        return resp.result.model_dump(by_alias=True, exclude_none=True)

    def update(self):
        if self.check_mode:
            return None

        resp = LbdnApi(self.client).update(id=self.existing.id, body=self.payload, inherit="full")
        return resp.result.model_dump(by_alias=True, exclude_none=True)

    def delete(self):
        if self.check_mode:
            return

        LbdnApi(self.client).delete(self.existing.id)

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
                result["msg"] = "Lbdn created"
            elif self.params["state"] == "present" and self.existing is not None:
                if self.payload_changed():
                    item = self.update()
                    result["changed"] = True
                    result["msg"] = "Lbdn updated"
            elif self.params["state"] == "absent" and self.existing is not None:
                self.delete()
                result["changed"] = True
                result["msg"] = "Lbdn deleted"

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
        disabled=dict(type="bool", default=False),
        dtc_policy=dict(
            type="dict",
            options=dict(
                policy_id=dict(type="str"),
            ),
        ),
        inheritance_sources=dict(
            type="dict",
            options=dict(
                ttl=dict(
                    type="dict",
                    options=dict(
                        action=dict(type="str"),
                    ),
                ),
            ),
        ),
        name=dict(type="str", required=True),
        precedence=dict(type="int"),
        tags=dict(type="dict"),
        ttl=dict(type="int"),
        view=dict(type="str", required=True),
    )

    module = LbdnModule(
        argument_spec=module_args,
        supports_check_mode=True,
        required_if=[("state", "present", ["name", "view"])],
    )

    module.run_command()


if __name__ == "__main__":
    main()
