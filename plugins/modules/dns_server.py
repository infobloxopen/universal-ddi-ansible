#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: Infoblox Inc.
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: dns_server
short_description: Manages a DNS Config Profile (Server).
description:
    - Manage a DNS Config Profile
    - A Server (DNS Config Profile) is a named configuration profile that can be shared for specified list of hosts.
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
    add_edns_option_in_outgoing_query:
        description:
            - "I(add_edns_option_in_outgoing_query) adds client IP, MAC address and view name into outgoing recursive query. Defaults to I(false)."
        type: bool
    auto_sort_views:
        description:
            - "Optional. Controls manual/automatic views ordering."
            - "Defaults to I(true)."
        type: bool
    comment:
        description:
            - "Optional. Comment for configuration."
        type: str
    custom_root_ns:
        description:
            - "Optional. List of custom root nameservers. The order does not matter."
            - "Error if empty while I(custom_root_ns_enabled) is I(true). Error if there are duplicate items in the list."
            - "Defaults to empty."
        type: list
        elements: dict
        suboptions:
            address:
                description:
                    - "IPv4 address."
                type: str
            fqdn:
                description:
                    - "FQDN."
                type: str
    custom_root_ns_enabled:
        description:
            - "Optional. I(true) to use custom root nameservers instead of the default ones."
            - "The I(custom_root_ns) is validated when enabled."
            - "Defaults to I(false)."
        type: bool
    dnssec_enable_validation:
        description:
            - "Optional. I(true) to perform DNSSEC validation. Ignored if I(dnssec_enabled) is I(false)."
            - "Defaults to I(true)."
        type: bool
    dnssec_enabled:
        description:
            - "Optional. Master toggle for all DNSSEC processing. Other I(dnssec)*_ configuration is unused if this is disabled."
            - "Defaults to I(true)."
        type: bool
    dnssec_trust_anchors:
        description:
            - "Optional. DNSSEC trust anchors."
            - "Error if there are list items with duplicate (I(zone), I(sep), I(algorithm)) combinations."
            - "Defaults to empty."
        type: list
        elements: dict
        suboptions:
            algorithm:
                description:
                    - "DNSSEC trust anchor."
                    - "Key algorithm. Algorithm values are as per standards. The mapping is as follows:"
                    - "* I(RSAMD5) = 1,"
                    - "* I(DH) = 2,"
                    - "* I(DSA) = 3,"
                    - "* I(RSASHA1) = 5,"
                    - "* I(DSANSEC3SHA1) = 6,"
                    - "* I(RSASHA1NSEC3SHA1) = 7,"
                    - "* I(RSASHA256) = 8,"
                    - "* I(RSASHA512) = 10,"
                    - "* I(ECDSAP256SHA256) = 13,"
                    - "* I(ECDSAP384SHA384) = 14."
                    - "Below algorithms are deprecated and not supported anymore:"
                    - "* I(RSAMD5) = 1,"
                    - "* I(DSA) = 3,"
                    - "* I(DSANSEC3SHA1) = 6."
                type: int
            public_key:
                description:
                    - "DNSSEC key data. Non-empty, valid base64 string."
                type: str
            sep:
                description:
                    - "Optional. Secure Entry Point flag."
                    - "Defaults to I(true)."
                type: bool
            zone:
                description:
                    - "Zone FQDN."
                type: str
    dnssec_validate_expiry:
        description:
            - "Optional. I(true) to reject expired DNSSEC keys. Ignored if either I(dnssec_enabled) or I(dnssec_enable_validation) is I(false)."
            - "Defaults to I(true)."
        type: bool
    ecs_enabled:
        description:
            - "Optional. I(true) to enable EDNS client subnet for recursive queries. Other I(ecs)*_ fields are ignored if this field is not enabled."
            - "Defaults to I(false)."
        type: bool
    ecs_forwarding:
        description:
            - "Optional. I(true) to enable ECS options in outbound queries. This functionality has additional overhead so it is disabled by default."
            - "Defaults to I(false)."
        type: bool
    ecs_prefix_v4:
        description:
            - "Optional. Maximum scope length for v4 ECS."
            - "Unsigned integer, min 1 max 24"
            - "Defaults to 24."
        type: int
    ecs_prefix_v6:
        description:
            - "Optional. Maximum scope length for v6 ECS."
            - "Unsigned integer, min 1 max 56"
            - "Defaults to 56."
        type: int
    ecs_zones:
        description:
            - "Optional. List of zones where ECS queries may be sent."
            - "Error if empty while I(ecs_enabled) is I(true). Error if there are duplicate FQDNs in the list."
            - "Defaults to empty."
        type: list
        elements: dict
        suboptions:
            access:
                description:
                    - "Access control for zone."
                    - "Allowed values:"
                    - "* I(allow),"
                    - "* I(deny)."
                type: str
            fqdn:
                description:
                    - "Zone FQDN."
                type: str
    filter_aaaa_acl:
        description:
            - "Optional. Specifies a list of client addresses for which AAAA filtering is to be applied."
            - "Defaults to I(empty)."
        type: list
        elements: dict
        suboptions:
            access:
                description:
                    - "Access permission for I(element)."
                    - "Allowed values:"
                    - "* I(allow),"
                    - "* I(deny)."
                type: str
            acl:
                description:
                    - "The resource identifier."
                type: str
            address:
                description:
                    - "Optional. Data for I(ip) I(element)."
                    - "Must be empty if I(element) is not I(ip)."
                type: str
            element:
                description:
                    - "Type of element."
                    - "Allowed values:"
                    - "* I(any),"
                    - "* I(ip),"
                    - "* I(acl),"
                    - "* I(tsig_key)."
                type: str
            tsig_key:
                description:
                    - "Optional. TSIG key."
                    - "Must be empty if I(element) is not I(tsig_key)."
                type: dict
                suboptions:
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
    filter_aaaa_on_v4:
        description:
            - "I(filter_aaaa_on_v4) allows named to omit some IPv6 addresses when responding to IPv4 clients."
            - "Allowed values:"
            - "* I(yes),"
            - "* I(no),"
            - "* I(break_dnssec)."
            - "Defaults to I(no)"
        type: str
    forwarders:
        description:
            - "Optional. List of forwarders."
            - "Error if empty while I(forwarders_only) or I(use_root_forwarders_for_local_resolution_with_b1td) is I(true). Error if there are items in the list with duplicate addresses."
            - "Defaults to empty."
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
    forwarders_only:
        description:
            - "Optional. I(true) to only forward."
            - "Defaults to I(false)."
        type: bool
    gss_tsig_enabled:
        description:
            - "I(gss_tsig_enabled) enables/disables GSS-TSIG signed dynamic updates."
            - "Defaults to I(false)."
        type: bool
    inheritance_sources:
        description:
            - "Optional. Inheritance configuration."
        type: dict
        suboptions:
            add_edns_option_in_outgoing_query:
                description:
                    - "Field config for I(add_edns_option_in_outgoing_query) field from I(Server) object."
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
            custom_root_ns_block:
                description:
                    - "Optional. Field config for I(custom_root_ns_block) field from I(Server) object."
                type: dict
                suboptions:
                    action:
                        description:
                            - "Defaults to I(inherit)."
                        type: str
            dnssec_validation_block:
                description:
                    - "Optional. Field config for I(dnssec_validation_block) field from I(Server) object."
                type: dict
                suboptions:
                    action:
                        description:
                            - "Defaults to I(inherit)."
                        type: str
            ecs_block:
                description:
                    - "Optional. Field config for I(ecs_block) field from I(Server) object."
                type: dict
                suboptions:
                    action:
                        description:
                            - "Defaults to I(inherit)."
                        type: str
            filter_aaaa_acl:
                description:
                    - "Optional. Field config for I(filter_aaaa_acl) field from I(Server) object."
                type: dict
                suboptions:
                    action:
                        description:
                            - "Optional. Inheritance setting for a field. Defaults to I(inherit)."
                        type: str
            filter_aaaa_on_v4:
                description:
                    - "Optional. Field config for I(filter_aaaa_on_v4) field from I(Server) object."
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
            forwarders_block:
                description:
                    - "Optional. Field config for I(forwarders_block) field from I(Server) object."
                type: dict
                suboptions:
                    action:
                        description:
                            - "Defaults to I(inherit)."
                        type: str
            gss_tsig_enabled:
                description:
                    - "Optional. Field config for I(gss_tsig_enabled) field from I(Server) object."
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
            kerberos_keys:
                description:
                    - "Optional. Field config for I(kerberos_keys) field from I(Server) object."
                type: dict
                suboptions:
                    action:
                        description:
                            - "Optional. Inheritance setting for a field. Defaults to I(inherit)."
                        type: str
            lame_ttl:
                description:
                    - "Optional. Field config for I(lame_ttl) field from I(Server) object."
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
            log_query_response:
                description:
                    - "Optional. Field config for I(log_queries_response) field from I(Server) object."
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
            match_recursive_only:
                description:
                    - "Optional. Field config for I(match_recursive_only) field from I(Server) object."
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
            max_cache_ttl:
                description:
                    - "Optional. Field config for I(max_cache_ttl) field from I(Server) object."
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
            max_negative_ttl:
                description:
                    - "Optional. Field config for I(max_negative_ttl) field from I(Server) object."
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
            minimal_responses:
                description:
                    - "Optional. Field config for I(minimal_responses) field from I(Server) object."
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
            notify:
                description:
                    - "Field config for I(notify) field from I(Server) object."
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
            query_acl:
                description:
                    - "Optional. Field config for I(query_acl) field from I(Server) object."
                type: dict
                suboptions:
                    action:
                        description:
                            - "Optional. Inheritance setting for a field. Defaults to I(inherit)."
                        type: str
            query_port:
                description:
                    - "Optional. Field config for I(query_port) field from I(Server) object."
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
            recursion_acl:
                description:
                    - "Optional. Field config for I(recursion_acl) field from I(Server) object."
                type: dict
                suboptions:
                    action:
                        description:
                            - "Optional. Inheritance setting for a field. Defaults to I(inherit)."
                        type: str
            recursion_enabled:
                description:
                    - "Optional. Field config for I(recursion_enabled) field from I(Server) object."
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
            recursive_clients:
                description:
                    - "Optional. Field config for I(recursive_clients) field from I(Server) object."
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
            resolver_query_timeout:
                description:
                    - "Optional. Field config for I(resolver_query_timeout) field from I(Server) object."
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
            secondary_axfr_query_limit:
                description:
                    - "Optional. Field config for I(secondary_axfr_query_limit) field from I(Server) object."
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
            secondary_soa_query_limit:
                description:
                    - "Optional. Field config for I(secondary_soa_query_limit) field from I(Server) object."
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
            sort_list:
                description:
                    - "Optional. Field config for I(sort_list) field from _Server object."
                type: dict
                suboptions:
                    action:
                        description:
                            - "Optional. Inheritance setting for a field. Defaults to I(inherit)."
                        type: str
            synthesize_address_records_from_https:
                description:
                    - "Field config for I(synthesize_address_records_from_https) field from I(Server) object."
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
            transfer_acl:
                description:
                    - "Optional. Field config for I(transfer_acl) field from I(Server) object."
                type: dict
                suboptions:
                    action:
                        description:
                            - "Optional. Inheritance setting for a field. Defaults to I(inherit)."
                        type: str
            update_acl:
                description:
                    - "Optional. Field config for I(update_acl) field from I(Server) object."
                type: dict
                suboptions:
                    action:
                        description:
                            - "Optional. Inheritance setting for a field. Defaults to I(inherit)."
                        type: str
            use_forwarders_for_subzones:
                description:
                    - "Optional. Field config for I(use_forwarders_for_subzones) field from I(Server) object."
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
    kerberos_keys:
        description:
            - "I(kerberos_keys) contains a list of keys for GSS-TSIG signed dynamic updates."
            - "Defaults to empty."
        type: list
        elements: dict
        suboptions:
            key:
                description:
                    - "The resource identifier."
                type: str
    lame_ttl:
        description:
            - "Optional. Unused in the current on-prem DNS server implementation."
            - "Unsigned integer, min 0 max 3600 (1h)."
            - "Defaults to 600."
        type: int
    log_query_response:
        description:
            - "Optional. Control DNS query/response logging functionality."
            - "Defaults to I(true)."
        type: bool
    match_recursive_only:
        description:
            - "Optional. If I(true) only recursive queries from matching clients access the view."
            - "Defaults to I(false)."
        type: bool
    max_cache_ttl:
        description:
            - "Optional. Seconds to cache positive responses."
            - "Unsigned integer, min 1 max 604800 (7d)."
            - "Defaults to 604800 (7d)."
        type: int
    max_negative_ttl:
        description:
            - "Optional. Seconds to cache negative responses."
            - "Unsigned integer, min 1 max 604800 (7d)."
            - "Defaults to 10800 (3h)."
        type: int
    minimal_responses:
        description:
            - "Optional. When enabled, the DNS server will only add records to the authority and additional data sections when they are required."
            - "Defaults to I(false)."
        type: bool
    name:
        description:
            - "Name of configuration."
        type: str
    notify:
        description:
            - "I(notify) all external secondary DNS servers."
            - "Defaults to I(false)."
        type: bool
    query_acl:
        description:
            - "Optional. Clients must match this ACL to make authoritative queries. Also used for recursive queries if that ACL is unset."
            - "Defaults to empty."
        type: list
        elements: dict
        suboptions:
            access:
                description:
                    - "Access permission for I(element)."
                    - "Allowed values:"
                    - "* I(allow),"
                    - "* I(deny)."
                type: str
            acl:
                description:
                    - "The resource identifier."
                type: str
            address:
                description:
                    - "Optional. Data for I(ip) I(element)."
                    - "Must be empty if I(element) is not I(ip)."
                type: str
            element:
                description:
                    - "Type of element."
                    - "Allowed values:"
                    - "* I(any),"
                    - "* I(ip),"
                    - "* I(acl),"
                    - "* I(tsig_key)."
                type: str
            tsig_key:
                description:
                    - "Optional. TSIG key."
                    - "Must be empty if I(element) is not I(tsig_key)."
                type: dict
                suboptions:
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
    query_port:
        description:
            - "Optional. Source port for outbound DNS queries. When set to 0 the port is unspecified and the implementation may randomize it using any available ports."
            - "Defaults to 0."
        type: int
    recursion_acl:
        description:
            - "Optional. Clients must match this ACL to make recursive queries. If this ACL is empty, then the I(query_acl) field will be used instead."
            - "Defaults to empty."
        type: list
        elements: dict
        suboptions:
            access:
                description:
                    - "Access permission for I(element)."
                    - "Allowed values:"
                    - "* I(allow),"
                    - "* I(deny)."
                type: str
            acl:
                description:
                    - "The resource identifier."
                type: str
            address:
                description:
                    - "Optional. Data for I(ip) I(element)."
                    - "Must be empty if I(element) is not I(ip)."
                type: str
            element:
                description:
                    - "Type of element."
                    - "Allowed values:"
                    - "* I(any),"
                    - "* I(ip),"
                    - "* I(acl),"
                    - "* I(tsig_key)."
                type: str
            tsig_key:
                description:
                    - "Optional. TSIG key."
                    - "Must be empty if I(element) is not I(tsig_key)."
                type: dict
                suboptions:
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
    recursion_enabled:
        description:
            - "Optional. I(true) to allow recursive DNS queries."
            - "Defaults to I(true)."
        type: bool
    recursive_clients:
        description:
            - "Optional. Defines the number of simultaneous recursive lookups the server will perform on behalf of its clients."
            - "Defaults to 1000."
        type: int
    resolver_query_timeout:
        description:
            - "Optional. Seconds before a recursive query times out."
            - "Unsigned integer, min 10 max 30."
            - "Defaults to 10."
        type: int
    secondary_axfr_query_limit:
        description:
            - "Optional. Maximum concurrent inbound AXFRs. When set to 0 a host-dependent default will be used."
            - "Defaults to 0."
        type: int
    secondary_soa_query_limit:
        description:
            - "Optional. Maximum concurrent outbound SOA queries. When set to 0 a host-dependent default will be used."
            - "Defaults to 0."
        type: int
    sort_list:
        description:
            - "Optional. Specifies a sorted network list for A/AAAA records in DNS query response."
            - "Defaults to I(empty)."
        type: list
        elements: dict
        suboptions:
            acl:
                description:
                    - "The resource identifier."
                type: str
            element:
                description:
                    - "Type of element."
                    - "Allowed values:"
                    - "* I(any),"
                    - "* I(ip),"
                    - "* I(acl),"
                type: str
            prioritized_networks:
                description:
                    - "Optional. The prioritized networks. If empty, the value of I(source) or networks from I(acl) is used."
                type: list
                elements: str
            source:
                description:
                    - "Must be empty if I(element) is not I(ip)."
                type: str
    synthesize_address_records_from_https:
        description:
            - "I(synthesize_address_records_from_https) enables/disables creation of A/AAAA records from HTTPS RR Defaults to I(false)."
        type: bool
    tags:
        description:
            - "Tagging specifics."
        type: dict
    transfer_acl:
        description:
            - "Optional. Clients must match this ACL to receive zone transfers."
            - "Defaults to empty."
        type: list
        elements: dict
        suboptions:
            access:
                description:
                    - "Access permission for I(element)."
                    - "Allowed values:"
                    - "* I(allow),"
                    - "* I(deny)."
                type: str
            acl:
                description:
                    - "The resource identifier."
                type: str
            address:
                description:
                    - "Optional. Data for I(ip) I(element)."
                    - "Must be empty if I(element) is not I(ip)."
                type: str
            element:
                description:
                    - "Type of element."
                    - "Allowed values:"
                    - "* I(any),"
                    - "* I(ip),"
                    - "* I(acl),"
                    - "* I(tsig_key)."
                type: str
            tsig_key:
                description:
                    - "Optional. TSIG key."
                    - "Must be empty if I(element) is not I(tsig_key)."
                type: dict
                suboptions:
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
    update_acl:
        description:
            - "Optional. Specifies which hosts are allowed to issue Dynamic DNS updates for authoritative zones of I(primary_type) I(cloud)."
            - "Defaults to empty."
        type: list
        elements: dict
        suboptions:
            access:
                description:
                    - "Access permission for I(element)."
                    - "Allowed values:"
                    - "* I(allow),"
                    - "* I(deny)."
                type: str
            acl:
                description:
                    - "The resource identifier."
                type: str
            address:
                description:
                    - "Optional. Data for I(ip) I(element)."
                    - "Must be empty if I(element) is not I(ip)."
                type: str
            element:
                description:
                    - "Type of element."
                    - "Allowed values:"
                    - "* I(any),"
                    - "* I(ip),"
                    - "* I(acl),"
                    - "* I(tsig_key)."
                type: str
            tsig_key:
                description:
                    - "Optional. TSIG key."
                    - "Must be empty if I(element) is not I(tsig_key)."
                type: dict
                suboptions:
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
    use_forwarders_for_subzones:
        description:
            - "Optional. Use default forwarders to resolve queries for subzones."
            - "Defaults to I(true)."
        type: bool
    use_root_forwarders_for_local_resolution_with_b1td:
        description:
            - "I(use_root_forwarders_for_local_resolution_with_b1td) allows DNS recursive queries sent to root forwarders for local resolution when deployed alongside BloxOne Thread Defense. Defaults to I(false)."
        type: bool
    views:
        description:
            - "Optional. Ordered list of I(dns/display_view) objects served by any of I(dns/host) assigned to a particular DNS Config Profile. Automatically determined. Allows re-ordering only."
        type: list
        elements: dict
        suboptions:
            view:
                description:
                    - "The resource identifier."
                type: str

