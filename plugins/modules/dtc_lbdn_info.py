#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: Infoblox Inc.
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: dtc_lbdn_info
short_description: Retrieves existing DTC LBDNs
description:
    - Retrieves information about existing DTC LBDNs
version_added: 1.2.0
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

EXAMPLES = r"""
    - name: Get Information about the DTC LBDN by ID
      infoblox.universal_ddi.dtc_lbdn_info:
        id: "{{ dtc_lbdn.id }}"

    - name: Get Information about the DTC LBDN by filters (Name)
      infoblox.universal_ddi.dtc_lbdn_info:
        filters:
          name: "example_dtc_lbdn"

    - name: Get Information about the DTC LBDN by filter query
      infoblox.universal_ddi.dtc_lbdn_info:
        filter_query: "name=='example_dtc_lbdn'"

    - name: Get Information about the DTC LBDN by tag filters
      infoblox.universal_ddi.dtc_lbdn_info:
        tag_filters:
          location: "site-1"
"""

RETURN = r"""
id:
    description:
        - ID of the Lbdn object
    type: str
    returned: Always
objects:
    description:
        - Lbdn object
    type: list
    elements: dict
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
    from dns_config import LbdnApi
    from universal_ddi_client import ApiException, NotFoundException
except ImportError:
    pass  # Handled by UniversalDDIAnsibleModule


class LbdnInfoModule(UniversalDDIAnsibleModule):
    def __init__(self, *args, **kwargs):
        super(LbdnInfoModule, self).__init__(*args, **kwargs)
        self._existing = None
        self._limit = 1000

    def find_by_id(self):
        try:
            resp = LbdnApi(self.client).read(self.params["id"], inherit="full")
            return [resp.result]
        except NotFoundException as e:
            return []

    def find(self):
        if self.params["id"] is not None:
            return self.find_by_id()

        filter_str = None

        if self.params["filters"] is not None:
            filters = dict(self.params["filters"])

            view = filters.get("view")
            if view and "/" in view:
                filters["view"] = view.split("/")[-1]

            filter_str = " and ".join([f"{k}=='{v}'" for k, v in filters.items()])

        elif self.params["filter_query"] is not None:
            filter_str = self.params["filter_query"]

            if "view==" in filter_str and "dns/view/" in filter_str:
                import re

                filter_str = re.sub(r"dns/view/([a-f0-9\-]+)", r"\1", filter_str)

        tag_filter_str = None
        if self.params["tag_filters"] is not None:
            tag_filter_str = " and ".join([f"{k}=='{v}'" for k, v in self.params["tag_filters"].items()])
        elif self.params["tag_filter_query"] is not None:
            tag_filter_str = self.params["tag_filter_query"]

        all_results = []
        offset = 0

        while True:
            try:
                resp = LbdnApi(self.client).list(
                    offset=offset, limit=self._limit, filter=filter_str, tfilter=tag_filter_str, inherit="full"
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

    module = LbdnInfoModule(
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
