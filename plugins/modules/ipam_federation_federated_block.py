#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: Infoblox Inc.
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: ipam_federation_federated_block
short_description: Manages a Federated Block
description:
    - Manages a Federated Block.
    - The Federated Block object allows a uniform representation of the address space segmentation, supporting functions such as administrative grouping, routing aggregation, delegation etc.
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
            - "The address field in form \"a.b.c.d/n\" where the \"/n\" may be omitted. In this case, the CIDR value must be defined in the I(cidr) field. When reading, the I(address) field is always in the form \"a.b.c.d\"."
        type: str
        required: true
    cidr:
        description:
            - "The CIDR of the federated block. This is required, if I(address) does not specify it in its input."
        type: int
    comment:
        description:
            - "The description for the federated block. May contain 0 to 1024 characters. Can include UTF-8."
        type: str
    federated_realm:
        description:
            - "The resource identifier."
        type: str
        required: true
    name:
        description:
            - "The name of the federated block. May contain 1 to 256 characters. Can include UTF-8."
        type: str
    parent:
        description:
            - "The resource identifier."
        type: str
    tags:
        description:
            - "The tags for the federated block in JSON format."
        type: dict

extends_documentation_fragment:
    - infoblox.universal_ddi.common
"""  # noqa: E501

EXAMPLES = r"""
    - name: Create a Federated Realm (required as parent)
      infoblox.universal_ddi.ipam_federation_federated_realm:
        name: "example_federated_realm"
        state: present
      register: federated_realm

    - name: Create a Federated Block
      infoblox.universal_ddi.ipam_federation_federated_block:
        address: "45.85.0.0/16"
        federated_realm: "{{ federated_realm.id }}"
        state: present

    - name: Create a Federated Block with Additional Fields
      infoblox.universal_ddi.ipam_federation_federated_block:
        address: "45.85.0.0/16"
        federated_realm: "{{ federated_realm.id }}"
        name: "example_federated_block"
        comment: "This is an example federated block"
        tags:
            location: "site-1"
        state: present

    - name: Delete the Federated Block
      infoblox.universal_ddi.ipam_federation_federated_block:
        address: "45.85.0.0/16"
        federated_realm: "{{ federated_realm.id }}"
        state: absent
"""  # noqa: E501

RETURN = r"""
id:
    description:
        - ID of the Federated Block object
    type: str
    returned: Always
item:
    description:
        - Federated Block object
    type: complex
    returned: Always
    contains:
        address:
            description:
                - "The address field in form \"a.b.c.d/n\" where the \"/n\" may be omitted. In this case, the CIDR value must be defined in the I(cidr) field. When reading, the I(address) field is always in the form \"a.b.c.d\"."
            type: str
            returned: Always
        allocation_v4:
            description:
                - "The percentage of the Federated Block's total address space that is consumed by Leaf Terminals."
            type: dict
            returned: Always
            contains:
                allocated:
                    description:
                        - "Percent of total space allocated."
                    type: int
                    returned: Always
                delegated:
                    description:
                        - "Percent of total space delegated."
                    type: int
                    returned: Always
                overlapping:
                    description:
                        - "Percent of total space in overlapping blocks."
                    type: int
                    returned: Always
                reserved:
                    description:
                        - "Percent of total space reserved."
                    type: int
                    returned: Always
        cidr:
            description:
                - "The CIDR of the federated block. This is required, if I(address) does not specify it in its input."
            type: int
            returned: Always
        comment:
            description:
                - "The description for the federated block. May contain 0 to 1024 characters. Can include UTF-8."
            type: str
            returned: Always
        created_at:
            description:
                - "Time when the object has been created."
            type: str
            returned: Always
        federated_realm:
            description:
                - "The resource identifier."
            type: str
            returned: Always
        id:
            description:
                - "The resource identifier."
            type: str
            returned: Always
        name:
            description:
                - "The name of the federated block. May contain 1 to 256 characters. Can include UTF-8."
            type: str
            returned: Always
        parent:
            description:
                - "The resource identifier."
            type: str
            returned: Always
        protocol:
            description:
                - "The type of protocol of federated block (I(ip4) or I(ip6))."
            type: str
            returned: Always
        tags:
            description:
                - "The tags for the federated block in JSON format."
            type: dict
            returned: Always
        updated_at:
            description:
                - "Time when the object has been updated. Equals to I(created_at) if not updated after creation."
            type: str
            returned: Always
