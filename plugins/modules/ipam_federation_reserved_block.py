#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: Infoblox Inc.
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: ipam_federation_reserved_block
short_description: Manages a Reserved Block
description:
    - Manages a Reserved Block.
    - The Reserved Block object is a set of contiguous IP addresses with no gap, expressed as a CIDR block. It is explicitly associated with a Federated Realm. A Reserved Block indicates an address range for which authority is expressly forbidden. Cooperating IPAM services must not make allocations in this range.
version_added: 1.3.0
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
            - "Exactly one of I(address) or I(next_available_id) is required. This field is immutable after creation."
        type: str
    cidr:
        description:
            - "The CIDR of the reserved block. This is required, if I(address) does not specify it in its input, and whenever I(next_available_id) is used."
        type: int
    comment:
        description:
            - "The description for the reserved block. May contain 0 to 1024 characters. Can include UTF-8."
        type: str
    federated_pool_id:
        description:
            - "The resource identifier."
        type: str
    federated_realm:
        description:
            - "The resource identifier."
        type: str
        required: true
    name:
        description:
            - "The name of the reserved block. May contain 1 to 256 characters. Can include UTF-8."
        type: str
    next_available_id:
        description:
            - "The resource identifier of the parent Federated Block under which the next available reserved block should be allocated."
            - "Exactly one of I(address) or I(next_available_id) is required."
        type: str
    tags:
        description:
            - "The tags for the reserved block in JSON format."
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

    - name: Create a Federated Block (required as parent)
      infoblox.universal_ddi.ipam_federation_federated_block:
        address: "45.85.0.0/16"
        federated_realm: "{{ federated_realm.id }}"
        state: present
      register: federated_block

    - name: Create a Reserved Block
      infoblox.universal_ddi.ipam_federation_reserved_block:
        address: "45.85.1.0/24"
        federated_realm: "{{ federated_realm.id }}"
        state: present

    - name: Create a Reserved Block with Additional Fields
      infoblox.universal_ddi.ipam_federation_reserved_block:
        address: "45.85.2.0/24"
        federated_realm: "{{ federated_realm.id }}"
        name: "example_reserved_block"
        comment: "This is an example reserved block"
        tags:
            location: "site-1"
        state: present

    - name: Create the Next Available Reserved Block under a Federated Block
      infoblox.universal_ddi.ipam_federation_reserved_block:
        next_available_id: "{{ federated_block.id }}"
        cidr: 24
        federated_realm: "{{ federated_realm.id }}"
        state: present

    - name: Delete the Reserved Block
      infoblox.universal_ddi.ipam_federation_reserved_block:
        address: "45.85.1.0/24"
        federated_realm: "{{ federated_realm.id }}"
        state: absent
"""  # noqa: E501

RETURN = r"""
id:
    description:
        - ID of the Reserved Block object
    type: str
    returned: Always
item:
    description:
        - Reserved Block object
    type: complex
    returned: Always
    contains:
        address:
            description:
                - "The address field in form \"a.b.c.d/n\" where the \"/n\" may be omitted. In this case, the CIDR value must be defined in the I(cidr) field. When reading, the I(address) field is always in the form \"a.b.c.d\"."
            type: str
            returned: Always
        cidr:
            description:
                - "The CIDR of the reserved block. This is required, if I(address) does not specify it in its input."
            type: int
            returned: Always
        comment:
            description:
                - "The description for the reserved block. May contain 0 to 1024 characters. Can include UTF-8."
            type: str
            returned: Always
        created_at:
            description:
                - "Time when the object has been created."
            type: str
            returned: Always
        federated_pool_id:
            description:
                - "The resource identifier."
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
        metadata:
            description:
                - "The metadata for the reserved block in JSON format."
            type: dict
            returned: Always
        name:
            description:
                - "The name of the reserved block. May contain 1 to 256 characters. Can include UTF-8."
            type: str
            returned: Always
        network_compliant:
            description:
                - "The compliance status of the reserved block, as determined by the federation service."
            type: bool
            returned: Always
        parent:
            description:
                - "The resource identifier."
            type: str
            returned: Always
        protocol:
            description:
                - "The type of protocol of reserved block (I(ip4) or I(ip6))."
            type: str
            returned: Always
        region:
            description:
                - "The region where the reserved block is located."
            type: str
            returned: Always
        tags:
            description:
                - "The tags for the reserved block in JSON format."
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
    from ipam_federation import (
        NextAvailableBlockRequest,
        NextAvailableReservedBlockApi,
        ReservedBlock,
        ReservedBlockApi,
    )
    from universal_ddi_client import ApiException, NotFoundException
except ImportError:
    pass  # Handled by UniversalDDIAnsibleModule