extends_documentation_fragment:
    - infoblox.universal_ddi.common
"""  # noqa: E501

EXAMPLES = r"""
  - name: Create a DNS Server
    infoblox.universal_ddi.dns_server:
      name: "example_server"
      state: "present"

  - name: Create a DNS Server with Additional Fields
    infoblox.universal_ddi.dns_server:
      name: "example_server"
      recursion_enabled: true
      forwarders:
        - address: "192.168.11.11"
          fqdn: "example.com."
      tags:
        location: "site-1"
      comment: "Example DNS Server"
      state: "present"

  - name: Delete the DNS Server
    infoblox.universal_ddi.dns_server:
      name: "example_server"
      state: "absent"
"""


RETURN = r"""
id:
    description:
        - ID of the Server object
    type: str
    returned: Always
item:
    description:
        - Server object
    type: complex
    returned: Always
    contains:
        add_edns_option_in_outgoing_query:
            description:
                - "I(add_edns_option_in_outgoing_query) adds client IP, MAC address and view name into outgoing recursive query. Defaults to I(false)."
            type: bool
            returned: Always
        auto_sort_views:
            description:
                - "Optional. Controls manual/automatic views ordering."
                - "Defaults to I(true)."
            type: bool
            returned: Always
        comment:
            description:
                - "Optional. Comment for configuration."
            type: str
            returned: Always
        created_at:
            description:
                - "Time when the object has been created."
            type: str
            returned: Always
        custom_root_ns:
            description:
                - "Optional. List of custom root nameservers. The order does not matter."
                - "Error if empty while I(custom_root_ns_enabled) is I(true). Error if there are duplicate items in the list."
                - "Defaults to empty."
            type: list
            returned: Always
            elements: dict
            contains:
                address:
                    description:
                        - "IPv4 address."
                    type: str
                    returned: Always
                fqdn:
                    description:
                        - "FQDN."
                    type: str
                    returned: Always
                protocol_fqdn:
                    description:
                        - "FQDN in punycode."
                    type: str
                    returned: Always
        custom_root_ns_enabled:
            description:
                - "Optional. I(true) to use custom root nameservers instead of the default ones."
                - "The I(custom_root_ns) is validated when enabled."
                - "Defaults to I(false)."
            type: bool
            returned: Always
        dnssec_enable_validation:
            description:
                - "Optional. I(true) to perform DNSSEC validation. Ignored if I(dnssec_enabled) is I(false)."
                - "Defaults to I(true)."
            type: bool
            returned: Always
        dnssec_enabled:
            description:
                - "Optional. Master toggle for all DNSSEC processing. Other I(dnssec)*_ configuration is unused if this is disabled."
                - "Defaults to I(true)."
            type: bool
            returned: Always
        dnssec_root_keys:
            description:
                - "DNSSEC root keys. The root keys are not configurable."
                - "A default list is provided by cloud management and included here for config generation."
            type: list
            returned: Always
            elements: dict
            contains:
                algorithm:
                    description:
                        - "Specifies the cryptographic algorithm used for DNSSEC. Supported values and their corresponding mappings are as follows."
                        - "RSAMD5 (1)"
                        - "DH (2)"
                        - "DSA (3)"
                        - "RSASHA1 (5)"
                        - "DSANSEC3SHA1 (6)"
                        - "RSASHA1NSEC3SHA1 (7)"
                        - "RSASHA256 (8)"
                        - "RSASHA512 (10)"
                        - "ECDSAP256SHA256 (13)"
                        - "ECDSAP384SHA384 (14)"
                        - "**Deprecated Algorithms:**"
                        - "RSAMD5 (1)"
                        - "DSA (3)"
                        - "DSANSEC3SHA1 (6)"
                    type: int
                    returned: Always
                protocol_zone:
                    description:
                        - "Zone FQDN in punycode."
                    type: str
                    returned: Always
                public_key:
                    description:
                        - "DNSSEC key data. Non-empty, valid base64 string."
                    type: str
                    returned: Always
                sep:
                    description:
                        - "Optional. Secure Entry Point flag."
                        - "Defaults to I(true)."
                    type: bool
                    returned: Always
                zone:
                    description:
                        - "Zone FQDN."
                    type: str
                    returned: Always
        dnssec_trust_anchors:
            description:
                - "Optional. DNSSEC trust anchors."
                - "Error if there are list items with duplicate (I(zone), I(sep), I(algorithm)) combinations."
                - "Defaults to empty."
            type: list
            returned: Always
            elements: dict
            contains:
                algorithm:
                    description: 
                        - "Specifies the cryptographic algorithm used for DNSSEC. Supported values and their corresponding mappings are as follows."
                        - "RSAMD5 (1)"
                        - "DH (2)"
                        - "DSA (3)"
                        - "RSASHA1 (5)"
                        - "DSANSEC3SHA1 (6)"
                        - "RSASHA1NSEC3SHA1 (7)"
                        - "RSASHA256 (8)"
                        - "RSASHA512 (10)"
                        - "ECDSAP256SHA256 (13)"
                        - "ECDSAP384SHA384 (14)"
                        - "**Deprecated Algorithms:**"
                        - "RSAMD5 (1)"
                        - "DSA (3)"
                        - "DSANSEC3SHA1 (6)"
                    type: int
                    returned: Always
                protocol_zone:
                    description:
                        - "Zone FQDN in punycode."
                    type: str
                    returned: Always
                public_key:
                    description:
                        - "DNSSEC key data. Non-empty, valid base64 string."
                    type: str
                    returned: Always
                sep:
                    description:
                        - "Optional. Secure Entry Point flag."
                        - "Defaults to I(true)."
                    type: bool
                    returned: Always
                zone:
                    description:
                        - "Zone FQDN."
                    type: str
                    returned: Always
        dnssec_validate_expiry:
            description:
                - "Optional. I(true) to reject expired DNSSEC keys. Ignored if either I(dnssec_enabled) or I(dnssec_enable_validation) is I(false)."
                - "Defaults to I(true)."
            type: bool
            returned: Always
        ecs_enabled:
            description:
                - "Optional. I(true) to enable EDNS client subnet for recursive queries. Other I(ecs)*_ fields are ignored if this field is not enabled."
                - "Defaults to I(false)."
            type: bool
            returned: Always
        ecs_forwarding:
            description:
                - "Optional. I(true) to enable ECS options in outbound queries. This functionality has additional overhead so it is disabled by default."
                - "Defaults to I(false)."
            type: bool
            returned: Always
        ecs_prefix_v4:
            description:
                - "Optional. Maximum scope length for v4 ECS."
                - "Unsigned integer, min 1 max 24"
                - "Defaults to 24."
            type: int
            returned: Always
        ecs_prefix_v6:
            description:
                - "Optional. Maximum scope length for v6 ECS."
                - "Unsigned integer, min 1 max 56"
                - "Defaults to 56."
            type: int
            returned: Always
        ecs_zones:
            description:
                - "Optional. List of zones where ECS queries may be sent."
                - "Error if empty while I(ecs_enabled) is I(true). Error if there are duplicate FQDNs in the list."
                - "Defaults to empty."
            type: list
            returned: Always
            elements: dict
            contains:
                access:
                    description:
                        - "Access control for zone."
                        - "Allowed values:"
                        - "* I(allow),"
                        - "* I(deny)."
                    type: str
                    returned: Always
                fqdn:
                    description:
                        - "Zone FQDN."
                    type: str
                    returned: Always
                protocol_fqdn:
                    description:
                        - "Zone FQDN in punycode."
                    type: str
                    returned: Always
        filter_aaaa_acl:
            description:
                - "Optional. Specifies a list of client addresses for which AAAA filtering is to be applied."
                - "Defaults to I(empty)."
            type: list
            returned: Always
            elements: dict
            contains:
                access:
                    description:
                        - "Access permission for I(element)."
                        - "Allowed values:"
                        - "* I(allow),"
                        - "* I(deny)."
                    type: str
                    returned: Always
                acl:
                    description:
                        - "The resource identifier."
                    type: str
                    returned: Always
                address:
                    description:
                        - "Optional. Data for I(ip) I(element)."
                        - "Must be empty if I(element) is not I(ip)."
                    type: str
                    returned: Always
                element:
                    description:
                        - "Type of element."
                        - "Allowed values:"
                        - "* I(any),"
                        - "* I(ip),"
                        - "* I(acl),"
                        - "* I(tsig_key)."
                    type: str
                    returned: Always
                tsig_key:
                    description:
                        - "Optional. TSIG key."
                        - "Must be empty if I(element) is not I(tsig_key)."
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
        filter_aaaa_on_v4:
            description:
                - "I(filter_aaaa_on_v4) allows named to omit some IPv6 addresses when responding to IPv4 clients."
                - "Allowed values:"
                - "* I(yes),"
                - "* I(no),"
                - "* I(break_dnssec)."
                - "Defaults to I(no)"
            type: str
            returned: Always
        forwarders:
            description:
                - "Optional. List of forwarders."
                - "Error if empty while I(forwarders_only) or I(use_root_forwarders_for_local_resolution_with_b1td) is I(true). Error if there are items in the list with duplicate addresses."
                - "Defaults to empty."
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
        forwarders_only:
            description:
                - "Optional. I(true) to only forward."
                - "Defaults to I(false)."
            type: bool
            returned: Always
        gss_tsig_enabled:
            description:
                - "I(gss_tsig_enabled) enables/disables GSS-TSIG signed dynamic updates."
                - "Defaults to I(false)."
            type: bool
            returned: Always
        id:
            description:
                - "The resource identifier."
            type: str
            returned: Always
        inheritance_sources:
            description:
                - "Optional. Inheritance configuration."
            type: dict
            returned: Always
            contains:
                add_edns_option_in_outgoing_query:
                    description:
                        - "Field config for I(add_edns_option_in_outgoing_query) field from I(Server) object."
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
                custom_root_ns_block:
                    description:
                        - "Optional. Field config for I(custom_root_ns_block) field from I(Server) object."
                    type: dict
                    returned: Always
                    contains:
                        action:
                            description:
                                - "Defaults to I(inherit)."
                            type: str
                            returned: Always
                        display_name:
                            description:
                                - "Human-readable display name for the object referred to by I(source)."
                            type: str
                            returned: Always
                        source:
                            description:
                                - "The resource identifier."
                            type: str
                            returned: Always
                        value:
                            description:
                                - "Inherited value."
                            type: dict
                            returned: Always
                            contains:
                                custom_root_ns:
                                    description:
                                        - "Optional. Field config for I(custom_root_ns) field."
                                    type: list
                                    returned: Always
                                    elements: dict
                                    contains:
                                        address:
                                            description:
                                                - "IPv4 address."
                                            type: str
                                            returned: Always
                                        fqdn:
                                            description:
                                                - "FQDN."
                                            type: str
                                            returned: Always
                                        protocol_fqdn:
                                            description:
                                                - "FQDN in punycode."
                                            type: str
                                            returned: Always
                                custom_root_ns_enabled:
                                    description:
                                        - "Optional. Field config for I(custom_root_ns_enabled) field."
                                    type: bool
                                    returned: Always
                dnssec_validation_block:
                    description:
                        - "Optional. Field config for I(dnssec_validation_block) field from I(Server) object."
                    type: dict
                    returned: Always
                    contains:
                        action:
                            description:
                                - "Defaults to I(inherit)."
                            type: str
                            returned: Always
                        display_name:
                            description:
                                - "Human-readable display name for the object referred to by I(source)."
                            type: str
                            returned: Always
                        source:
                            description:
                                - "The resource identifier."
                            type: str
                            returned: Always
                        value:
                            description:
                                - "Inherited value."
                            type: dict
                            returned: Always
                            contains:
                                dnssec_enable_validation:
                                    description:
                                        - "Optional. Field config for I(dnssec_enable_validation) field."
                                    type: bool
                                    returned: Always
                                dnssec_enabled:
                                    description:
                                        - "Optional. Field config for I(dnssec_enabled) field."
                                    type: bool
                                    returned: Always
                                dnssec_trust_anchors:
                                    description:
                                        - "Optional. Field config for I(dnssec_trust_anchors) field."
                                    type: list
                                    returned: Always
                                    elements: dict
                                    contains:
                                        algorithm:
                                            description: 
                                                - "Specifies the cryptographic algorithm used for DNSSEC. Supported values and their corresponding mappings are as follows."
                                                - "RSAMD5 (1)"
                                                - "DH (2)"
                                                - "DSA (3)"
                                                - "RSASHA1 (5)"
                                                - "DSANSEC3SHA1 (6)"
                                                - "RSASHA1NSEC3SHA1 (7)"
                                                - "RSASHA256 (8)"
                                                - "RSASHA512 (10)"
                                                - "ECDSAP256SHA256 (13)"
                                                - "ECDSAP384SHA384 (14)"
                                                - "**Deprecated Algorithms:**"
                                                - "RSAMD5 (1)"
                                                - "DSA (3)"
                                                - "DSANSEC3SHA1 (6)"
                                            type: int
                                            returned: Always
                                        protocol_zone:
                                            description:
                                                - "Zone FQDN in punycode."
                                            type: str
                                            returned: Always
                                        public_key:
                                            description:
                                                - "DNSSEC key data. Non-empty, valid base64 string."
                                            type: str
                                            returned: Always
                                        sep:
                                            description:
                                                - "Optional. Secure Entry Point flag."
                                                - "Defaults to I(true)."
                                            type: bool
                                            returned: Always
                                        zone:
                                            description:
                                                - "Zone FQDN."
                                            type: str
                                            returned: Always
                                dnssec_validate_expiry:
                                    description:
                                        - "Optional. Field config for I(dnssec_validate_expiry) field."
                                    type: bool
                                    returned: Always
                ecs_block:
                    description:
                        - "Optional. Field config for I(ecs_block) field from I(Server) object."
                    type: dict
                    returned: Always
                    contains:
                        action:
                            description:
                                - "Defaults to I(inherit)."
                            type: str
                            returned: Always
                        display_name:
                            description:
                                - "Human-readable display name for the object referred to by I(source)."
                            type: str
                            returned: Always
                        source:
                            description:
                                - "The resource identifier."
                            type: str
                            returned: Always
                        value:
                            description:
                                - "Inherited value."
                            type: dict
                            returned: Always
                            contains:
                                ecs_enabled:
                                    description:
                                        - "Optional. Field config for I(ecs_enabled) field."
                                    type: bool
                                    returned: Always
                                ecs_forwarding:
                                    description:
                                        - "Optional. Field config for I(ecs_forwarding) field."
                                    type: bool
                                    returned: Always
                                ecs_prefix_v4:
                                    description:
                                        - "Optional. Field config for I(ecs_prefix_v4) field."
                                    type: int
                                    returned: Always
                                ecs_prefix_v6:
                                    description:
                                        - "Optional. Field config for I(ecs_prefix_v6) field."
                                    type: int
                                    returned: Always
                                ecs_zones:
                                    description:
                                        - "Optional. Field config for I(ecs_zones) field."
                                    type: list
                                    returned: Always
                                    elements: dict
                                    contains:
                                        access:
                                            description:
                                                - "Access control for zone."
                                                - "Allowed values:"
                                                - "* I(allow),"
                                                - "* I(deny)."
                                            type: str
                                            returned: Always
                                        fqdn:
                                            description:
                                                - "Zone FQDN."
                                            type: str
                                            returned: Always
                                        protocol_fqdn:
                                            description:
                                                - "Zone FQDN in punycode."
                                            type: str
                                            returned: Always
                filter_aaaa_acl:
                    description:
                        - "Optional. Field config for I(filter_aaaa_acl) field from I(Server) object."
                    type: dict
                    returned: Always
                    contains:
                        action:
                            description:
                                - "Optional. Inheritance setting for a field. Defaults to I(inherit)."
                            type: str
                            returned: Always
                        display_name:
                            description:
                                - "Human-readable display name for the object referred to by I(source)."
                            type: str
                            returned: Always
                        source:
                            description:
                                - "The resource identifier."
                            type: str
                            returned: Always
                        value:
                            description:
                                - "Inherited value."
                            type: list
                            returned: Always
                            elements: dict
                            contains:
                                access:
                                    description:
                                        - "Access permission for I(element)."
                                        - "Allowed values:"
                                        - "* I(allow),"
                                        - "* I(deny)."
                                    type: str
                                    returned: Always
                                acl:
                                    description:
                                        - "The resource identifier."
                                    type: str
                                    returned: Always
                                address:
                                    description:
                                        - "Optional. Data for I(ip) I(element)."
                                        - "Must be empty if I(element) is not I(ip)."
                                    type: str
                                    returned: Always
                                element:
                                    description:
                                        - "Type of element."
                                        - "Allowed values:"
                                        - "* I(any),"
                                        - "* I(ip),"
                                        - "* I(acl),"
                                        - "* I(tsig_key)."
                                    type: str
                                    returned: Always
                                tsig_key:
                                    description:
                                        - "Optional. TSIG key."
                                        - "Must be empty if I(element) is not I(tsig_key)."
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
                filter_aaaa_on_v4:
                    description:
                        - "Optional. Field config for I(filter_aaaa_on_v4) field from I(Server) object."
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
                forwarders_block:
                    description:
                        - "Optional. Field config for I(forwarders_block) field from I(Server) object."
                    type: dict
                    returned: Always
                    contains:
                        action:
                            description:
                                - "Defaults to I(inherit)."
                            type: str
                            returned: Always
                        display_name:
                            description:
                                - "Human-readable display name for the object referred to by I(source)."
                            type: str
                            returned: Always
                        source:
                            description:
                                - "The resource identifier."
                            type: str
                            returned: Always
                        value:
                            description:
                                - "Inherited value."
                            type: dict
                            returned: Always
                            contains:
                                forwarders:
                                    description:
                                        - "Optional. Field config for I(forwarders) field from."
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
                                forwarders_only:
                                    description:
                                        - "Optional. Field config for I(forwarders_only) field."
                                    type: bool
                                    returned: Always
                                use_root_forwarders_for_local_resolution_with_b1td:
                                    description:
                                        - "Optional. Field config for I(use_root_forwarders_for_local_resolution_with_b1td) field."
                                    type: bool
                                    returned: Always
                gss_tsig_enabled:
                    description:
                        - "Optional. Field config for I(gss_tsig_enabled) field from I(Server) object."
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
                kerberos_keys:
                    description:
                        - "Optional. Field config for I(kerberos_keys) field from I(Server) object."
                    type: dict
                    returned: Always
                    contains:
                        action:
                            description:
                                - "Optional. Inheritance setting for a field. Defaults to I(inherit)."
                            type: str
                            returned: Always
                        display_name:
                            description:
                                - "Human-readable display name for the object referred to by I(source)."
                            type: str
                            returned: Always
                        source:
                            description:
                                - "The resource identifier."
                            type: str
                            returned: Always
                        value:
                            description:
                                - "Inherited value."
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
                lame_ttl:
                    description:
                        - "Optional. Field config for I(lame_ttl) field from I(Server) object."
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
                log_query_response:
                    description:
                        - "Optional. Field config for I(log_queries_response) field from I(Server) object."
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
                match_recursive_only:
                    description:
                        - "Optional. Field config for I(match_recursive_only) field from I(Server) object."
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
                max_cache_ttl:
                    description:
                        - "Optional. Field config for I(max_cache_ttl) field from I(Server) object."
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
                max_negative_ttl:
                    description:
                        - "Optional. Field config for I(max_negative_ttl) field from I(Server) object."
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
                minimal_responses:
                    description:
                        - "Optional. Field config for I(minimal_responses) field from I(Server) object."
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
                notify:
                    description:
                        - "Field config for I(notify) field from I(Server) object."
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
                query_acl:
                    description:
                        - "Optional. Field config for I(query_acl) field from I(Server) object."
                    type: dict
                    returned: Always
                    contains:
                        action:
                            description:
                                - "Optional. Inheritance setting for a field. Defaults to I(inherit)."
                            type: str
                            returned: Always
                        display_name:
                            description:
                                - "Human-readable display name for the object referred to by I(source)."
                            type: str
                            returned: Always
                        source:
                            description:
                                - "The resource identifier."
                            type: str
                            returned: Always
                        value:
                            description:
                                - "Inherited value."
                            type: list
                            returned: Always
                            elements: dict
                            contains:
                                access:
                                    description:
                                        - "Access permission for I(element)."
                                        - "Allowed values:"
                                        - "* I(allow),"
                                        - "* I(deny)."
                                    type: str
                                    returned: Always
                                acl:
                                    description:
                                        - "The resource identifier."
                                    type: str
                                    returned: Always
                                address:
                                    description:
                                        - "Optional. Data for I(ip) I(element)."
                                        - "Must be empty if I(element) is not I(ip)."
                                    type: str
                                    returned: Always
                                element:
                                    description:
                                        - "Type of element."
                                        - "Allowed values:"
                                        - "* I(any),"
                                        - "* I(ip),"
                                        - "* I(acl),"
                                        - "* I(tsig_key)."
                                    type: str
                                    returned: Always
                                tsig_key:
                                    description:
                                        - "Optional. TSIG key."
                                        - "Must be empty if I(element) is not I(tsig_key)."
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
                query_port:
                    description:
                        - "Optional. Field config for I(query_port) field from I(Server) object."
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
                recursion_acl:
                    description:
                        - "Optional. Field config for I(recursion_acl) field from I(Server) object."
                    type: dict
                    returned: Always
                    contains:
                        action:
                            description:
                                - "Optional. Inheritance setting for a field. Defaults to I(inherit)."
                            type: str
                            returned: Always
                        display_name:
                            description:
                                - "Human-readable display name for the object referred to by I(source)."
                            type: str
                            returned: Always
                        source:
                            description:
                                - "The resource identifier."
                            type: str
                            returned: Always
                        value:
                            description:
                                - "Inherited value."
                            type: list
                            returned: Always
                            elements: dict
                            contains:
                                access:
                                    description:
                                        - "Access permission for I(element)."
                                        - "Allowed values:"
                                        - "* I(allow),"
                                        - "* I(deny)."
                                    type: str
                                    returned: Always
                                acl:
                                    description:
                                        - "The resource identifier."
                                    type: str
                                    returned: Always
                                address:
                                    description:
                                        - "Optional. Data for I(ip) I(element)."
                                        - "Must be empty if I(element) is not I(ip)."
                                    type: str
                                    returned: Always
                                element:
                                    description:
                                        - "Type of element."
                                        - "Allowed values:"
                                        - "* I(any),"
                                        - "* I(ip),"
                                        - "* I(acl),"
                                        - "* I(tsig_key)."
                                    type: str
                                    returned: Always
                                tsig_key:
                                    description:
                                        - "Optional. TSIG key."
                                        - "Must be empty if I(element) is not I(tsig_key)."
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
                recursion_enabled:
                    description:
                        - "Optional. Field config for I(recursion_enabled) field from I(Server) object."
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
                recursive_clients:
                    description:
                        - "Optional. Field config for I(recursive_clients) field from I(Server) object."
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
                resolver_query_timeout:
                    description:
                        - "Optional. Field config for I(resolver_query_timeout) field from I(Server) object."
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
                secondary_axfr_query_limit:
                    description:
                        - "Optional. Field config for I(secondary_axfr_query_limit) field from I(Server) object."
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
                secondary_soa_query_limit:
                    description:
                        - "Optional. Field config for I(secondary_soa_query_limit) field from I(Server) object."
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
                sort_list:
                    description:
                        - "Optional. Field config for I(sort_list) field from _Server object."
                    type: dict
                    returned: Always
                    contains:
                        action:
                            description:
                                - "Optional. Inheritance setting for a field. Defaults to I(inherit)."
                            type: str
                            returned: Always
                        display_name:
                            description:
                                - "Human-readable display name for the object referred to by I(source)."
                            type: str
                            returned: Always
                        source:
                            description:
                                - "The resource identifier."
                            type: str
                            returned: Always
                        value:
                            description:
                                - "Inherited value."
                            type: list
                            returned: Always
                            elements: dict
                            contains:
                                acl:
                                    description:
                                        - "The resource identifier."
                                    type: str
                                    returned: Always
                                element:
                                    description:
                                        - "Type of element."
                                        - "Allowed values:"
                                        - "* I(any),"
                                        - "* I(ip),"
                                        - "* I(acl),"
                                    type: str
                                    returned: Always
                                prioritized_networks:
                                    description:
                                        - "Optional. The prioritized networks. If empty, the value of I(source) or networks from I(acl) is used."
                                    type: list
                                    returned: Always
                                source:
                                    description:
                                        - "Must be empty if I(element) is not I(ip)."
                                    type: str
                                    returned: Always
                synthesize_address_records_from_https:
                    description:
                        - "Field config for I(synthesize_address_records_from_https) field from I(Server) object."
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
                transfer_acl:
                    description:
                        - "Optional. Field config for I(transfer_acl) field from I(Server) object."
                    type: dict
                    returned: Always
                    contains:
                        action:
                            description:
                                - "Optional. Inheritance setting for a field. Defaults to I(inherit)."
                            type: str
                            returned: Always
                        display_name:
                            description:
                                - "Human-readable display name for the object referred to by I(source)."
                            type: str
                            returned: Always
                        source:
                            description:
                                - "The resource identifier."
                            type: str
                            returned: Always
                        value:
                            description:
                                - "Inherited value."
                            type: list
                            returned: Always
                            elements: dict
                            contains:
                                access:
                                    description:
                                        - "Access permission for I(element)."
                                        - "Allowed values:"
                                        - "* I(allow),"
                                        - "* I(deny)."
                                    type: str
                                    returned: Always
                                acl:
                                    description:
                                        - "The resource identifier."
                                    type: str
                                    returned: Always
                                address:
                                    description:
                                        - "Optional. Data for I(ip) I(element)."
                                        - "Must be empty if I(element) is not I(ip)."
                                    type: str
                                    returned: Always
                                element:
                                    description:
                                        - "Type of element."
                                        - "Allowed values:"
                                        - "* I(any),"
                                        - "* I(ip),"
                                        - "* I(acl),"
                                        - "* I(tsig_key)."
                                    type: str
                                    returned: Always
                                tsig_key:
                                    description:
                                        - "Optional. TSIG key."
                                        - "Must be empty if I(element) is not I(tsig_key)."
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
                update_acl:
                    description:
                        - "Optional. Field config for I(update_acl) field from I(Server) object."
                    type: dict
                    returned: Always
                    contains:
                        action:
                            description:
                                - "Optional. Inheritance setting for a field. Defaults to I(inherit)."
                            type: str
                            returned: Always
                        display_name:
                            description:
                                - "Human-readable display name for the object referred to by I(source)."
                            type: str
                            returned: Always
                        source:
                            description:
                                - "The resource identifier."
                            type: str
                            returned: Always
                        value:
                            description:
                                - "Inherited value."
                            type: list
                            returned: Always
                            elements: dict
                            contains:
                                access:
                                    description:
                                        - "Access permission for I(element)."
                                        - "Allowed values:"
                                        - "* I(allow),"
                                        - "* I(deny)."
                                    type: str
                                    returned: Always
                                acl:
                                    description:
                                        - "The resource identifier."
                                    type: str
                                    returned: Always
                                address:
                                    description:
                                        - "Optional. Data for I(ip) I(element)."
                                        - "Must be empty if I(element) is not I(ip)."
                                    type: str
                                    returned: Always
                                element:
                                    description:
                                        - "Type of element."
                                        - "Allowed values:"
                                        - "* I(any),"
                                        - "* I(ip),"
                                        - "* I(acl),"
                                        - "* I(tsig_key)."
                                    type: str
                                    returned: Always
                                tsig_key:
                                    description:
                                        - "Optional. TSIG key."
                                        - "Must be empty if I(element) is not I(tsig_key)."
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
                use_forwarders_for_subzones:
                    description:
                        - "Optional. Field config for I(use_forwarders_for_subzones) field from I(Server) object."
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
        lame_ttl:
            description:
                - "Optional. Unused in the current on-prem DNS server implementation."
                - "Unsigned integer, min 0 max 3600 (1h)."
                - "Defaults to 600."
            type: int
            returned: Always
        log_query_response:
            description:
                - "Optional. Control DNS query/response logging functionality."
                - "Defaults to I(true)."
            type: bool
            returned: Always
        match_recursive_only:
            description:
                - "Optional. If I(true) only recursive queries from matching clients access the view."
                - "Defaults to I(false)."
            type: bool
            returned: Always
        max_cache_ttl:
            description:
                - "Optional. Seconds to cache positive responses."
                - "Unsigned integer, min 1 max 604800 (7d)."
                - "Defaults to 604800 (7d)."
            type: int
            returned: Always
        max_negative_ttl:
            description:
                - "Optional. Seconds to cache negative responses."
                - "Unsigned integer, min 1 max 604800 (7d)."
                - "Defaults to 10800 (3h)."
            type: int
            returned: Always
        minimal_responses:
            description:
                - "Optional. When enabled, the DNS server will only add records to the authority and additional data sections when they are required."
                - "Defaults to I(false)."
            type: bool
            returned: Always
        name:
            description:
                - "Name of configuration."
            type: str
            returned: Always
        notify:
            description:
                - "I(notify) all external secondary DNS servers."
                - "Defaults to I(false)."
            type: bool
            returned: Always
        query_acl:
            description:
                - "Optional. Clients must match this ACL to make authoritative queries. Also used for recursive queries if that ACL is unset."
                - "Defaults to empty."
            type: list
            returned: Always
            elements: dict
            contains:
                access:
                    description:
                        - "Access permission for I(element)."
                        - "Allowed values:"
                        - "* I(allow),"
                        - "* I(deny)."
                    type: str
                    returned: Always
                acl:
                    description:
                        - "The resource identifier."
                    type: str
                    returned: Always
                address:
                    description:
                        - "Optional. Data for I(ip) I(element)."
                        - "Must be empty if I(element) is not I(ip)."
                    type: str
                    returned: Always
                element:
                    description:
                        - "Type of element."
                        - "Allowed values:"
                        - "* I(any),"
                        - "* I(ip),"
                        - "* I(acl),"
                        - "* I(tsig_key)."
                    type: str
                    returned: Always
                tsig_key:
                    description:
                        - "Optional. TSIG key."
                        - "Must be empty if I(element) is not I(tsig_key)."
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
        query_port:
            description:
                - "Optional. Source port for outbound DNS queries. When set to 0 the port is unspecified and the implementation may randomize it using any available ports."
                - "Defaults to 0."
            type: int
            returned: Always
        recursion_acl:
            description:
                - "Optional. Clients must match this ACL to make recursive queries. If this ACL is empty, then the I(query_acl) field will be used instead."
                - "Defaults to empty."
            type: list
            returned: Always
            elements: dict
            contains:
                access:
                    description:
                        - "Access permission for I(element)."
                        - "Allowed values:"
                        - "* I(allow),"
                        - "* I(deny)."
                    type: str
                    returned: Always
                acl:
                    description:
                        - "The resource identifier."
                    type: str
                    returned: Always
                address:
                    description:
                        - "Optional. Data for I(ip) I(element)."
                        - "Must be empty if I(element) is not I(ip)."
                    type: str
                    returned: Always
                element:
                    description:
                        - "Type of element."
                        - "Allowed values:"
                        - "* I(any),"
                        - "* I(ip),"
                        - "* I(acl),"
                        - "* I(tsig_key)."
                    type: str
                    returned: Always
                tsig_key:
                    description:
                        - "Optional. TSIG key."
                        - "Must be empty if I(element) is not I(tsig_key)."
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
        recursion_enabled:
            description:
                - "Optional. I(true) to allow recursive DNS queries."
                - "Defaults to I(true)."
            type: bool
            returned: Always
        recursive_clients:
            description:
                - "Optional. Defines the number of simultaneous recursive lookups the server will perform on behalf of its clients."
                - "Defaults to 1000."
            type: int
            returned: Always
        resolver_query_timeout:
            description:
                - "Optional. Seconds before a recursive query times out."
                - "Unsigned integer, min 10 max 30."
                - "Defaults to 10."
            type: int
            returned: Always
        secondary_axfr_query_limit:
            description:
                - "Optional. Maximum concurrent inbound AXFRs. When set to 0 a host-dependent default will be used."
                - "Defaults to 0."
            type: int
            returned: Always
        secondary_soa_query_limit:
            description:
                - "Optional. Maximum concurrent outbound SOA queries. When set to 0 a host-dependent default will be used."
                - "Defaults to 0."
            type: int
            returned: Always
        sort_list:
            description:
                - "Optional. Specifies a sorted network list for A/AAAA records in DNS query response."
                - "Defaults to I(empty)."
            type: list
            returned: Always
            elements: dict
            contains:
                acl:
                    description:
                        - "The resource identifier."
                    type: str
                    returned: Always
                element:
                    description:
                        - "Type of element."
                        - "Allowed values:"
                        - "* I(any),"
                        - "* I(ip),"
                        - "* I(acl),"
                    type: str
                    returned: Always
                prioritized_networks:
                    description:
                        - "Optional. The prioritized networks. If empty, the value of I(source) or networks from I(acl) is used."
                    type: list
                    returned: Always
                source:
                    description:
                        - "Must be empty if I(element) is not I(ip)."
                    type: str
                    returned: Always
        synthesize_address_records_from_https:
            description:
                - "I(synthesize_address_records_from_https) enables/disables creation of A/AAAA records from HTTPS RR Defaults to I(false)."
            type: bool
            returned: Always
        tags:
            description:
                - "Tagging specifics."
            type: dict
            returned: Always
        transfer_acl:
            description:
                - "Optional. Clients must match this ACL to receive zone transfers."
                - "Defaults to empty."
            type: list
            returned: Always
            elements: dict
            contains:
                access:
                    description:
                        - "Access permission for I(element)."
                        - "Allowed values:"
                        - "* I(allow),"
                        - "* I(deny)."
                    type: str
                    returned: Always
                acl:
                    description:
                        - "The resource identifier."
                    type: str
                    returned: Always
                address:
                    description:
                        - "Optional. Data for I(ip) I(element)."
                        - "Must be empty if I(element) is not I(ip)."
                    type: str
                    returned: Always
                element:
                    description:
                        - "Type of element."
                        - "Allowed values:"
                        - "* I(any),"
                        - "* I(ip),"
                        - "* I(acl),"
                        - "* I(tsig_key)."
                    type: str
                    returned: Always
                tsig_key:
                    description:
                        - "Optional. TSIG key."
                        - "Must be empty if I(element) is not I(tsig_key)."
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
        update_acl:
            description:
                - "Optional. Specifies which hosts are allowed to issue Dynamic DNS updates for authoritative zones of I(primary_type) I(cloud)."
                - "Defaults to empty."
            type: list
            returned: Always
            elements: dict
            contains:
                access:
                    description:
                        - "Access permission for I(element)."
                        - "Allowed values:"
                        - "* I(allow),"
                        - "* I(deny)."
                    type: str
                    returned: Always
                acl:
                    description:
                        - "The resource identifier."
                    type: str
                    returned: Always
                address:
                    description:
                        - "Optional. Data for I(ip) I(element)."
                        - "Must be empty if I(element) is not I(ip)."
                    type: str
                    returned: Always
                element:
                    description:
                        - "Type of element."
                        - "Allowed values:"
                        - "* I(any),"
                        - "* I(ip),"
                        - "* I(acl),"
                        - "* I(tsig_key)."
                    type: str
                    returned: Always
                tsig_key:
                    description:
                        - "Optional. TSIG key."
                        - "Must be empty if I(element) is not I(tsig_key)."
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
        updated_at:
            description:
                - "Time when the object has been updated. Equals to I(created_at) if not updated after creation."
            type: str
            returned: Always
        use_forwarders_for_subzones:
            description:
                - "Optional. Use default forwarders to resolve queries for subzones."
                - "Defaults to I(true)."
            type: bool
            returned: Always
        use_root_forwarders_for_local_resolution_with_b1td:
            description:
                - "I(use_root_forwarders_for_local_resolution_with_b1td) allows DNS recursive queries sent to root forwarders for local resolution when deployed alongside BloxOne Thread Defense. Defaults to I(false)."
            type: bool
            returned: Always
        views:
            description:
                - "Optional. Ordered list of I(dns/display_view) objects served by any of I(dns/host) assigned to a particular DNS Config Profile. Automatically determined. Allows re-ordering only."
            type: list
            returned: Always
            elements: dict
            contains:
                comment:
                    description:
                        - "DNS view description."
                    type: str
                    returned: Always
                name:
                    description:
                        - "DNS view name."
                    type: str
                    returned: Always
                view:
                    description:
                        - "The resource identifier."
                    type: str
                    returned: Always
