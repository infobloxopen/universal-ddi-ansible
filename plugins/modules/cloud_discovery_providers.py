#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: Infoblox Inc.
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: cloud_discovery_providers
short_description: Manage Cloud Providers
description:
    - Manage Cloud Providers
version_added: 1.0.0
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
    account_preference:
        description:
            - "Account preference."
        type: str
        required: true
        choices:
            - "single"
            - "multiple"
            - "auto_discover_multiple"
    additional_config:
        description:
            - "Additional configuration."
        type: dict
        suboptions:
            excluded_accounts:
                description: "List of accounts to be excluded from the discovery process."
                type: list
                elements: str
            forward_zone_enabled:
                description: "Flag to enable or disable forwarding of zones."
                type: bool
            internal_ranges_enabled:
                description: "Flag to enable or disable internal range discovery."
                type: bool
            object_type:
                description: "Configuration for object types to be discovered."
                type: dict
                suboptions:
                    discover_new:
                        description: "Flag to enable or disable discovery of new objects."
                        type: bool
                    objects:
                        description: "List of objects to be discovered."
                        type: list
                        elements: dict
                        suboptions:
                            category:
                                description: "Category of the object."
                                type: dict
                                suboptions:
                                    excluded:
                                        description: "Flag to exclude the object category from discovery."
                                        type: bool
                            resource_set:
                                description: "Set of resources to be discovered."
                                type: list
                                elements: dict
                                suboptions:
                                    excluded:
                                        description: "Flag to exclude the resource set from discovery."
                                        type: bool
                    version:
                        description: "Version of the object type configuration."
                        type: float
    credential_preference:
        description:
            - "Credential preference."
        type: dict
        suboptions:
            access_identifier_type:
                description: "Type of access identifier"
                type: str
                choices:
                    - "role_arn"
                    - "tenant_id"
                    - "project_id"
            credential_type:
                description: "Type of credential, e.g., 'static' or 'delegated'."
                type: str
    description:
        description:
            - "Description of the discovery config. Optional."
        type: str
    desired_state:
        description:
            - "Desired state. Default is \"enabled\"."
        type: str
    destination_types_enabled:
        description:
            - "Destinations types enabled: Ex.: DNS, IPAM and ACCOUNT."
        type: list
        elements: str
    destinations:
        description:
            - "Destinations."
        type: list
        elements: dict
        suboptions:
            config:
                description:
                    - Destination configuration includes DNS settings (view name, view ID, consolidated zone data, sync type, split view), IPAM settings (IP space), and account settings.
                type: dict
                suboptions:
                    dns:
                        description: "DNS configuration details."
                        type: dict
                        suboptions:
                            consolidated_zone_data_enabled:
                                description: "Flag to enable or disable consolidated zone data."
                                type: bool
                            split_view_enabled:
                                description:
                                    - "split_view_enabled consolidates private zones into a single view, which is separate from the public zone view."
                                type: bool
                            sync_type:
                                description: "Type of sync operation, e.g., 'read_only' or 'read_write'."
                                type: str
                                choices:
                                    - "read_only"
                                    - "read_write"
                            view_id:
                                description: "ID of the view."
                                type: str
                            view_name:
                                description: "Name of the view."
                                type: str
                    ipam:
                        description: "IPAM configuration details."
                        type: dict
                        suboptions:
                            dhcp_server:
                                description: "DHCP server associated with the IPAM."
                                type: str
                            disable_ipam_projection:
                                description:
                                    - "This flag controls the IPAM Sync/Reconciliation for the provider"
                                type: bool
                            ip_space:
                                description: "IP space associated with the IPAM."
                                type: str
            destination_type:
                description:
                    - "Destination type"
                type: str
                choices:
                    - "DNS"
                    - "IPAM"
                    - "ACCOUNTS"
    name:
        description:
            - "Name of the discovery config."
        type: str
        required: true
    provider_type:
        description:
            - "Provider type."
        type: str
        choices:
            - "Amazon Web Services"
            - "Google Cloud Platform"
            - "Microsoft Azure"
        required: true
    source_configs:
        description:
            - "Source configs."
        type: list
        elements: dict
        suboptions:
            accounts:
                description: "List of source accounts."
                type: list
                elements: dict
                suboptions:
                    composite_status:
                        description: "Composite status of the sync operation."
                        type: str
                    composite_status_message:
                        description:
                            - "Status message of the sync operation."
                        type: str
                    name:
                        description:
                            - "Name of the source account."
                        type: str
                    parent_id:
                        description:
                            - "Parent ID."
                        type: str
                    provider_account_id:
                        description: "Provider account ID."
                        type: str
            cloud_credential_id:
                description:
                    - "Cloud Credential ID."
                type: str
            credential_config:
                description:
                    - "Credential configuration. Ex.: '{ \"access_identifier\": \"arn:aws:iam::1234:role/access_for_discovery\", \"region\": \"us-east-1\", \"enclave\": \"commercial/gov\" }'."
                type: dict
                suboptions:
                    access_identifier:
                        description: "Access identifier for the credential."
                        type: str
                    enclave:
                        description: "Enclave for the credential."
                        type: str
                    region:
                        description: "Region for the credential."
                        type: str
            restricted_to_accounts:
                description:
                    - "Provider account IDs such as accountID/ SubscriptionID to be restricted for a given source_config."
                type: list
                elements: str
    sync_interval:
        description: "Sync interval for the discovery process."
        type: str
        choices:
            - "Auto"
            - "15"
            - "30"
            - "60"
            - "120"
            - "180"
            - "240"
            - "360"
            - "480"
            - "720"
            - "1440"
        default: "Auto"
    tags:
        description:
            - "Tagging specifics."
        type: dict

