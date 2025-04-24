#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: Infoblox Inc.
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: cloud_discovery_providers_info
short_description: Retrieves Cloud Discovery Providers.
description:
    - Retrieves information about existing Cloud Discovery Providers.
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

extends_documentation_fragment:
    - infoblox.universal_ddi.common
"""  # noqa: E501

EXAMPLES = r"""
# Note: The following examples demonstrate how to retrieve information for AWS cloud discovery providers.
# Similar examples can be used for other providers like GCP and Azure by changing the provider-specific details.

- name: Get AWS cloud discovery provider by ID
  infoblox.universal_ddi.cloud_discovery_providers_info:
    id: "{{ aws_provider.id }}"

- name: Get AWS cloud discovery provider by filter
  infoblox.universal_ddi.cloud_discovery_providers_info:
    filters:
      name: "aws_provider_name"

- name: Get AWS cloud discovery provider by filter query
  infoblox.universal_ddi.cloud_discovery_providers_info:
    filter_query: "provider_type=='Amazon Web Services' and name=='aws_provider_name'"

"""

RETURN = r"""
id:
    description:
        - ID of the Providers object.
    type: str
    returned: Always
objects:
    description:
        - Providers object.
    type: list
    elements: dict
    returned: Always
    contains:
        account_preference:
            description:
                - "Account preference. For example: single, multiple, auto-discover-multiple."
            type: str
            returned: Always
        additional_config:
            description:
                - "Additional configuration. Example: '{ \"excluded_object_types\": [], \"exclusion_account_list\": [], \"zone_forwarding\": \"true\" or \"false\" }'."
            type: dict
            returned: Always
            contains:
                excluded_accounts:
                    description: "List of accounts to be excluded from the discovery process."
                    type: list
                    returned: Always
                forward_zone_enabled:
                    description: "Flag to enable or disable forwarding of zones."
                    type: bool
                    returned: Always
                internal_ranges_enabled:
                    description: "Flag to enable or disable internal range discovery."
                    type: bool
                    returned: Always
                object_type:
                    description: "Configuration for object types to be discovered."
                    type: dict
                    returned: Always
                    contains:
                        discover_new:
                            description: "Flag to enable or disable discovery of new objects."
                            type: bool
                            returned: Always
                        objects:
                            description: "List of objects to be discovered."
                            type: list
                            returned: Always
                            elements: dict
                            contains:
                                category:
                                    description: "Category of the object."
                                    type: dict
                                    returned: Always
                                    contains:
                                        excluded:
                                            description: "Flag to exclude the category."
                                            type: bool
                                            returned: Always
                                        id:
                                            description: "ID of the category."
                                            type: str
                                            returned: Always
                                resource_set:
                                    description: "Set of resources."
                                    type: list
                                    returned: Always
                                    elements: dict
                                    contains:
                                        excluded:
                                            description: "Flag to exclude the resource set."
                                            type: bool
                                            returned: Always
                                        id:
                                            description: "ID of the resource set."
                                            type: str
                                            returned: Always
                        version:
                            description: "Version of the object type configuration."
                            type: float
                            returned: Always
        created_at:
            description:
                - "Timestamp when the object has been created."
            type: str
            returned: Always
        credential_preference:
            description:
                - "Credential preference. Example: '{ \"type\": \"static\" or \"delegated\", \"access_identifier_type\": \"role_arn\" or \"tenant_id\" or \"project_id\" }'."
            type: dict
            returned: Always
            contains:
                access_identifier_type:
                    description: "Type of access identifier, e.g., 'role_arn', 'tenant_id', or 'project_id'."
                    type: str
                    returned: Always
                credential_type:
                    description: "Type of credential, e.g., 'static' or 'delegated'."
                    type: str
                    returned: Always
        deleted_at:
            description:
                - "Timestamp when the object has been deleted."
            type: str
            returned: Always
        description:
            description:
                - "Description of the discovery config. Optional."
            type: str
            returned: Always
        desired_state:
            description:
                - "Desired state. Default is 'enabled'."
            type: str
            returned: Always
        destination_types_enabled:
            description:
                - "Destinations types enabled: Example: DNS, IPAM, and ACCOUNT."
            type: list
            returned: Always
        destinations:
            description:
                - "Destinations."
            type: list
            returned: Always
            elements: dict
            contains:
                config:
                    description:
                        - "Destination configuration. Example: '{ \"dns\": { \"view_name\": \"view 1\", \"view_id\": \"dns/view/v1\", \"consolidated_zone_data_enabled\": false, \"sync_type\": \"read_only/read_write\", \"split_view_enabled\": false }, \"ipam\": { \"ip_space\": \"\" }, \"account\": {} }'."
                    type: dict
                    returned: Always
                    contains:
                        dns:
                            description: "DNS configuration details."
                            type: dict
                            returned: Always
                            contains:
                                consolidated_zone_data_enabled:
                                    description: "Flag to enable or disable consolidated zone data."
                                    type: bool
                                    returned: Always
                                split_view_enabled:
                                    description:
                                        - "Flag to enable or disable split view, consolidating private zones into a single view, separate from the public zone view."
                                    type: bool
                                    returned: Always
                                sync_type:
                                    description: "Type of synchronization, e.g., 'read_only' or 'read_write'."
                                    type: str
                                    returned: Always
                                view_id:
                                    description: "ID of the DNS view."
                                    type: str
                                    returned: Always
                                view_name:
                                    description: "Name of the DNS view."
                                    type: str
                                    returned: Always
                        ipam:
                            description: "IPAM configuration details."
                            type: dict
                            returned: Always
                            contains:
                                dhcp_server:
                                    description: "ID of the DHCP server."
                                    type: str
                                    returned: Always
                                disable_ipam_projection:
                                    description:
                                        - "Flag to control the IPAM Sync/Reconciliation for the provider."
                                    type: bool
                                    returned: Always
                                ip_space:
                                    description: "IP space for the IPAM configuration."
                                    type: str
                                    returned: Always
                created_at:
                    description:
                        - "Timestamp when the object has been created."
                    type: str
                    returned: Always
                deleted_at:
                    description:
                        - "Timestamp when the object has been deleted."
                    type: str
                    returned: Always
                destination_type:
                    description:
                        - "Destination type: DNS / IPAM / ACCOUNT."
                    type: str
                    returned: Always
                id:
                    description:
                        - "Auto-generated unique destination ID. Format BloxID."
                    type: str
                    returned: Always
                updated_at:
                    description:
                        - "Timestamp when the object has been updated."
                    type: str
                    returned: Always
        id:
            description:
                - "Auto-generated unique discovery config ID. Format BloxID."
            type: str
            returned: Always
        last_sync:
            description:
                - "Last sync timestamp."
            type: str
            returned: Always
        name:
            description:
                - "Name of the discovery config."
            type: str
            returned: Always
        provider_type:
            description:
                - "Provider type. Example: Amazon Web Services, Google Cloud Platform, Microsoft Azure."
            type: str
            returned: Always
        source_configs:
            description:
                - "Source configs."
            type: list
            returned: Always
            elements: dict
            contains:
                account_schedule_id:
                    description:
                        - "Account Schedule ID."
                    type: str
                    returned: Always
                accounts:
                    description: "List of source accounts."
                    type: list
                    returned: Always
                    elements: dict
                    contains:
                        composite_status:
                            description: "Composite status of the sync operation."
                            type: str
                            returned: Always
                        composite_status_message:
                            description:
                                - "Status message of the sync operation."
                            type: str
                            returned: Always
                        created_at:
                            description:
                                - "Timestamp when the object has been created."
                            type: str
                            returned: Always
                        deleted_at:
                            description:
                                - "Timestamp when the object has been deleted."
                            type: str
                            returned: Always
                        dhcp_server_id:
                            description: "ID of the DHCP server."
                            type: str
                            returned: Always
                        dns_server_id:
                            description:
                                - "DNS Server ID."
                            type: str
                            returned: Always
                        id:
                            description:
                                - "Auto-generated unique source account ID. Format BloxID."
                            type: str
                            returned: Always
                        last_successful_sync:
                            description:
                                - "Last successful sync timestamp."
                            type: str
                            returned: Always
                        last_sync:
                            description:
                                - "Last sync timestamp."
                            type: str
                            returned: Always
                        name:
                            description:
                                - "Name of the source account."
                            type: str
                            returned: Always
                        parent_id:
                            description:
                                - "Parent ID."
                            type: str
                            returned: Always
                        percent_complete:
                            description:
                                - "Sync progress as a percentage."
                            type: int
                            returned: Always
                        provider_account_id:
                            description: "Provider account ID."
                            type: str
                            returned: Always
                        schedule_id:
                            description:
                                - "Schedule ID."
                            type: str
                            returned: Always
                        state:
                            description: "State of the sync operation."
                            type: str
                            returned: Always
                        status:
                            description:
                                - "Status of the sync operation."
                            type: str
                            returned: Always
                        status_message:
                            description:
                                - "Status message of the sync operation."
                            type: str
                            returned: Always
                        updated_at:
                            description:
                                - "Timestamp when the object has been updated."
                            type: str
                            returned: Always
                cloud_credential_id:
                    description:
                        - "Cloud Credential ID."
                    type: str
                    returned: Always
                created_at:
                    description:
                        - "Timestamp when the object has been created."
                    type: str
                    returned: Always
                credential_config:
                    description:
                        - "Credential configuration. Example: '{ \"access_identifier\": \"arn:aws:iam::1234:role/access_for_discovery\", \"region\": \"us-east-1\", \"enclave\": \"commercial/gov\" }'."
                    type: dict
                    returned: Always
                    contains:
                        access_identifier:
                            description: "Access identifier for the credential."
                            type: str
                            returned: Always
                        enclave:
                            description: "Enclave for the credential."
                            type: str
                            returned: Always
                        region:
                            description: "Region for the credential."
                            type: str
                            returned: Always
                deleted_at:
                    description:
                        - "Timestamp when the object has been deleted."
                    type: str
                    returned: Always
                id:
                    description:
                        - "Auto-generated unique source config ID. Format BloxID."
                    type: str
                    returned: Always
                restricted_to_accounts:
                    description:
                        - "Provider account IDs such as accountID/ SubscriptionID to be restricted for a given source_config."
                    type: list
                    returned: Always
                updated_at:
                    description:
                        - "Timestamp when the object has been updated."
                    type: str
                    returned: Always
        status:
            description:
                - "Status of the sync operation. In single account case, it's the combined status of account & all the destinations statuses. In auto discover case, it's the status of the account discovery only."
            type: str
            returned: Always
        status_message:
            description:
                - "Aggregate status message of the sync operation."
            type: str
            returned: Always
        sync_interval:
            description: "Sync interval for the discovery process."
            type: str
            returned: Always
        tags:
            description:
                - "Tagging specifics."
            type: dict
            returned: Always
        updated_at:
            description:
                - "Timestamp when the object has been updated."
            type: str
            returned: Always
"""  # noqa: E501

from ansible_collections.infoblox.universal_ddi.plugins.module_utils.modules import UniversalDDIAnsibleModule

try:
    from cloud_discovery import ProvidersApi
    from universal_ddi_client import ApiException, NotFoundException
except ImportError:
    pass  # Handled by UniversalDDIAnsibleModule


class ProvidersInfoModule(UniversalDDIAnsibleModule):
    def __init__(self, *args, **kwargs):
        super(ProvidersInfoModule, self).__init__(*args, **kwargs)
        self._existing = None
        self._limit = 1000

    def find_by_id(self):
        try:
            resp = ProvidersApi(self.client).read(self.params["id"])
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

        all_results = []
        offset = 0

        while True:
            try:
                resp = ProvidersApi(self.client).list(offset=offset, limit=self._limit, filter=filter_str)

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
    )

    module = ProvidersInfoModule(
        argument_spec=module_args,
        supports_check_mode=True,
        mutually_exclusive=[
            ["id", "filters", "filter_query"],
        ],
    )
    module.run_command()


if __name__ == "__main__":
    main()