"""  # noqa: E501

from ansible_collections.infoblox.universal_ddi.plugins.module_utils.modules import UniversalDDIAnsibleModule

try:
    from ipam_federation import FederatedBlock, FederatedBlockApi
    from universal_ddi_client import ApiException, NotFoundException
except ImportError:
    pass  # Handled by UniversalDDIAnsibleModule


class FederatedBlockModule(UniversalDDIAnsibleModule):
    def __init__(self, *args, **kwargs):
        super(FederatedBlockModule, self).__init__(*args, **kwargs)

        if "/" in self.params["address"]:
            self.params["address"], netmask = self.params["address"].split("/")
            self.params["cidr"] = int(netmask)

        exclude = ["state", "csp_url", "api_key", "portal_url", "portal_key", "id"]
        self._payload_params = {k: v for k, v in self.params.items() if v is not None and k not in exclude}
        self._payload = FederatedBlock.from_dict(self._payload_params)
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
                resp = FederatedBlockApi(self.client).read(self.params["id"])
                return resp.result
            except NotFoundException as e:
                if self.params["state"] == "absent":
                    return None
                raise e
        else:
            address = self.params.get("address")
            cidr = self.params.get("cidr")

            # [NORTHSTAR-12774] Due to this bug federated realm cannot be added as a filter
            # filter = f"address=='{self.params['address']}' and federated_realm=='{self.params['federated_realm']}'"

            filter = f"address=='{address}/{cidr}'"
            resp = FederatedBlockApi(self.client).list(filter=filter)

            for index, val in enumerate(resp.results):
                if getattr(val, "federated_realm") != self.params["federated_realm"]:
                    return resp.results.pop(index)

            if not resp.results:
                resp.results = []

            if len(resp.results) == 1:
                return resp.results[0]
            if len(resp.results) > 1:
                self.fail_json(msg=f"Found multiple Federated Blocks: {resp.results}")
            if len(resp.results) == 0:
                return None

    def create(self):
        if self.check_mode:
            return None

        resp = FederatedBlockApi(self.client).create(body=self.payload)
        return resp.result.model_dump(by_alias=True, exclude_none=True)

    def update(self):
        if self.check_mode:
            return None

        update_body = self.payload
        update_body = self.validate_readonly_on_update(self.existing, update_body, ["address"])

        resp = FederatedBlockApi(self.client).update(id=self.existing.id, body=update_body)
        return resp.result.model_dump(by_alias=True, exclude_none=True)

    def delete(self):
        if self.check_mode:
            return

        FederatedBlockApi(self.client).delete(self.existing.id)

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
                result["msg"] = "Federated Block created"
            elif self.params["state"] == "present" and self.existing is not None:
                if self.payload_changed():
                    item = self.update()
                    result["changed"] = True
                    result["msg"] = "Federated Block updated"
            elif self.params["state"] == "absent" and self.existing is not None:
                self.delete()
                result["changed"] = True
                result["msg"] = "Federated Block deleted"

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
        address=dict(type="str", required=True),
        cidr=dict(type="int"),
        comment=dict(type="str"),
        federated_realm=dict(type="str", required=True),
        name=dict(type="str"),
        parent=dict(type="str"),
        tags=dict(type="dict"),
    )

    module = FederatedBlockModule(
        argument_spec=module_args,
        supports_check_mode=True,
        required_if=[("state", "present", ["address", "federated_realm"])],
    )

    module.run_command()


if __name__ == "__main__":
    main()