extends_documentation_fragment:
    - infoblox.universal_ddi.common
"""  # noqa: E501

EXAMPLES = r"""
    - name: Create a View
      infoblox.universal_ddi.dns_view:
        name: "dnsView"
        state: present
      register: _view

    - name: Create an AWS cloud discovery provider 
      infoblox.universal_ddi.cloud_discovery_providers:
        name: "aws_provider_minimal"
        provider_type: "Amazon Web Services"
        account_preference: "single"
        credential_preference:
          access_identifier_type: "account_id"
          credential_type: "static"
        source_configs:
          - credential_config:
                access_identifier: "arn:aws:iam::123456789123:role/infoblox_discovery"
        state: present
        register: aws_provider

    - name: Create an AWS cloud discovery provider with additional attributes
      infoblox.universal_ddi.cloud_discovery_providers:
        name: "aws_provider_additional"
        provider_type: "Amazon Web Services"
        account_preference: "single"
        credential_preference:
          access_identifier_type: "account_id"
          credential_type: "static"
        source_configs:
          - credential_config:
                access_identifier: "arn:aws:iam::123456789123:role/infoblox_discovery"
        additional_config:
          excluded_accounts:
            - "123456789012"
          forward_zone_enabled: true
          internal_ranges_enabled: true
          object_type:
            discover_new: true
        destination_types_enabled:
          - "DNS"
        destinations:
          - config:
              dns:
                sync_type: "read_only"
                view_id: "{{ _view.id }}"
            destination_type: "DNS"
        sync_interval: "15"
        desired_state: "disabled"
        tags:
          environment: "production"
        state: present

    - name: Delete an AWS cloud discovery provider
      infoblox.universal_ddi.cloud_discovery_providers:
        name: "aws_provider_minimal"
        provider_type: "Amazon Web Services"
        account_preference: "single"
        state: absent
        
    - name: Create a GCP cloud discovery provider 
      infoblox.universal_ddi.cloud_discovery_providers:
        name: "gcp_provider_minimal"
        provider_type: "Google Cloud Platform"
        account_preference: "single"
        credential_preference:
          access_identifier_type: "project_id"
          credential_type: "dynamic"
        source_configs:
          - credential_config:
                access_identifier: "123456789012"
        state: present
        register: gcp_provider

    - name: Create an Azure cloud discovery provider 
      infoblox.universal_ddi.cloud_discovery_providers:
        name: "azure_provider_minimal"
        provider_type: "Microsoft Azure"
        account_preference: "single"
        credential_preference:
          access_identifier_type: "subscription_id"
          credential_type: "static"
        source_configs:
          - credential_config:
                access_identifier: "123456789012"
        state: present
        register: azure_provider
"""  # noqa: E501

RETURN = r"""
id:
    description:
        - ID of the Providers object
    type: str
    returned: Always