class ReservedBlockModule(UniversalDDIAnsibleModule):
    def __init__(self, *args, **kwargs):
        super(ReservedBlockModule, self).__init__(*args, **kwargs)
        self.next_available_id = self.params.get("next_available_id")

        if self.params["address"] is not None and "/" in self.params["address"]:
            self.params["address"], netmask = self.params["address"].split("/")
            self.params["cidr"] = int(netmask)

        exclude = ["state", "csp_url", "api_key", "portal_url", "portal_key", "id", "next_available_id"]
        self._payload_params = {k: v for k, v in self.params.items() if v is not None and k not in exclude}

        # ReservedBlock.address is a required, non-Optional field in the SDK. When next_available_id
        # is used instead of address, or when updating an object by id without re-supplying address,
        # self._payload_params has no "address" key -- substitute a placeholder so construction
        # doesn't fail; create()/update() never send this placeholder as-is (see below).
        payload_dict = dict(self._payload_params)
        payload_dict.setdefault("address", "")
        self._payload = ReservedBlock.from_dict(payload_dict)

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
                resp = ReservedBlockApi(self.client).read(self.params["id"])
                return resp.result
            except NotFoundException as e:
                if self.params["state"] == "absent":
                    return None
                raise e
        else:
            address = self.params.get("address")
            cidr = self.params.get("cidr")

            # If address is None, next_available_id is being used to create a new reserved block,
            # or an existing one is being managed by id -- nothing to look up by address/cidr yet.
            if address is None:
                return None

            # [NORTHSTAR-12774] federated_realm cannot be added as a filter clause, so filter on
            # address/cidr alone. address+cidr is otherwise the identifying key: matching on it
            # alone (not also federated_realm) is what lets a reassignment to a different realm
            # be recognized as an update of the existing object rather than a new create.
            filter = f"address=='{address}/{cidr}'"
            resp = ReservedBlockApi(self.client).list(filter=filter)

            if not resp.results:
                resp.results = []

            if len(resp.results) == 1:
                return resp.results[0]
            if len(resp.results) > 1:
                self.fail_json(msg=f"Found multiple ReservedBlock: {resp.results}")
            return None

    def create(self):
        if self.check_mode:
            return None

        if self.next_available_id is not None:
            body = NextAvailableBlockRequest.from_dict(
                {k: v for k, v in self._payload_params.items() if k in ("cidr", "comment", "name", "tags")}
            )
            resp = NextAvailableReservedBlockApi(self.client).create_next_available_reserved_blocks(
                id=self.next_available_id, body=body
            )
            if not resp.results:
                self.fail_json(msg="Unable to create next available ReservedBlock, no results were returned")
            result = resp.results[0]

            # The create-next-available endpoint does not persist federated_pool_id, so patch it
            # in with a follow-up update when the user configured it.
            federated_pool_id = self._payload_params.get("federated_pool_id")
            if federated_pool_id is not None:
                update_body = ReservedBlock.from_dict({"address": "", "federated_pool_id": federated_pool_id})
                object.__setattr__(update_body, "address", None)
                try:
                    resp = ReservedBlockApi(self.client).update(id=result.id, body=update_body)
                    result = resp.result
                except ApiException as e:
                    # Nothing persisted federated_pool_id: roll back the created block rather than
                    # leaving behind a reserved block the user never asked to keep untagged.
                    ReservedBlockApi(self.client).delete(result.id)
                    self.fail_json(
                        msg=f"Unable to set federated_pool_id on next available ReservedBlock, rolled back "
                        f"creation: {e.status} {e.reason} {e.body}"
                    )

            return result.model_dump(by_alias=True, exclude_none=True)

        resp = ReservedBlockApi(self.client).create(body=self.payload)
        return resp.result.model_dump(by_alias=True, exclude_none=True)

    def update(self):
        if self.check_mode:
            return None

        update_body = self.payload
        configured_address = self.payload_params.get("address")
        if configured_address is not None and configured_address != getattr(self.existing, "address"):
            self.fail_json(msg="address cannot be updated")

        # NOTE: like FederatedBlock, we cannot route this through validate_readonly_on_update()'s
        # setattr(update_body, field, None) trick here: ReservedBlock.address is a required,
        # non-Optional StrictStr field in the SDK (with validate_assignment=True), so a normal
        # attribute assignment of None raises a pydantic ValidationError. The API itself rejects
        # a PATCH containing `address`, even unchanged, so it must be excluded from the request
        # body entirely. Bypass pydantic's assignment validation to null it out; ReservedBlock's
        # serialization does model_dump(exclude_none=True), so a None value here is correctly
        # dropped from the outgoing payload.
        object.__setattr__(update_body, "address", None)

        resp = ReservedBlockApi(self.client).update(id=self.existing.id, body=update_body)
        return resp.result.model_dump(by_alias=True, exclude_none=True)

    def delete(self):
        if self.check_mode:
            return

        ReservedBlockApi(self.client).delete(self.existing.id)

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
                result["msg"] = "Reserved Block created"
            elif self.params["state"] == "present" and self.existing is not None:
                if self.payload_changed():
                    item = self.update()
                    result["changed"] = True
                    result["msg"] = "Reserved Block updated"
            elif self.params["state"] == "absent" and self.existing is not None:
                self.delete()
                result["changed"] = True
                result["msg"] = "Reserved Block deleted"

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
        address=dict(type="str"),
        cidr=dict(type="int"),
        comment=dict(type="str"),
        federated_pool_id=dict(type="str"),
        federated_realm=dict(type="str", required=True),
        name=dict(type="str"),
        next_available_id=dict(type="str"),
        tags=dict(type="dict"),
    )

    module = ReservedBlockModule(
        argument_spec=module_args,
        supports_check_mode=True,
        mutually_exclusive=[["address", "next_available_id"]],
        required_one_of=[["address", "next_available_id"]],
        required_by={"next_available_id": "cidr"},
    )

    module.run_command()


if __name__ == "__main__":
    main()