"""  # noqa: E501

from ansible_collections.infoblox.universal_ddi.plugins.module_utils.modules import UniversalDDIAnsibleModule

try:
    from dns_config import Server, ServerApi
    from universal_ddi_client import ApiException, NotFoundException
except ImportError:
    pass  # Handled by UniversalDDIAnsibleModule


class ServerModule(UniversalDDIAnsibleModule):
    def __init__(self, *args, **kwargs):
        super(ServerModule, self).__init__(*args, **kwargs)

        exclude = ["state", "csp_url", "api_key", "portal_url", "portal_key", "id"]
        self._payload_params = {k: v for k, v in self.params.items() if v is not None and k not in exclude}
        self._payload = Server.from_dict(self._payload_params)
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
                resp = ServerApi(self.client).read(self.params["id"], inherit="full")
                return resp.result
            except NotFoundException as e:
                if self.params["state"] == "absent":
                    return None
                raise e
        else:
            filter = f"name=='{self.params['name']}'"
            resp = ServerApi(self.client).list(filter=filter, inherit="full")
            if len(resp.results) == 1:
                return resp.results[0]
            if len(resp.results) > 1:
                self.fail_json(msg=f"Found multiple Server: {resp.results}")
            if len(resp.results) == 0:
                return None

    def create(self):
        if self.check_mode:
            return None

        resp = ServerApi(self.client).create(body=self.payload, inherit="full")
        return resp.result.model_dump(by_alias=True, exclude_none=True)

    def update(self):
        if self.check_mode:
            return None

        resp = ServerApi(self.client).update(id=self.existing.id, body=self.payload, inherit="full")
        return resp.result.model_dump(by_alias=True, exclude_none=True)

    def delete(self):
        if self.check_mode:
            return

        ServerApi(self.client).delete(self.existing.id)

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
                result["msg"] = "Server created"
            elif self.params["state"] == "present" and self.existing is not None:
                if self.payload_changed():
                    item = self.update()
                    result["changed"] = True
                    result["msg"] = "Server updated"
            elif self.params["state"] == "absent" and self.existing is not None:
                self.delete()
                result["changed"] = True
                result["msg"] = "Server deleted"

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
        add_edns_option_in_outgoing_query=dict(type="bool"),
        auto_sort_views=dict(type="bool"),
        comment=dict(type="str"),
        custom_root_ns=dict(
            type="list",
            elements="dict",
            options=dict(
                address=dict(type="str"),
                fqdn=dict(type="str"),
            ),
        ),
        custom_root_ns_enabled=dict(type="bool"),
        dnssec_enable_validation=dict(type="bool"),
        dnssec_enabled=dict(type="bool"),
        dnssec_trust_anchors=dict(
            type="list",
            elements="dict",
            options=dict(
                algorithm=dict(type="int"),
                public_key=dict(type="str"),
                sep=dict(type="bool"),
                zone=dict(type="str"),
            ),
        ),
        dnssec_validate_expiry=dict(type="bool"),
        ecs_enabled=dict(type="bool"),
        ecs_forwarding=dict(type="bool"),
        ecs_prefix_v4=dict(type="int"),
        ecs_prefix_v6=dict(type="int"),
        ecs_zones=dict(
            type="list",
            elements="dict",
            options=dict(
                access=dict(type="str"),
                fqdn=dict(type="str"),
            ),
        ),
        filter_aaaa_acl=dict(
            type="list",
            elements="dict",
            options=dict(
                access=dict(type="str"),
                acl=dict(type="str"),
                address=dict(type="str"),
                element=dict(type="str"),
                tsig_key=dict(
                    type="dict",
                    no_log=True,
                    options=dict(
                        algorithm=dict(type="str"),
                        comment=dict(type="str"),
                        key=dict(type="str", no_log=True),
                        name=dict(type="str"),
                        secret=dict(type="str", no_log=True),
                    ),
                ),
            ),
        ),
        filter_aaaa_on_v4=dict(type="str"),
        forwarders=dict(
            type="list",
            elements="dict",
            options=dict(
                address=dict(type="str"),
                fqdn=dict(type="str"),
            ),
        ),
        forwarders_only=dict(type="bool"),
        gss_tsig_enabled=dict(type="bool"),
        inheritance_sources=dict(
            type="dict",
            options=dict(
                add_edns_option_in_outgoing_query=dict(
                    type="dict",
                    options=dict(
                        action=dict(type="str"),
                    ),
                ),
                custom_root_ns_block=dict(
                    type="dict",
                    options=dict(
                        action=dict(type="str"),
                    ),
                ),
                dnssec_validation_block=dict(
                    type="dict",
                    options=dict(
                        action=dict(type="str"),
                    ),
                ),
                ecs_block=dict(
                    type="dict",
                    options=dict(
                        action=dict(type="str"),
                    ),
                ),
                filter_aaaa_acl=dict(
                    type="dict",
                    options=dict(
                        action=dict(type="str"),
                    ),
                ),
                filter_aaaa_on_v4=dict(
                    type="dict",
                    options=dict(
                        action=dict(type="str"),
                    ),
                ),
                forwarders_block=dict(
                    type="dict",
                    options=dict(
                        action=dict(type="str"),
                    ),
                ),
                gss_tsig_enabled=dict(
                    type="dict",
                    options=dict(
                        action=dict(type="str"),
                    ),
                ),
                kerberos_keys=dict(
                    type="dict",
                    no_log=True,
                    options=dict(
                        action=dict(type="str"),
                    ),
                ),
                lame_ttl=dict(
                    type="dict",
                    options=dict(
                        action=dict(type="str"),
                    ),
                ),
                log_query_response=dict(
                    type="dict",
                    options=dict(
                        action=dict(type="str"),
                    ),
                ),
                match_recursive_only=dict(
                    type="dict",
                    options=dict(
                        action=dict(type="str"),
                    ),
                ),
                max_cache_ttl=dict(
                    type="dict",
                    options=dict(
                        action=dict(type="str"),
                    ),
                ),
                max_negative_ttl=dict(
                    type="dict",
                    options=dict(
                        action=dict(type="str"),
                    ),
                ),
                minimal_responses=dict(
                    type="dict",
                    options=dict(
                        action=dict(type="str"),
                    ),
                ),
                notify=dict(
                    type="dict",
                    options=dict(
                        action=dict(type="str"),
                    ),
                ),
                query_acl=dict(
                    type="dict",
                    options=dict(
                        action=dict(type="str"),
                    ),
                ),
                query_port=dict(
                    type="dict",
                    options=dict(
                        action=dict(type="str"),
                    ),
                ),
                recursion_acl=dict(
                    type="dict",
                    options=dict(
                        action=dict(type="str"),
                    ),
                ),
                recursion_enabled=dict(
                    type="dict",
                    options=dict(
                        action=dict(type="str"),
                    ),
                ),
                recursive_clients=dict(
                    type="dict",
                    options=dict(
                        action=dict(type="str"),
                    ),
                ),
                resolver_query_timeout=dict(
                    type="dict",
                    options=dict(
                        action=dict(type="str"),
                    ),
                ),
                secondary_axfr_query_limit=dict(
                    type="dict",
                    options=dict(
                        action=dict(type="str"),
                    ),
                ),
                secondary_soa_query_limit=dict(
                    type="dict",
                    options=dict(
                        action=dict(type="str"),
                    ),
                ),
                sort_list=dict(
                    type="dict",
                    options=dict(
                        action=dict(type="str"),
                    ),
                ),
                synthesize_address_records_from_https=dict(
                    type="dict",
                    options=dict(
                        action=dict(type="str"),
                    ),
                ),
                transfer_acl=dict(
                    type="dict",
                    options=dict(
                        action=dict(type="str"),
                    ),
                ),
                update_acl=dict(
                    type="dict",
                    options=dict(
                        action=dict(type="str"),
                    ),
                ),
                use_forwarders_for_subzones=dict(
                    type="dict",
                    options=dict(
                        action=dict(type="str"),
                    ),
                ),
            ),
        ),
        kerberos_keys=dict(
            type="list",
            no_log=True,
            elements="dict",
            options=dict(
                key=dict(type="str", no_log=True),
            ),
        ),
        lame_ttl=dict(type="int"),
        log_query_response=dict(type="bool"),
        match_recursive_only=dict(type="bool"),
        max_cache_ttl=dict(type="int"),
        max_negative_ttl=dict(type="int"),
        minimal_responses=dict(type="bool"),
        name=dict(type="str"),
        notify=dict(type="bool"),
        query_acl=dict(
            type="list",
            elements="dict",
            options=dict(
                access=dict(type="str"),
                acl=dict(type="str"),
                address=dict(type="str"),
                element=dict(type="str"),
                tsig_key=dict(
                    type="dict",
                    no_log=True,
                    options=dict(
                        algorithm=dict(type="str"),
                        comment=dict(type="str"),
                        key=dict(type="str", no_log=True),
                        name=dict(type="str"),
                        secret=dict(type="str", no_log=True),
                    ),
                ),
            ),
        ),
        query_port=dict(type="int"),
        recursion_acl=dict(
            type="list",
            elements="dict",
            options=dict(
                access=dict(type="str"),
                acl=dict(type="str"),
                address=dict(type="str"),
                element=dict(type="str"),
                tsig_key=dict(
                    type="dict",
                    no_log=True,
                    options=dict(
                        algorithm=dict(type="str"),
                        comment=dict(type="str"),
                        key=dict(type="str", no_log=True),
                        name=dict(type="str"),
                        secret=dict(type="str", no_log=True),
                    ),
                ),
            ),
        ),
        recursion_enabled=dict(type="bool"),
        recursive_clients=dict(type="int"),
        resolver_query_timeout=dict(type="int"),
        secondary_axfr_query_limit=dict(type="int"),
        secondary_soa_query_limit=dict(type="int"),
        sort_list=dict(
            type="list",
            elements="dict",
            options=dict(
                acl=dict(type="str"),
                element=dict(type="str"),
                prioritized_networks=dict(type="list", elements="str"),
                source=dict(type="str"),
            ),
        ),
        synthesize_address_records_from_https=dict(type="bool"),
        tags=dict(type="dict"),
        transfer_acl=dict(
            type="list",
            no_log=True,
            elements="dict",
            options=dict(
                access=dict(type="str"),
                acl=dict(type="str"),
                address=dict(type="str"),
                element=dict(type="str"),
                tsig_key=dict(
                    type="dict",
                    no_log=True,
                    options=dict(
                        algorithm=dict(type="str"),
                        comment=dict(type="str"),
                        key=dict(type="str", no_log=True),
                        name=dict(type="str"),
                        secret=dict(type="str", no_log=True),
                    ),
                ),
            ),
        ),
        update_acl=dict(
            type="list",
            elements="dict",
            options=dict(
                access=dict(type="str"),
                acl=dict(type="str"),
                address=dict(type="str"),
                element=dict(type="str"),
                tsig_key=dict(
                    type="dict",
                    no_log=True,
                    options=dict(
                        algorithm=dict(type="str"),
                        comment=dict(type="str"),
                        key=dict(type="str", no_log=True),
                        name=dict(type="str"),
                        secret=dict(type="str", no_log=True),
                    ),
                ),
            ),
        ),
        use_forwarders_for_subzones=dict(type="bool"),
        use_root_forwarders_for_local_resolution_with_b1td=dict(type="bool"),
        views=dict(
            type="list",
            elements="dict",
            options=dict(
                view=dict(type="str"),
            ),
        ),
    )

    module = ServerModule(
        argument_spec=module_args,
        supports_check_mode=True,
        required_if=[("state", "present", ["name"])],
    )

    module.run_command()


if __name__ == "__main__":
    main()