item:
    description:
        - Providers object
    type: complex
    returned: Always
    contains:
        account_preference:
            description:
                - "Account preference. For ex.: single, multiple, auto-discover-multiple."
            type: str
            returned: Always
        additional_config:
            description:
                - "Additional configuration. Ex.: '{ \"excluded_object_types\": [], \"exclusion_account_list\": [], \"zone_forwarding\": \"true\" or \"false\" }'."
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
                                            description: "Flag to exclude the object category from discovery."
                                            type: bool
                                            returned: Always
                                        id:
                                            description: "ID of the object category."
                                            type: str
                                            returned: Always
                                resource_set:
                                    description: "Set of resources to be discovered."
                                    type: list
                                    returned: Always
                                    elements: dict
                                    contains:
                                        excluded:
                                            description: "Flag to exclude the resource set from discovery."
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
                - "Credential preference. Ex.: '{ \"type\": \"static\" or \"delegated\", \"access_identifier_type\": \"role_arn\" or \"tenant_id\" or \"project_id\" }'."
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
                - "Desired state. Default is \"enabled\"."
            type: str
            returned: Always
        destination_types_enabled:
            description:
                - "Destinations types enabled: Ex.: DNS, IPAM and ACCOUNT."
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
                        - "Destination configuration. Ex.: '{ \"dns\": { \"view_name\": \"view 1\", \"view_id\": \"dns/view/v1\", \"consolidated_zone_data_enabled\": false, \"sync_type\": \"read_only/read_write\" \"split_view_enabled\": false }, \"ipam\": { \"ip_space\": \"\", }, \"account\": {}, }'."
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
                                        - "split_view_enabled consolidates private zones into a single view, which is separate from the public zone view."
                                    type: bool
                                    returned: Always
                                sync_type:
                                    description: "Type of sync operation, e.g., 'read_only' or 'read_write'."
                                    type: str
                                    returned: Always
                                view_id:
                                    description: "ID of the view."
                                    type: str
                                    returned: Always
                                view_name:
                                    description: "Name of the view."
                                    type: str
                                    returned: Always
                        ipam:
                            description: "IPAM configuration details."
                            type: dict
                            returned: Always
                            contains:
                                dhcp_server:
                                    description: "DHCP server associated with the IPAM."
                                    type: str
                                    returned: Always
                                disable_ipam_projection:
                                    description:
                                        - "This flag controls the IPAM Sync/Reconciliation for the provider."
                                    type: bool
                                    returned: Always
                                ip_space:
                                    description: "IP space associated with the IPAM."
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
                - "Provider type. Ex.: Amazon Web Services, Google Cloud Platform, Microsoft Azure."
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
                    description: "Account Schedule ID."
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
                        - "Credential configuration. Ex.: '{ \"access_identifier\": \"arn:aws:iam::1234:role/access_for_discovery\", \"region\": \"us-east-1\", \"enclave\": \"commercial/gov\" }'."
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
                - "Status of the sync operation. In single account case, Its the combined status of account & all the destinations statuses In auto discover case, Its the status of the account discovery only."
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
    from cloud_discovery import DiscoveryConfig, ProvidersApi
    from universal_ddi_client import ApiException, NotFoundException
except ImportError:
    pass  # Handled by UniversalDDIAnsibleModule


