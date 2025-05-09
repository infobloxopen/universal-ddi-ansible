#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: Infoblox Inc.
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: dhcp_server_info
short_description: Retrieves DHCP Config Profiles.
description:
    - Retrieves information about existing DHCP Config Profiles.
    - A Server (DHCP Config Profile) is a named configuration profile that can be shared for specified list of hosts.
version_added: 1.1.0
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
    - name: Get DHCP server information by ID
      infoblox.universal_ddi.dhcp_server_info:
        id: "{{ dhcp_server.id }}"

    - name: Get DHCP server information by name
      infoblox.universal_ddi.dhcp_server_info:
        filters:
          name: "example-dhcp-server"

    - name: Get DHCP server information by tag_filters
      infoblox.universal_ddi.dhcp_server_info:
        tag_filters:
          location: "site-1"
          
    - name: Get DHCP server information by filter query
      infoblox.universal_ddi.dns_acl_info:
        filter_query: "name=='example-dhcp-server'"
        
"""  # noqa: E501

RETURN = r"""
id:
    description:
        - ID of the Server object
    type: str
    returned: Always
objects:
    description:
        - Server object
    type: list
    elements: dict
    returned: Always
    contains:
        client_principal:
            description:
                - "The Kerberos principal name. It uses the typical Kerberos notation: <SERVICE-NAME>/<server-domain-name>@<REALM>."
                - "Defaults to empty."
            type: str
            returned: Always
        comment:
            description:
                - "The description for the DHCP Config Profile. May contain 0 to 1024 characters. Can include UTF-8."
            type: str
            returned: Always
        created_at:
            description:
                - "Time when the object has been created."
            type: str
            returned: Always
        ddns_client_update:
            description:
                - "Controls who does the DDNS updates."
                - "Valid values are:"
                - "* I(client): DHCP server updates DNS if requested by client."
                - "* I(server): DHCP server always updates DNS, overriding an update request from the client, unless the client requests no updates."
                - "* I(ignore): DHCP server always updates DNS, even if the client says not to."
                - "* I(over_client_update): Same as I(server). DHCP server always updates DNS, overriding an update request from the client, unless the client requests no updates."
                - "* I(over_no_update): DHCP server updates DNS even if the client requests that no updates be done. If the client requests to do the update, DHCP server allows it."
                - "Defaults to I(client)."
            type: str
            returned: Always
        ddns_conflict_resolution_mode:
            description:
                - "The mode used for resolving conflicts while performing DDNS updates."
                - "Valid values are:"
                - "* I(check_with_dhcid): It includes adding a DHCID record and checking that record via conflict detection as per RFC 4703."
                - "* I(no_check_with_dhcid): This will ignore conflict detection but add a DHCID record when creating/updating an entry."
                - "* I(check_exists_with_dhcid): This will check if there is an existing DHCID record but does not verify the value of the record matches the update. This will also update the DHCID record for the entry."
                - "* I(no_check_without_dhcid): This ignores conflict detection and will not add a DHCID record when creating/updating a DDNS entry."
                - "Defaults to I(check_with_dhcid)."
            type: str
            returned: Always
        ddns_domain:
            description:
                - "The domain suffix for DDNS updates. FQDN, may be empty."
                - "Required if I(ddns_enabled) is true."
                - "Defaults to empty."
            type: str
            returned: Always
        ddns_enabled:
            description:
                - "Indicates if DDNS updates should be performed for leases. All other I(ddns)*_ configuration is ignored when this flag is unset."
                - "At a minimum, I(ddns_domain) and I(ddns_zones) must be configured to enable DDNS."
                - "Defaults to I(false)."
            type: bool
            returned: Always
        ddns_generate_name:
            description:
                - "Indicates if DDNS should generate a hostname when not supplied by the client."
                - "Defaults to I(false)."
            type: bool
            returned: Always
        ddns_generated_prefix:
            description:
                - "The prefix used in the generation of an FQDN."
                - "When generating a name, DHCP server will construct the name in the format: [ddns-generated-prefix]-[address-text].[ddns-qualifying-suffix]. where address-text is simply the lease IP address converted to a hyphenated string."
                - "Defaults to \"myhost\"."
            type: str
            returned: Always
        ddns_send_updates:
            description:
                - "Determines if DDNS updates are enabled at the server level. Defaults to I(true)."
            type: bool
            returned: Always
        ddns_ttl_percent:
            description:
                - "DDNS TTL value - to be calculated as a simple percentage of the lease's lifetime, using the parameter's value as the percentage. It is specified as a percentage (e.g. 25, 75). Defaults to unspecified."
            type: float
            returned: Always
        ddns_update_on_renew:
            description:
                - "Instructs the DHCP server to always update the DNS information when a lease is renewed even if its DNS information has not changed."
                - "Defaults to I(false)."
            type: bool
            returned: Always
        ddns_use_conflict_resolution:
            description:
                - "When true, DHCP server will apply conflict resolution, as described in RFC 4703, when attempting to fulfill the update request."
                - "When false, DHCP server will simply attempt to update the DNS entries per the request, regardless of whether or not they conflict with existing entries owned by other DHCP4 clients."
                - "Defaults to I(true)."
            type: bool
            returned: Always
        ddns_zones:
            description:
                - "The DNS zones that DDNS updates can be sent to. There is no resolver fallback. The target zone must be explicitly configured for the update to be performed."
                - "Updates are sent to the closest enclosing zone."
                - "Error if I(ddns_enabled) is I(true) and the I(ddns_domain) does not have a corresponding entry in I(ddns_zones)."
                - "Error if there are items with duplicate zone in the list."
                - "Defaults to empty list."
            type: list
            returned: Always
            elements: dict
            contains:
                fqdn:
                    description:
                        - "Zone FQDN."
                        - "If I(zone) is defined, the I(fqdn) field must be empty."
                    type: str
                    returned: Always
                gss_tsig_enabled:
                    description:
                        - "I(gss_tsig_enabled) enables/disables GSS-TSIG signed dynamic updates."
                        - "Defaults to I(false)."
                    type: bool
                    returned: Always
                nameservers:
                    description:
                        - "The Nameservers in the zone."
                        - "Each nameserver IP should be unique across the list of nameservers."
                    type: list
                    returned: Always
                    elements: dict
                    contains:
                        client_principal:
                            description:
                                - "The Kerberos principal name. It uses the typical Kerberos notation: <SERVICE-NAME>/<server-domain-name>@<REALM>."
                                - "Defaults to empty."
                            type: str
                            returned: Always
                        gss_tsig_fallback:
                            description:
                                - "The behavior when GSS-TSIG should be used (a matching external DNS server is configured) but no GSS-TSIG key is available. If configured to I(false) (the default) this DNS server is skipped, if configured to I(true) the DNS server is ignored and the DNS update is sent with the configured DHCP-DDNS protection e.g. TSIG key or without any protection when none was configured."
                                - "Defaults to I(false)."
                            type: bool
                            returned: Always
                        kerberos_rekey_interval:
                            description:
                                - "Time interval (in seconds) the keys for each configured external DNS server are checked for rekeying, i.e. a new key is created to replace the current usable one when its age is greater than the I(kerberos_rekey_interval) value."
                                - "Defaults to 120 seconds."
                            type: int
                            returned: Always
                        kerberos_retry_interval:
                            description:
                                - "Time interval (in seconds) to retry to create a key if any error occurred previously for any configured external DNS server."
                                - "Defaults to 30 seconds."
                            type: int
                            returned: Always
                        kerberos_tkey_lifetime:
                            description:
                                - "Lifetime (in seconds) of GSS-TSIG keys in the TKEY protocol."
                                - "Defaults to 160 seconds."
                            type: int
                            returned: Always
                        kerberos_tkey_protocol:
                            description:
                                - "Determines which protocol is used to establish the security context with the external DNS servers, TCP or UDP."
                                - "Defaults to I(tcp)."
                            type: str
                            returned: Always
                        nameserver:
                            description: "The Nameservers in the zone.Each nameserver IP should be unique across the list of nameservers."
                            type: str
                            returned: Always
                        server_principal:
                            description:
                                - "The Kerberos principal name of this DNS server that will receive updates."
                                - "Defaults to empty."
                            type: str
                            returned: Always
                tsig_enabled:
                    description:
                        - "Indicates if TSIG key should be used for the update."
                        - "Defaults to I(false)."
                    type: bool
                    returned: Always
                tsig_key:
                    description:
                        - "The TSIG key. Required if I(tsig_enabled) is I(true)."
                        - "Defaults to empty."
                    type: dict
                    returned: Always
                    contains:
                        algorithm:
                            description:
                                - "TSIG key algorithm."
                                - "Valid values are:"
                                - "* I(hmac_sha256)"
                                - "* I(hmac_sha1)"
                                - "* I(hmac_sha224)"
                                - "* I(hmac_sha384)"
                                - "* I(hmac_sha512)"
                            type: str
                            returned: Always
                        comment:
                            description:
                                - "The description for the TSIG key. May contain 0 to 1024 characters. Can include UTF-8."
                            type: str
                            returned: Always
                        key:
                            description:
                                - "The resource identifier."
                            type: str
                            returned: Always
                        name:
                            description:
                                - "The TSIG key name, FQDN."
                            type: str
                            returned: Always
                        protocol_name:
                            description:
                                - "The TSIG key name in punycode."
                            type: str
                            returned: Always
                        secret:
                            description:
                                - "The TSIG key secret, base64 string."
                            type: str
                            returned: Always
                view:
                    description:
                        - "The resource identifier."
                    type: str
                    returned: Always
                view_name:
                    description:
                        - "The name of the view."
                    type: str
                    returned: Always
                zone:
                    description:
                        - "The resource identifier."
                    type: str
                    returned: Always
        dhcp_config:
            description:
                - "The DHCP configuration for the profile. This controls how leases are issued."
            type: dict
            returned: Always
            contains:
                abandoned_reclaim_time:
                    description:
                        - "The abandoned reclaim time in seconds for IPV4 clients."
                    type: int
                    returned: Always
                abandoned_reclaim_time_v6:
                    description:
                        - "The abandoned reclaim time in seconds for IPV6 clients."
                    type: int
                    returned: Always
                allow_unknown:
                    description:
                        - "Disable to allow leases only for known IPv4 clients, those for which a fixed address is configured."
                    type: bool
                    returned: Always
                allow_unknown_v6:
                    description:
                        - "Disable to allow leases only for known IPV6 clients, those for which a fixed address is configured."
                    type: bool
                    returned: Always
                echo_client_id:
                    description:
                        - "Enable/disable to include/exclude the client id when responding to discover or request."
                    type: bool
                    returned: Always
                filters:
                    description:
                        - "The resource identifier."
                    type: list
                    returned: Always
                filters_large_selection:
                    description:
                        - "The resource identifier."
                    type: list
                    returned: Always
                filters_v6:
                    description:
                        - "The resource identifier."
                    type: list
                    returned: Always
                ignore_client_uid:
                    description:
                        - "Enable to ignore the client UID when issuing a DHCP lease. Use this option to prevent assigning two IP addresses for a client which does not have a UID during one phase of PXE boot but acquires one for the other phase."
                    type: bool
                    returned: Always
                ignore_list:
                    description:
                        - "The list of clients to ignore requests from."
                    type: list
                    returned: Always
                    elements: dict
                    contains:
                        type:
                            description:
                                - "Type of ignore matching: client to ignore by client identifier (client hex or client text) or hardware to ignore by hardware identifier (MAC address). It can have one of the following values:"
                                - "* I(client_hex),"
                                - "* I(client_text),"
                                - "* I(hardware)."
                            type: str
                            returned: Always
                        value:
                            description:
                                - "Value to match."
                            type: str
                            returned: Always
                lease_time:
                    description:
                        - "The lease duration in seconds."
                    type: int
                    returned: Always
                lease_time_v6:
                    description:
                        - "The lease duration in seconds for IPV6 clients."
                    type: int
                    returned: Always
        dhcp_options:
            description:
                - "The list of DHCP options or group of options for IPv4. An option list is ordered and may include both option groups and specific options. Multiple occurences of the same option or group is not an error. The last occurence of an option in the list will be used."
                - "Error if the graph of referenced groups contains cycles."
                - "Defaults to empty list."
            type: list
            returned: Always
            elements: dict
            contains:
                group:
                    description:
                        - "The resource identifier."
                    type: str
                    returned: Always
                option_code:
                    description:
                        - "The resource identifier."
                    type: str
                    returned: Always
                option_value:
                    description:
                        - "The option value."
                    type: str
                    returned: Always
                type:
                    description:
                        - "The type of item."
                        - "Valid values are:"
                        - "* I(group)"
                        - "* I(option)"
                    type: str
                    returned: Always
        dhcp_options_v6:
            description:
                - "The list of DHCP options or group of options for IPv6. An option list is ordered and may include both option groups and specific options. Multiple occurences of the same option or group is not an error. The last occurence of an option in the list will be used."
                - "Error if the graph of referenced groups contains cycles."
                - "Defaults to empty list."
            type: list
            returned: Always
            elements: dict
            contains:
                group:
                    description:
                        - "The resource identifier."
                    type: str
                    returned: Always
                option_code:
                    description:
                        - "The resource identifier."
                    type: str
                    returned: Always
                option_value:
                    description:
                        - "The option value."
                    type: str
                    returned: Always
                type:
                    description:
                        - "The type of item."
                        - "Valid values are:"
                        - "* I(group)"
                        - "* I(option)"
                    type: str
                    returned: Always
        gss_tsig_fallback:
            description:
                - "The behavior when GSS-TSIG should be used (a matching external DNS server is configured) but no GSS-TSIG key is available. If configured to I(false) (the default) this DNS server is skipped, if configured to I(true) the DNS server is ignored and the DNS update is sent with the configured DHCP-DDNS protection e.g. TSIG key or without any protection when none was configured."
                - "Defaults to I(false)."
            type: bool
            returned: Always
        header_option_filename:
            description:
                - "The configuration for header option filename field."
            type: str
            returned: Always
        header_option_server_address:
            description:
                - "The configuration for header option server address field."
            type: str
            returned: Always
        header_option_server_name:
            description:
                - "The configuration for header option server name field."
            type: str
            returned: Always
        hostname_rewrite_char:
            description:
                - "The character to replace non-matching characters with, when hostname rewrite is enabled."
                - "Any single ASCII character or no character if the invalid characters should be removed without replacement."
                - "Defaults to \"-\"."
            type: str
            returned: Always
        hostname_rewrite_enabled:
            description:
                - "Indicates if client supplied hostnames will be rewritten prior to DDNS update by replacing every character that does not match I(hostname_rewrite_regex) by I(hostname_rewrite_char)."
                - "Defaults to I(false)."
            type: bool
            returned: Always
        hostname_rewrite_regex:
            description:
                - "The regex bracket expression to match valid characters."
                - "Must begin with \"[\" and end with \"]\" and be a compilable POSIX regex."
                - "Defaults to \"[^a-zA-Z0-9_.]\"."
            type: str
            returned: Always
        id:
            description:
                - "The resource identifier."
            type: str
            returned: Always
        inheritance_sources:
            description:
                - "The inheritance configuration."
            type: dict
            returned: Always
            contains:
                ddns_block:
                    description:
                        - "The inheritance configuration for I(ddns_enabled), I(ddns_send_updates), I(ddns_domain), I(ddns_zones) fields from I(Server) object."
                    type: dict
                    returned: Always
                    contains:
                        action:
                            description:
                                - "The inheritance setting."
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
                            type: dict
                            returned: Always
                            contains:
                                client_principal:
                                    description:
                                        - "The Kerberos principal name. It uses the typical Kerberos notation: <SERVICE-NAME>/<server-domain-name>@<REALM>."
                                        - "Defaults to empty."
                                    type: str
                                    returned: Always
                                ddns_domain:
                                    description:
                                        - "The domain name for DDNS."
                                    type: str
                                    returned: Always
                                ddns_enabled:
                                    description:
                                        - "Indicates if DDNS is enabled."
                                    type: bool
                                    returned: Always
                                ddns_send_updates:
                                    description:
                                        - "Determines if DDNS updates are enabled at this level."
                                    type: bool
                                    returned: Always
                                ddns_zones:
                                    description:
                                        - "The list of DDNS zones."
                                    type: list
                                    returned: Always
                                    elements: dict
                                    contains:
                                        fqdn:
                                            description:
                                                - "Zone FQDN."
                                                - "If I(zone) is defined, the I(fqdn) field must be empty."
                                            type: str
                                            returned: Always
                                        gss_tsig_enabled:
                                            description:
                                                - "I(gss_tsig_enabled) enables/disables GSS-TSIG signed dynamic updates."
                                                - "Defaults to I(false)."
                                            type: bool
                                            returned: Always
                                        nameservers:
                                            description:
                                                - "The Nameservers in the zone."
                                                - "Each nameserver IP should be unique across the list of nameservers."
                                            type: list
                                            returned: Always
                                            elements: dict
                                            contains:
                                                client_principal:
                                                    description:
                                                        - "The Kerberos principal name. It uses the typical Kerberos notation: <SERVICE-NAME>/<server-domain-name>@<REALM>."
                                                        - "Defaults to empty."
                                                    type: str
                                                    returned: Always
                                                gss_tsig_fallback:
                                                    description:
                                                        - "The behavior when GSS-TSIG should be used (a matching external DNS server is configured) but no GSS-TSIG key is available. If configured to I(false) (the default) this DNS server is skipped, if configured to I(true) the DNS server is ignored and the DNS update is sent with the configured DHCP-DDNS protection e.g. TSIG key or without any protection when none was configured."
                                                        - "Defaults to I(false)."
                                                    type: bool
                                                    returned: Always
                                                kerberos_rekey_interval:
                                                    description:
                                                        - "Time interval (in seconds) the keys for each configured external DNS server are checked for rekeying, i.e. a new key is created to replace the current usable one when its age is greater than the I(kerberos_rekey_interval) value."
                                                        - "Defaults to 120 seconds."
                                                    type: int
                                                    returned: Always
                                                kerberos_retry_interval:
                                                    description:
                                                        - "Time interval (in seconds) to retry to create a key if any error occurred previously for any configured external DNS server."
                                                        - "Defaults to 30 seconds."
                                                    type: int
                                                    returned: Always
                                                kerberos_tkey_lifetime:
                                                    description:
                                                        - "Lifetime (in seconds) of GSS-TSIG keys in the TKEY protocol."
                                                        - "Defaults to 160 seconds."
                                                    type: int
                                                    returned: Always
                                                kerberos_tkey_protocol:
                                                    description:
                                                        - "Determines which protocol is used to establish the security context with the external DNS servers, TCP or UDP."
                                                        - "Defaults to I(tcp)."
                                                    type: str
                                                    returned: Always
                                                nameserver:
                                                    description: "The Nameservers in the zone.Each nameserver IP should be unique across the list of nameservers."
                                                    type: str
                                                    returned: Always
                                                server_principal:
                                                    description:
                                                        - "The Kerberos principal name of this DNS server that will receive updates."
                                                        - "Defaults to empty."
                                                    type: str
                                                    returned: Always
                                        tsig_enabled:
                                            description:
                                                - "Indicates if TSIG key should be used for the update."
                                                - "Defaults to I(false)."
                                            type: bool
                                            returned: Always
                                        tsig_key:
                                            description:
                                                - "The TSIG key. Required if I(tsig_enabled) is I(true)."
                                                - "Defaults to empty."
                                            type: dict
                                            returned: Always
                                            contains:
                                                algorithm:
                                                    description:
                                                        - "TSIG key algorithm."
                                                        - "Valid values are:"
                                                        - "* I(hmac_sha256)"
                                                        - "* I(hmac_sha1)"
                                                        - "* I(hmac_sha224)"
                                                        - "* I(hmac_sha384)"
                                                        - "* I(hmac_sha512)"
                                                    type: str
                                                    returned: Always
                                                comment:
                                                    description:
                                                        - "The description for the TSIG key. May contain 0 to 1024 characters. Can include UTF-8."
                                                    type: str
                                                    returned: Always
                                                key:
                                                    description:
                                                        - "The resource identifier."
                                                    type: str
                                                    returned: Always
                                                name:
                                                    description:
                                                        - "The TSIG key name, FQDN."
                                                    type: str
                                                    returned: Always
                                                protocol_name:
                                                    description:
                                                        - "The TSIG key name in punycode."
                                                    type: str
                                                    returned: Always
                                                secret:
                                                    description:
                                                        - "The TSIG key secret, base64 string."
                                                    type: str
                                                    returned: Always
                                        view:
                                            description:
                                                - "The resource identifier."
                                            type: str
                                            returned: Always
                                        view_name:
                                            description:
                                                - "The name of the view."
                                            type: str
                                            returned: Always
                                        zone:
                                            description:
                                                - "The resource identifier."
                                            type: str
                                            returned: Always
                                gss_tsig_fallback:
                                    description:
                                        - "The behavior when GSS-TSIG should be used (a matching external DNS server is configured) but no GSS-TSIG key is available. If configured to I(false) (the default) this DNS server is skipped, if configured to I(true) the DNS server is ignored and the DNS update is sent with the configured DHCP-DDNS protection e.g. TSIG key or without any protection when none was configured."
                                        - "Defaults to I(false)."
                                    type: bool
                                    returned: Always
                                kerberos_kdc:
                                    description:
                                        - "Address of Kerberos Key Distribution Center."
                                        - "Defaults to empty."
                                    type: str
                                    returned: Always
                                kerberos_keys:
                                    description:
                                        - "I(kerberos_keys) contains a list of keys for GSS-TSIG signed dynamic updates."
                                        - "Defaults to empty."
                                    type: list
                                    returned: Always
                                    elements: dict
                                    contains:
                                        algorithm:
                                            description:
                                                - "Encryption algorithm of the key in accordance with RFC 3961."
                                            type: str
                                            returned: Always
                                        domain:
                                            description:
                                                - "Kerberos realm of the principal."
                                            type: str
                                            returned: Always
                                        key:
                                            description:
                                                - "The resource identifier."
                                            type: str
                                            returned: Always
                                        principal:
                                            description:
                                                - "Kerberos principal associated with key."
                                            type: str
                                            returned: Always
                                        uploaded_at:
                                            description:
                                                - "Upload time for the key."
                                            type: str
                                            returned: Always
                                        version:
                                            description:
                                                - "The version number (KVNO) of the key."
                                            type: int
                                            returned: Always
                                kerberos_rekey_interval:
                                    description:
                                        - "Time interval (in seconds) the keys for each configured external DNS server are checked for rekeying, i.e. a new key is created to replace the current usable one when its age is greater than the rekey_interval value."
                                        - "Defaults to 120 seconds."
                                    type: int
                                    returned: Always
                                kerberos_retry_interval:
                                    description:
                                        - "Time interval (in seconds) to retry to create a key if any error occurred previously for any configured external DNS server."
                                        - "Defaults to 30 seconds."
                                    type: int
                                    returned: Always
                                kerberos_tkey_lifetime:
                                    description:
                                        - "Lifetime (in seconds) of GSS-TSIG keys in the TKEY protocol."
                                        - "Defaults to 160 seconds."
                                    type: int
                                    returned: Always
                                kerberos_tkey_protocol:
                                    description:
                                        - "Determines which protocol is used to establish the security context with the external DNS servers, TCP or UDP."
                                        - "Defaults to I(tcp)."
                                    type: str
                                    returned: Always
                                server_principal:
                                    description:
                                        - "The Kerberos principal name of the external DNS server that will receive updates."
                                        - "Defaults to empty."
                                    type: str
                                    returned: Always
                ddns_client_update:
                    description:
                        - "The inheritance configuration for I(ddns_client_update) field from I(Server) object."
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
                            type: str
                            returned: Always
                ddns_conflict_resolution_mode:
                    description:
                        - "The inheritance configuration for I(ddns_conflict_resolution_mode) field from I(Server) object."
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
                            type: str
                            returned: Always
                ddns_hostname_block:
                    description:
                        - "The inheritance configuration for I(ddns_generate_name) and I(ddns_generated_prefix) fields from I(Server) object."
                    type: dict
                    returned: Always
                    contains:
                        action:
                            description:
                                - "The inheritance setting."
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
                            type: dict
                            returned: Always
                            contains:
                                ddns_generate_name:
                                    description:
                                        - "Indicates if DDNS should generate a hostname when not supplied by the client."
                                    type: bool
                                    returned: Always
                                ddns_generated_prefix:
                                    description:
                                        - "The prefix used in the generation of an FQDN."
                                    type: str
                                    returned: Always
                ddns_ttl_percent:
                    description:
                        - "The inheritance configuration for I(ddns_ttl_percent) field from I(Server) object."
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
                            type: float
                            returned: Always
                ddns_update_on_renew:
                    description:
                        - "The inheritance configuration for I(ddns_update_on_renew) field from I(Server) object."
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
                            type: bool
                            returned: Always
                ddns_use_conflict_resolution:
                    description:
                        - "The inheritance configuration for I(ddns_use_conflict_resolution) field from I(Server) object."
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
                            type: bool
                            returned: Always
                dhcp_config:
                    description:
                        - "The inheritance configuration for I(dhcp_config) field from I(Server) object."
                    type: dict
                    returned: Always
                    contains:
                        abandoned_reclaim_time:
                            description:
                                - "The inheritance configuration for I(abandoned_reclaim_time) field from I(DHCPConfig) object."
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
                        abandoned_reclaim_time_v6:
                            description:
                                - "The inheritance configuration for I(abandoned_reclaim_time_v6) field from I(DHCPConfig) object."
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
                        allow_unknown:
                            description:
                                - "The inheritance configuration for I(allow_unknown) field from I(DHCPConfig) object."
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
                                    type: bool
                                    returned: Always
                        allow_unknown_v6:
                            description:
                                - "The inheritance configuration for I(allow_unknown_v6) field from I(DHCPConfig) object."
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
                                    type: bool
                                    returned: Always
                        echo_client_id:
                            description:
                                - "The inheritance configuration for I(echo_client_id) field from I(DHCPConfig) object."
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
                                    type: bool
                                    returned: Always
                        filters:
                            description:
                                - "The inheritance configuration for filters field from I(DHCPConfig) object."
                            type: dict
                            returned: Always
                            contains:
                                action:
                                    description:
                                        - "The inheritance setting."
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
                                        - "The resource identifier."
                                    type: list
                                    returned: Always
                        filters_v6:
                            description:
                                - "The inheritance configuration for I(filters_v6) field from I(DHCPConfig) object."
                            type: dict
                            returned: Always
                            contains:
                                action:
                                    description:
                                        - "The inheritance setting."
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
                                        - "The resource identifier."
                                    type: list
                                    returned: Always
                        ignore_client_uid:
                            description:
                                - "The inheritance configuration for I(ignore_client_uid) field from I(DHCPConfig) object."
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
                                    type: bool
                                    returned: Always
                        ignore_list:
                            description:
                                - "The inheritance configuration for I(ignore_list) field from I(DHCPConfig) object."
                            type: dict
                            returned: Always
                            contains:
                                action:
                                    description:
                                        - "The inheritance setting."
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
                                    type: list
                                    returned: Always
                                    elements: dict
                                    contains:
                                        type:
                                            description:
                                                - "Type of ignore matching: client to ignore by client identifier (client hex or client text) or hardware to ignore by hardware identifier (MAC address). It can have one of the following values:"
                                                - "* I(client_hex),"
                                                - "* I(client_text),"
                                                - "* I(hardware)."
                                            type: str
                                            returned: Always
                                        value:
                                            description:
                                                - "Value to match."
                                            type: str
                                            returned: Always
                        lease_time:
                            description:
                                - "The inheritance configuration for I(lease_time) field from I(DHCPConfig) object."
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
                        lease_time_v6:
                            description:
                                - "The inheritance configuration for I(lease_time_v6) field from I(DHCPConfig) object."
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
                dhcp_options:
                    description:
                        - "The inheritance configuration for I(dhcp_options) field from I(Server) object."
                    type: dict
                    returned: Always
                    contains:
                        action:
                            description:
                                - "The inheritance setting."
                                - "Valid values are:"
                                - "* I(inherit): Use the inherited value."
                                - "* I(block): Don't use the inherited value."
                                - "Defaults to I(inherit)."
                            type: str
                            returned: Always
                        value:
                            description:
                                - "The inherited DHCP option values."
                            type: list
                            returned: Always
                            elements: dict
                            contains:
                                action:
                                    description:
                                        - "The inheritance setting."
                                        - "Valid values are:"
                                        - "* I(inherit): Use the inherited value."
                                        - "* I(block): Don't use the inherited value."
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
                                        - "The inherited value for the DHCP option."
                                    type: dict
                                    returned: Always
                                    contains:
                                        option:
                                            description:
                                                - "Option inherited from the ancestor."
                                            type: dict
                                            returned: Always
                                            contains:
                                                group:
                                                    description:
                                                        - "The resource identifier."
                                                    type: str
                                                    returned: Always
                                                option_code:
                                                    description:
                                                        - "The resource identifier."
                                                    type: str
                                                    returned: Always
                                                option_value:
                                                    description:
                                                        - "The option value."
                                                    type: str
                                                    returned: Always
                                                type:
                                                    description:
                                                        - "The type of item."
                                                        - "Valid values are:"
                                                        - "* I(group)"
                                                        - "* I(option)"
                                                    type: str
                                                    returned: Always
                                        overriding_group:
                                            description:
                                                - "The resource identifier."
                                            type: str
                                            returned: Always
                dhcp_options_v6:
                    description:
                        - "The inheritance configuration for I(dhcp_options_v6) field from I(Server) object."
                    type: dict
                    returned: Always
                    contains:
                        action:
                            description:
                                - "The inheritance setting."
                                - "Valid values are:"
                                - "* I(inherit): Use the inherited value."
                                - "* I(block): Don't use the inherited value."
                                - "Defaults to I(inherit)."
                            type: str
                            returned: Always
                        value:
                            description:
                                - "The inherited DHCP option values."
                            type: list
                            returned: Always
                            elements: dict
                            contains:
                                action:
                                    description:
                                        - "The inheritance setting."
                                        - "Valid values are:"
                                        - "* I(inherit): Use the inherited value."
                                        - "* I(block): Don't use the inherited value."
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
                                        - "The inherited value for the DHCP option."
                                    type: dict
                                    returned: Always
                                    contains:
                                        option:
                                            description:
                                                - "Option inherited from the ancestor."
                                            type: dict
                                            returned: Always
                                            contains:
                                                group:
                                                    description:
                                                        - "The resource identifier."
                                                    type: str
                                                    returned: Always
                                                option_code:
                                                    description:
                                                        - "The resource identifier."
                                                    type: str
                                                    returned: Always
                                                option_value:
                                                    description:
                                                        - "The option value."
                                                    type: str
                                                    returned: Always
                                                type:
                                                    description:
                                                        - "The type of item."
                                                        - "Valid values are:"
                                                        - "* I(group)"
                                                        - "* I(option)"
                                                    type: str
                                                    returned: Always
                                        overriding_group:
                                            description:
                                                - "The resource identifier."
                                            type: str
                                            returned: Always
                header_option_filename:
                    description:
                        - "The inheritance configuration for I(header_option_filename) field."
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
                            type: str
                            returned: Always
                header_option_server_address:
                    description:
                        - "The inheritance configuration for I(header_option_server_address) field."
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
                            type: str
                            returned: Always
                header_option_server_name:
                    description:
                        - "The inheritance configuration for I(header_option_server_name) field."
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
                            type: str
                            returned: Always
                hostname_rewrite_block:
                    description:
                        - "The inheritance configuration for I(hostname_rewrite_enabled), I(hostname_rewrite_regex), I(hostname_rewrite_char) fields from I(Server) object."
                    type: dict
                    returned: Always
                    contains:
                        action:
                            description:
                                - "The inheritance setting."
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
                            type: dict
                            returned: Always
                            contains:
                                hostname_rewrite_char:
                                    description:
                                        - "The inheritance configuration for I(hostname_rewrite_char) field."
                                    type: str
                                    returned: Always
                                hostname_rewrite_enabled:
                                    description:
                                        - "The inheritance configuration for I(hostname_rewrite_enabled) field."
                                    type: bool
                                    returned: Always
                                hostname_rewrite_regex:
                                    description:
                                        - "The inheritance configuration for I(hostname_rewrite_regex) field."
                                    type: str
                                    returned: Always
                vendor_specific_option_option_space:
                    description:
                        - "The inheritance configuration for I(vendor_specific_option_option_space) field from I(Server) object."
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
                                - "The resource identifier."
                            type: str
                            returned: Always
        kerberos_kdc:
            description:
                - "Address of Kerberos Key Distribution Center."
                - "Defaults to empty."
            type: str
            returned: Always
        kerberos_keys:
            description:
                - "I(kerberos_keys) contains a list of keys for GSS-TSIG signed dynamic updates."
                - "Defaults to empty."
            type: list
            returned: Always
            elements: dict
            contains:
                algorithm:
                    description:
                        - "Encryption algorithm of the key in accordance with RFC 3961."
                    type: str
                    returned: Always
                domain:
                    description:
                        - "Kerberos realm of the principal."
                    type: str
                    returned: Always
                key:
                    description:
                        - "The resource identifier."
                    type: str
                    returned: Always
                principal:
                    description:
                        - "Kerberos principal associated with key."
                    type: str
                    returned: Always
                uploaded_at:
                    description:
                        - "Upload time for the key."
                    type: str
                    returned: Always
                version:
                    description:
                        - "The version number (KVNO) of the key."
                    type: int
                    returned: Always
        kerberos_rekey_interval:
            description:
                - "Time interval (in seconds) the keys for each configured external DNS server are checked for rekeying, i.e. a new key is created to replace the current usable one when its age is greater than the I(kerberos_rekey_interval) value."
                - "Defaults to 120 seconds."
            type: int
            returned: Always
        kerberos_retry_interval:
            description:
                - "Time interval (in seconds) to retry to create a key if any error occurred previously for any configured external DNS server."
                - "Defaults to 30 seconds."
            type: int
            returned: Always
        kerberos_tkey_lifetime:
            description:
                - "Lifetime (in seconds) of GSS-TSIG keys in the TKEY protocol."
                - "Defaults to 160 seconds."
            type: int
            returned: Always
        kerberos_tkey_protocol:
            description:
                - "Determines which protocol is used to establish the security context with the external DNS servers, TCP or UDP."
                - "Defaults to I(tcp)."
            type: str
            returned: Always
        name:
            description:
                - "The name of the DHCP Config Profile. Must contain 1 to 256 characters. Can include UTF-8."
            type: str
            returned: Always
        profile_type:
            description:
                - "The type of server object."
                - "Defaults to I(server)."
                - "Valid values are:"
                - "* I(server): The server profile type."
                - "* I(subnet): The subnet profile type."
            type: str
            returned: Always
        server_principal:
            description:
                - "The Kerberos principal name of the external DNS server that will receive updates."
                - "Defaults to empty."
            type: str
            returned: Always
        tags:
            description:
                - "The tags for the DHCP Config Profile in JSON format."
            type: dict
            returned: Always
        updated_at:
            description:
                - "Time when the object has been updated. Equals to I(created_at) if not updated after creation."
            type: str
            returned: Always
        vendor_specific_option_option_space:
            description:
                - "The resource identifier."
            type: str
            returned: Always
"""  # noqa: E501

from ansible_collections.infoblox.universal_ddi.plugins.module_utils.modules import UniversalDDIAnsibleModule

try:
    from ipam import ServerApi
    from universal_ddi_client import ApiException, NotFoundException
except ImportError:
    pass  # Handled by UniversalDDIAnsibleModule


class DHCPServerInfoModule(UniversalDDIAnsibleModule):
    def __init__(self, *args, **kwargs):
        super(DHCPServerInfoModule, self).__init__(*args, **kwargs)
        self._existing = None
        self._limit = 1000

    def find_by_id(self):
        try:
            resp = ServerApi(self.client).read(self.params["id"], inherit="full")
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

        tag_filter_str = None
        if self.params["tag_filters"] is not None:
            tag_filter_str = " and ".join([f"{k}=='{v}'" for k, v in self.params["tag_filters"].items()])
        elif self.params["tag_filter_query"] is not None:
            tag_filter_str = self.params["tag_filter_query"]

        all_results = []
        offset = 0

        while True:
            try:
                resp = ServerApi(self.client).list(
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

    module = DHCPServerInfoModule(
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
