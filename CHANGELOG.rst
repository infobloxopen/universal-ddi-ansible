=====================================
infoblox.universal\_ddi Release Notes
=====================================

.. contents:: Topics

v1.2.0
======

Release Summary
---------------

Adds full Ansible support for DTC (DNS Traffic Control): new modules for DTC Servers, Pools, Policies, LBDNs, and HTTP/ICMP/SNMP/TCP Health Checks (plus SNMP User Security Models). Also adds SSHFP and HTTPS DNS record support, a new record-protection option to ``dns_record``, zone filtering in ``cloud_discovery_providers``, and several bug fixes across Anycast, DHCP, DNS, IPAM, and Cloud Discovery modules.

Minor Changes
-------------

- cloud_discovery_providers - Added a ``zone_filters`` option to include or exclude specific zones from discovery for AWS, Azure, and GCP providers (https://github.com/infobloxopen/universal-ddi-ansible/pull/68).
- dhcp_ha_group - ``anycast`` mode is deprecated(https://github.com/infobloxopen/universal-ddi-ansible/pull/58).
- dns_record - Added a ``configure_record_protection`` option to set, update, or remove protected-access levels on DNS resource records (https://github.com/infobloxopen/universal-ddi-ansible/pull/51).
- dns_record, dns_record_info - Added a ``target_name`` ``rdata`` sub-option used by HTTPS/SVCB record types (https://github.com/infobloxopen/universal-ddi-ansible/pull/51).
- dns_record, dns_record_info - Added support for managing SSHFP (SSH public key fingerprint) records (https://github.com/infobloxopen/universal-ddi-ansible/pull/61).
- ipam_address_block, ipam_ip_space - Added previously missing ``authoritative_dhcp``, ``hold_reclaimed_time``, and ``hold_reclaimed_time_v6`` inheritance options (https://github.com/infobloxopen/universal-ddi-ansible/pull/58).

Bugfixes
--------

- anycast_config, anycast_config_info - Fixed an invalid ``service`` choice (``DHCP``) that should have been ``NTP`` (https://github.com/infobloxopen/universal-ddi-ansible/pull/58).
- cloud_discovery_providers - Fixed provider deletion to transition the provider to a disabled state before deleting it, as required by the API (https://github.com/infobloxopen/universal-ddi-ansible/pull/68).
- dns_record, ipam_address_block, ipam_ip_space, ipam_subnet - Fixed ``changed`` status reporting by re-reading the resource when the API's update response omits the result object (https://github.com/infobloxopen/universal-ddi-ansible/pull/58).

New Modules
-----------

- infoblox.universal_ddi.dtc_server - Manage DTC Server.
- infoblox.universal_ddi.dtc_server_info - Get DTC Server information.
- infoblox.universal_ddi.dtc_pool - Manage DTC Pool.
- infoblox.universal_ddi.dtc_pool_info - Get DTC Pool information.
- infoblox.universal_ddi.dtc_policy - Manage DTC Policy.
- infoblox.universal_ddi.dtc_policy_info - Get DTC Policy information.
- infoblox.universal_ddi.dtc_lbdn - Manage DTC LBDN.
- infoblox.universal_ddi.dtc_lbdn_info - Get DTC LBDN information.
- infoblox.universal_ddi.dtc_health_check_http - Manage DTC HTTP Health Check.
- infoblox.universal_ddi.dtc_health_check_http_info - Get DTC HTTP Health Check information.
- infoblox.universal_ddi.dtc_health_check_icmp - Manage DTC ICMP Health Check.
- infoblox.universal_ddi.dtc_health_check_icmp_info - Get DTC ICMP Health Check information.
- infoblox.universal_ddi.dtc_health_check_tcp - Manage DTC TCP Health Check.
- infoblox.universal_ddi.dtc_health_check_tcp_info - Get DTC TCP Health Check information.
- infoblox.universal_ddi.dtc_health_check_snmp - Manage DTC SNMP Health Check.
- infoblox.universal_ddi.dtc_health_check_snmp_info - Get DTC SNMP Health Check information.
- infoblox.universal_ddi.dtc_snmp_user_security_model - Manage DTC SNMP User Security Model.
- infoblox.universal_ddi.dtc_snmp_user_security_model_info - Get DTC SNMP User Security Model information.

v1.1.0
======

Release Summary
---------------

- Added support for DHCP and IPAM Federation modules.
- Added support for Cloud Discovery Providers module.
- Added support for DNS View Bulk Copy module.
- Added Support for Tag Filters for Next Available IP.
- Added support for Tag Filter for Next Available Subnet.
- Added support for Tag filters in Next Available Address Block.

New Modules
-----------

- infoblox.universal_ddi.anycast_config - Manage Anycast Config.
- infoblox.universal_ddi.anycast_config_info - Get Anycast Config information.
- infoblox.universal_ddi.anycast_host - Manage Anycast Host.
- infoblox.universal_ddi.anycast_host_info - Get Anycast Host information.
- infoblox.universal_ddi.cloud_discovery_providers - Manage Cloud Discovery Providers.
- infoblox.universal_ddi.cloud_discovery_providers_info - Get Cloud Discovery Providers information.
- infoblox.universal_ddi.dhcp_fixed_address - Manage DHCP Fixed Address.
- infoblox.universal_ddi.dhcp_fixed_address_info - Get DHCP Fixed Address information.
- infoblox.universal_ddi.dhcp_ha_group - Manage DHCP HA Group.
- infoblox.universal_ddi.dhcp_ha_group_info - Get DHCP HA Group information.
- infoblox.universal_ddi.dhcp_host - Manage DHCP Host.
- infoblox.universal_ddi.dhcp_host_info - Get DHCP Host information.
- infoblox.universal_ddi.dhcp_option_code - Manage DHCP Option Code.
- infoblox.universal_ddi.dhcp_option_code_info - Get DHCP Option Code information.
- infoblox.universal_ddi.dhcp_option_group - Manage DHCP Option Group.
- infoblox.universal_ddi.dhcp_option_group_info - Get DHCP Option Group information.
- infoblox.universal_ddi.dhcp_option_space - Manage DHCP Option Space.
- infoblox.universal_ddi.dhcp_option_space_info - Get DHCP Option Space information.
- infoblox.universal_ddi.dhcp_server - Manage DHCP Server.
- infoblox.universal_ddi.dhcp_server_info - Get DHCP Server information.
- infoblox.universal_ddi.dns_view_bulk_copy - Manage DNS View Bulk Copy.
- infoblox.universal_ddi.ipam_federation_federated_block - Manage IPAM Federation Federated Block.
- infoblox.universal_ddi.ipam_federation_federated_block_info - Get IPAM Federation Federated Block information.
- infoblox.universal_ddi.ipam_federation_federated_realm - Manage IPAM Federation Federated Realm.
- infoblox.universal_ddi.ipam_federation_federated_realm_info - Get IPAM Federation Federated Realm information.

v1.0.0
======

Release Summary
---------------

Initial Release for Universal DDI Ansible Collection.

New Modules
-----------

- infoblox.universal_ddi.dns_acl - Manage DNS ACL.
- infoblox.universal_ddi.dns_acl_info - Get DNS ACL information.
- infoblox.universal_ddi.dns_auth_nsg - Manage DNS Auth NSG.
- infoblox.universal_ddi.dns_auth_nsg_info - Get DNS Auth NSG information.
- infoblox.universal_ddi.dns_auth_zone - Manage DNS Auth zone.
- infoblox.universal_ddi.dns_auth_zone_info - Get DNS Auth zone information.
- infoblox.universal_ddi.dns_delegation - Manage DNS delegation.
- infoblox.universal_ddi.dns_delegation_info - Get DNS delegation information.
- infoblox.universal_ddi.dns_forward_nsg - Manage DNS Forward NSG.
- infoblox.universal_ddi.dns_forward_nsg_info - Get DNS Forward NSG information.
- infoblox.universal_ddi.dns_forward_zone - Manage DNS Forward zone.
- infoblox.universal_ddi.dns_forward_zone_info - Get DNS Forward zone information.
- infoblox.universal_ddi.dns_host - Manage DNS Host.
- infoblox.universal_ddi.dns_host_info - Get DNS Host information.
- infoblox.universal_ddi.dns_record - Manage DNS Record.
- infoblox.universal_ddi.dns_record_info - Get DNS Record information.
- infoblox.universal_ddi.dns_server - Manage DNS Server.
- infoblox.universal_ddi.dns_server_info - Get DNS Server information.
- infoblox.universal_ddi.dns_view - Manage DNS View.
- infoblox.universal_ddi.dns_view_info - Get DNS View information.
- infoblox.universal_ddi.infra_host - Manage Infra Host.
- infoblox.universal_ddi.infra_host_info - Get Infra Host information.
- infoblox.universal_ddi.infra_join_token - Manage Infra join token.
- infoblox.universal_ddi.infra_join_token_info - Get Infra join token information.
- infoblox.universal_ddi.infra_service - Manage Infra Service.
- infoblox.universal_ddi.infra_service_info - Get Infra Service information.
- infoblox.universal_ddi.ipam_address - Manage IPAM Address.
- infoblox.universal_ddi.ipam_address_block - Manage IPAM Address Block.
- infoblox.universal_ddi.ipam_address_block_info - Get IPAM Address Block information.
- infoblox.universal_ddi.ipam_address_info - Get IPAM Address information.
- infoblox.universal_ddi.ipam_host - Manage IPAM Host.
- infoblox.universal_ddi.ipam_host_info - Get IPAM Host information.
- infoblox.universal_ddi.ipam_ip_space - Manage IPAM IPSpace.
- infoblox.universal_ddi.ipam_ip_space_info - Get IPAM IPSpace information.
- infoblox.universal_ddi.ipam_next_available_address_block_info - Get next available Address Block information.
- infoblox.universal_ddi.ipam_next_available_ip_info - Get next available IP information.
- infoblox.universal_ddi.ipam_next_available_subnet_info - Get next available Subnet information.
- infoblox.universal_ddi.ipam_range - Manage IPAM Range.
- infoblox.universal_ddi.ipam_range_info - Get IPAM Range information.
- infoblox.universal_ddi.ipam_subnet - Manage IPAM Subnet.
- infoblox.universal_ddi.ipam_subnet_info - Get IPAM Subnet information.
- infoblox.universal_ddi.kerberos_key_info - Get Kerberos Keys information.
- infoblox.universal_ddi.tsig_key - Manage TSIG Keys.
- infoblox.universal_ddi.tsig_key_info - Get TSIG Keys information.