class ProvidersModule(UniversalDDIAnsibleModule):
    def __init__(self, *args, **kwargs):
        super(ProvidersModule, self).__init__(*args, **kwargs)

        exclude = ["state", "csp_url", "api_key", "portal_url", "portal_key", "id"]
        self._payload_params = {k: v for k, v in self.params.items() if v is not None and k not in exclude}
        self._payload = DiscoveryConfig.from_dict(self._payload_params)
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
                resp = ProvidersApi(self.client).read(self.params["id"])
                return resp.result
            except NotFoundException as e:
                if self.params["state"] == "absent":
                    return None
                raise e
        else:
            filter = f"name=='{self.params['name']}'"
            resp = ProvidersApi(self.client).list(filter=filter)

            # If no results, set results to empty list
            if not resp.results:
                resp.results = []

            if len(resp.results) == 1:
                return resp.results[0]
            if len(resp.results) > 1:
                self.fail_json(msg=f"Found multiple Providers: {resp.results}")
            if len(resp.results) == 0:
                return None

    def create(self):
        if self.check_mode:
            return None

        resp = ProvidersApi(self.client).create(body=self.payload)
        return resp.result.model_dump(by_alias=True, exclude_none=True)

    def update(self):
        if self.check_mode:
            return None

        for i in range(len(self.payload.source_configs)):
            self.payload.source_configs[i].id = self.existing.source_configs[i].id

        ProvidersApi(self.client).update(id=self.existing.id, body=self.payload)

    def delete(self):
        if self.check_mode:
            return

        ProvidersApi(self.client).delete(self.existing.id)

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
                result["msg"] = "Providers created"
            elif self.params["state"] == "present" and self.existing is not None:
                if self.payload_changed():
                    self.update()
                    result["changed"] = True
                    result["msg"] = "Providers updated"
            elif self.params["state"] == "absent" and self.existing is not None:
                self.delete()
                result["changed"] = True
                result["msg"] = "Providers deleted"

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
        account_preference=dict(type="str", choices=["single", "multiple", "auto_discover_multiple"], required=True),
        additional_config=dict(
            type="dict",
            options=dict(
                excluded_accounts=dict(type="list", elements="str"),
                forward_zone_enabled=dict(type="bool"),
                internal_ranges_enabled=dict(type="bool"),
                object_type=dict(
                    type="dict",
                    options=dict(
                        discover_new=dict(type="bool"),
                        objects=dict(
                            type="list",
                            elements="dict",
                            options=dict(
                                category=dict(
                                    type="dict",
                                    options=dict(
                                        excluded=dict(type="bool"),
                                    ),
                                ),
                                resource_set=dict(
                                    type="list",
                                    elements="dict",
                                    options=dict(
                                        excluded=dict(type="bool"),
                                    ),
                                ),
                            ),
                        ),
                        version=dict(type="float"),
                    ),
                ),
            ),
        ),
        credential_preference=dict(
            type="dict",
            options=dict(
                access_identifier_type=dict(type="str", choices=["role_arn", "tenant_id", "project_id"]),
                credential_type=dict(type="str"),
            ),
        ),
        description=dict(type="str"),
        desired_state=dict(type="str"),
        destination_types_enabled=dict(type="list", elements="str"),
        destinations=dict(
            type="list",
            elements="dict",
            options=dict(
                config=dict(
                    type="dict",
                    options=dict(
                        dns=dict(
                            type="dict",
                            options=dict(
                                consolidated_zone_data_enabled=dict(type="bool"),
                                split_view_enabled=dict(type="bool"),
                                sync_type=dict(type="str", choices=["read_only", "read_write"]),
                                view_id=dict(type="str"),
                                view_name=dict(type="str"),
                            ),
                        ),
                        ipam=dict(
                            type="dict",
                            options=dict(
                                dhcp_server=dict(type="str"),
                                disable_ipam_projection=dict(type="bool"),
                                ip_space=dict(type="str"),
                            ),
                        ),
                    ),
                ),
                destination_type=dict(type="str", choices=["DNS", "IPAM", "ACCOUNTS"]),
            ),
        ),
        name=dict(type="str", required=True),
        provider_type=dict(
            type="str", choices=["Amazon Web Services", "Google Cloud Platform", "Microsoft Azure"], required=True
        ),
        source_configs=dict(
            type="list",
            elements="dict",
            options=dict(
                accounts=dict(
                    type="list",
                    elements="dict",
                    options=dict(
                        composite_status=dict(type="str"),
                        composite_status_message=dict(type="str"),
                        name=dict(type="str"),
                        parent_id=dict(type="str"),
                        provider_account_id=dict(type="str"),
                    ),
                ),
                cloud_credential_id=dict(type="str"),
                credential_config=dict(
                    type="dict",
                    options=dict(
                        access_identifier=dict(type="str"),
                        enclave=dict(type="str"),
                        region=dict(type="str"),
                    ),
                ),
                restricted_to_accounts=dict(type="list", elements="str"),
            ),
        ),
        sync_interval=dict(
            type="str",
            choices=["Auto", "15", "30", "60", "120", "180", "240", "360", "480", "720", "1440"],
            default="Auto",
        ),
        tags=dict(type="dict"),
    )

    module = ProvidersModule(
        argument_spec=module_args,
        supports_check_mode=True,
        required_if=[("state", "present", ["name", "account_preference", "provider_type"])],
    )

    module.run_command()


if __name__ == "__main__":
    main()
