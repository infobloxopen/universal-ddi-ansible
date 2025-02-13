# Migration Guide: Bloxone Ansible to Universal DDI Ansible

## Contents

- [Introduction](#introduction)
- [Overview of Changes](#overview-of-changes)
- [Renaming and Module Reorganization](#renaming-and-module-reorganization)
- [New Modules](#new-modules)
- [Enhancement and New Features](#enhancement-and-new-features)
- [Example Migrations](#example-migrations)
    - [IPAM Subnet](#ipam-subnet)
    - [IPAM Address Block](#ipam-address-block)
    - [IPAM Next Available Address Block](#ipam-next-available-address-block)
    - [IPAM Next Available Subnet](#ipam-next-available-subnet)
    - [IPAM Next Available IP](#ipam-next-available-ip)
    - [IPAM Address](#ipam-address)
    - [DNS Auth Zone](#dns-auth-zone)
    - [DNS Record](#dns-record)
- [Support](#support)

## Introduction

This document provides a comprehensive guide for transitioning from the Bloxone Ansible modules to the new Universal DDI Ansible modules. It highlights deprecated features, introduces new and enhanced modules, and provides detailed migration examples to facilitate a smooth transition.

### Background on Repository Changes
Originally, all development was done through the [Bloxone Ansible](https://github.com/infobloxopen/bloxone-ansible) repository, with updates and new modules introduced in the v2 branch. This branch also marked the beginning of the deprecation phase for older modules, signaling upcoming changes and the need for users to transition to newer modules.

### Now Transitioning
With the launch of the [Universal DDI Ansible](https://github.com/infobloxopen/universal-ddi-ansible) repository, which exclusively contains new and improved modules, we have ceased updates to the [Bloxone Ansible](https://github.com/infobloxopen/bloxone-ansible) v2 branch modules. This new repository simplifies module management and ensures users have access to the most advanced features with continued support.

### Detailed Migration Steps
In the following sections of this guide, detailed steps are provided for migrating modules. This includes comparisons of configurations, parameter changes, and the enhanced functionalities offered by the Universal DDI Ansible modules.

## Overview of Changes

- **Renaming:** The collection has transitioned from `b1ddi_modules` to `universal_ddi`, reflecting broader support and functionality.
- **Module Reorganization:** The modules are renamed to follow the Universal DDI naming conventions. The old module names are deprecated and will be removed in the next major release.
- **Dependency Updates:** The modules are rewritten to use the [Universal DDI Python](https://github.com/infobloxopen/universal-ddi-python-client) client library. This provides a more consistent experience across the modules and supports a wider range of BloxOne services.

## Renaming and Module Reorganization

 Modules have been renamed and reorganized to align with standard naming conventions. Here is a table with old and new names for quick reference

| Bloxone Ansible                 | Universal DDI Ansible   |
|---------------------------------|-------------------------|
| b1_dns_auth_zone                | dns_auth_zone           |
| b1_dns_zone_gather              | dns_auth_zone_info      |
| b1_dns_view                     | dns_view                |
| b1_dns_view_gather              | dns_view_info           |
| b1_ipam_ip_space                | ipam_ip_space           |
| b1_ipam_ip_space_gather         | ipam_ip_space_info      |
| b1_ipam_ip_subnet               | ipam_subnet             |
| b1_ipam_ip_subnet_gather        | ipam_subnet_info        |
| b1_ipam_ip_address_block        | ipam_address_block      |
| b1_ipam_ip_address_block_gather | ipam_address_block_info |
| b1_ipam_host                    | ipam_host               |
| b1_ipam_host_gather             | ipam_host_info          |
| b1_ipam_ipv4_reservation        | ipam_address            |
| b1_ipam_ipv4_reservation_gather | ipam_address_info       |
 
> **_NOTE:_** A single module dns_record is now capable of handling all types of DNS records

| Bloxone Ansible        | Universal DDI Ansible |
|------------------------|-----------------------|
| b1_a_record            | dns_record            |
| b1_cname_record        | dns_record            |
| b1_ns_record           | dns_record            |
| b1_ptr_record          | dns_record            |
| b1_a_record_gather     | dns_record_info       |
| b1_cname_record_gather | dns_record_info       |
| b1_ns_record_gather    | dns_record_info       |
| b1_ptr_record_gather   | dns_record_info       |

## New Modules

Several new features and modules have been added to enhance functionality and provide more comprehensive management capabilities across networking services:

#### DNS Management
  - `dns_forward_zone`
  - `dns_forward_zone_info`
  - `dns_delegation`
  - `dns_delegation_info`
  - `dns_auth_nsg`
  - `dns_auth_nsg_info`
  - `dns_forward_nsg`
  - `dns_forward_nsg_info`
  - `dns_server`
  - `dns_server_info`
  - `dns_host`
  - `dns_host_info`
  - `dns_acl`
  - `dns_acl_info`

#### IPAM Management
  - `ipam_range`
  - `ipam_range_info`
  - `ipam_next_available_address_block_info`
  - `ipam_next_available_subnet_info`
  - `ipam_next_available_ip_info`

#### Infrastructure Management
  - `infra_host`
  - `infra_host_info`
  - `infra_service`
  - `infra_service_info`
  - `infra_join_token`
  - `infra_join_token_info`

#### Keys Management
  - `tsig_key`
  - `tsig_key_info`
  - `kerberos_key_info`

## Enhancement and New Features

### Added Return Section in Documentation

Documentation has been significantly improved to include a **Return** section detailing the data types and values returned by module executions.

### Simplified Configuration with Module Defaults

In Bloxone Ansible, every example required explicit declaration of api_key and host under the task parameters to establish connectivity and authentication details for operations. Here's how parameters were defined

```
vars:   
  - host: "{{ Host server to connect to }}"
  - api: "{{ api key to access the server }}"

  tasks:
    #  Create a given IP space
    - name: Create IP space
      b1_ipam_ip_space:
        name: "qa-space-1"
        tags:
          - "Org": "Infoblox"
          - "Dept": "QA"
        comment: "This is a test IPSpace to validate Infoblox Ansible Collection"
        host: "{{ host }}"
        api: "{{ api }}"
        state: present
   ```

However, in Universal DDI Ansible, we have streamlined this setup by introducing `module_defaults`. This enhancement allows portal_key and portal_url to be set once for all modules in a block, eliminating redundancy and simplifying the configuration for all tasks within the block. This provides a cleaner, more maintainable setup

```
- module_defaults:
    group/infoblox.universal_ddi.all:
      portal_url: "{{ portal_url }}"
      portal_key: "{{ portal_key }}"
  block:
    # Create a random IP space name to avoid conflicts
    - Ansible.builtin.set_fact:
        name: "test-ip-space-{{ 999999 | random | string }}"
    - name: "Create an IP space"
    infoblox.universal_ddi.ipam_ip_space:
      name: "{{ name }}"
      state: "present"
    register: ip_space
```

###  Module States

In the update from Bloxone Ansible to Universal DDI Ansible , there's been a simplification of the options available for the state parameter, which is used to define the desired state of the resource being managed by the playbook.

#### Bloxone Ansible State Options:
In .py files
- `present` : Ensures that the resource exists.
- `absent` : Ensures that the resource does not exist.
- `get` : Retrieves the resource details without making any changes.

In _gather.py files
- `present` : Ensures that the resource exists.
- `absent` : Ensures that the resource does not exist.
- `gather` : Retrieves the resource details without making any changes.

#### Universal DDI Ansible State Options:

- `present`: Ensures that the resource exists.
- `absent`: Ensures that the resource does not exist.

> **_NOTE:_**  The new `_info.py` files do not use a state parameter because they are designed solely for retrieval purposes

### Check Mode Support

One of the significant enhancements in Universal DDI Ansible is the addition of support for **Check Mode**. This feature allows users to run playbooks in a dry-run mode, enabling them to review the potential changes and effects without making any actual modifications to the target environment.

#### Example Usage
``` 
- name: "Create an IP space (check mode)"
  infoblox.universal_ddi.ipam_ip_space:
    name: "{{ name }}"
    state: "present"
  check_mode: true
```
## Example Migrations

### IPAM Subnet

#### Creation in Bloxone Ansible
In Bloxone Ansible, when creating a subnet, you directly specify the IP Space name as a string:

```
- name: Create IP space
  b1_ipam_ip_space:
    name: "qa-space-1"
    host: "{{ host }}"
    api_key: "{{ api }}"
    state: present

- name: Create Subnet in a given IP Space
  b1_ipam_subnet:
    space: "qa-space-1"
    address: "40.0.0.0/25"
    name: "qa-test-Subnet1"
    host: "{{ host }}"
    api_key: "{{ api }}"
    state: present
```

#### Creation in Universal DDI Ansible
Universal DDI Ansible uses the IP Space id, which is a more precise and programmatically robust method of referencing the IP space when creating a subnet:

```
- name: "Create an IP space"
  infoblox.universal_ddi.ipam_ip_space:
      name: "{{ ip_space_name }}"
      state: "present"
  register: ip_space

- name: "Create a subnet"
  infoblox.universal_ddi.ipam_subnet:
    address: "10.0.0.0/24"
    space: "{{ ip_space.id }}"
    state: "present"
```

### IPAM Address Block

In Bloxone Ansible, IP Spaces were directly referenced by their names where as in Universal DDI Ansible it is referenced by id

#### Creation in Bloxone Ansible
```
- name: Create IP space
  b1_ipam_ip_space:
    name: "qa-space-1"
    host: "{{ host }}"
    api_key: "{{ api }}"
    state: present

- name: Create Address Block in a given IP Space
  b1_ipam_address_block:
    space: "qa-space-1"
    address: "40.0.0.0/24"
    name: "qa-block-1"
    comment: "This is created by QA"
    tags:
      - "Org": "Infoblox"
      - "Dept": "Engineering"
    api_key: "{{ api }}"
    host: "{{ host }}"
    state: present
```

#### Creation in Universal DDI Ansible
```
- name: "Create an IP space (required as parent)"
  infoblox.universal_ddi.ipam_ip_space:
    name: "my-ip-space"
    state: "present"
    register: ip_space

- name: "Create an address block"
  infoblox.universal_ddi.ipam_address_block:
    address: "10.0.0.0/16"
    space: "{{ ip_space.id }}"
    state: "present"
    register: address_block
```

### IPAM Next Available Address Block

#### Creation in Bloxone Ansible : 

The implementation for creating a next available address block was accomplished by specifying a complex structured input within the address field

```
- name: Create IP space
  b1_ipam_ip_space:
    name: "qa-space-1"
    host: "{{ host }}"
    api_key: "{{ api }}"
    state: present

- name: Create Address Block in a given IP Space
  b1_ipam_address_block:
    space: "qa-space-1"
    address: "40.0.0.0/24"
    name: "qa-block-1"
    host: "{{ host }}"
    api_key: "{{ api }}"
    state: present
        
- name: Create Address Block using next-available subnet
  b1_ipam_address_block:
    space: "qa-space-1"
    address: '{"next_available_address_block": {"cidr": "28", "count": "5", "parent_block": "40.0.0.0/24"}}'
    name: "qa-nextAvailable"
    comment: "Created by QA using nextavailable"
    host: "{{ host }}"
    api_key: "{{ api }}"
    state: present
```

#### Creation in Universal DDI Ansible

Universal DDI Ansible simplifies this process significantly, allowing for a more intuitive declaration of next available options directly

```
- name: "Create an IP space (required as parent)"
  infoblox.universal_ddi.ipam_ip_space:
    name: "my-ip-space"
    state: "present"
    register: ip_space

- name: "Create an address block"
  infoblox.universal_ddi.ipam_address_block:
    address: "10.0.0.0/16"
    space: "{{ ip_space.id }}"
    state: "present"
    register: address_block

- name: "Create Next Available Address Block"
  infoblox.universal_ddi.ipam_address_block:
    space: "{{ ip_space.id }}"
    cidr: 20
    next_available_id: "{{ address_block.id }}"
    state: "present"
```

### IPAM Next Available Subnet

#### Creation in Bloxone Ansible

The implementation for creating a next available subnet was accomplished by specifying a complex structured input within the address field

```
- name: Create IP space
  b1_ipam_ip_space:
    name: "qa-space-1"
    host: "{{ host }}"
    api_key: "{{ api }}"
    state: present

- name: Create Address Block using next-available subnet
  b1_ipam_subnet:
    space: "qa-space-1"
    address: '{"next_available_subnet": {"cidr": "28", "count": "2", "parent_block": "40.0.0.0/24"}}'
    name: "qa-test-nextAvailable"
    comment: "This is the test subnet creation using nextavailable"
    api_key: "{{ api }}"
    host: "{{ host }}"
    state: present
```

#### Creation in Universal DDI Ansible

Universal DDI Ansible simplifies this process significantly, allowing for a more intuitive declaration of next available options directly

```
- name: "Create an IP Space (required as parent)"
  infoblox.universal_ddi.ipam_ip_space:
    name: "example-ipspace"
    state: "present"
  register: ip_space

- name: "Create an Address Block (required as parent)"
  infoblox.universal_ddi.ipam_address_block:
    address: "10.0.0.0/16"
    space: "{{ ip_space.id }}"
    state: "present"
  register: address_block

- name: "Create a subnet"
  infoblox.universal_ddi.ipam_subnet:
    address: "10.0.0.0/24"
    space: "{{ ip_space.id }}"
    state: "present"

- name: "Create a Next available Subnet"
  infoblox.universal_ddi.ipam_subnet:
    cidr: 24
    next_available_id: "{{ address_block.id }}"
    space: "{{ ip_space.id }}"
    state: "present"

```

### IPAM Next Available IP

#### Creation in Bloxone Ansible

The implementation for creating a next available address in a subnet was accomplished by specifying a complex structured input within the address field

```
- name: Create IPv4 address reservation
  b1_ipam_ipv4_reservation:
    address: "{{ IP_address }}"
    space: "{{ IP_space }}"
    name: "{{ reservation_name }}"
    tags:
      - {{ key }}: "{{ value }}"
    comment: "{{ comment }}"
    api_key: "{{ api_token }}"
    host: "{{ host_server }}"
    state: present

- name: Create IPv4 address reservation using next available IP functionality
  b1_ipam_ipv4_reservation:
    address: '{"next_available_ip": {"parent": "<subnet>"}}'
    space: "{{ IP_space }}"
    name: "{{ reservation_name }}"
    tags:
      - {{ key }}: "{{ value }}"
    comment: "{{ comment }}"
    api_key: "{{ api_token }}"
    host: "{{ host_server }}"
    state: present

```

#### Creation in Universal DDI Ansible

Universal DDI Ansible simplifies this process significantly, allowing for a more intuitive declaration of next available options directly


```
- name: "Create an IP Space (required as parent)"
  infoblox.universal_ddi.ipam_ip_space:
    name: "example-ipspace"
    state: "present"
  register: ip_space

- name: "Create a Subnet (required as parent)"
  infoblox.universal_ddi.ipam_subnet:
    address: "10.0.0.0/16"
    space: "{{ ip_space.id }}"
    state: "present"
  register: subnet

- name: Create an Address
  infoblox.universal_ddi.ipam_address:
    address: "10.0.0.3"
    space: "{{ ip_space.id }}"
    state: "present"

- name: Create a Next Available Address in subnet
  infoblox.universal_ddi.ipam_address:
    space: "{{ _ip_space.id }}"
    next_available_id: "{{ subnet.id }}"
    state: "present"
```


### IPAM Address

#### Creation in Bloxone Ansible

Previously it was referred as an IPv4 reservation

```
- name: Create IP space
  b1_ipam_ip_space:
    name: "qa-space-1"
    host: "{{ host }}"
    api_key: "{{ api }}"
    state: present

- name: Create ipv4 reserved address in a given IP Space
  b1_ipam_ipv4_reservation:
    space: "qa-space-1"
    address: "40.0.0.100"
    name: "qa-res-1"
    comment: "This is reserved by QA"
    tags:
      - "Org": "Infoblox"
    api_key: "{{ api }}"
    host: "{{ host }}"
    state: present
```
#### Creation in Universal DDI Ansible

 Here the setup involves creating an IP space and a subnet as prerequisites, after which you can create the address

```
- name: "Create an IP Space (required as parent)"
  infoblox.universal_ddi.ipam_ip_space:
    name: "example-ipspace"
    state: "present"
  register: ip_space

- name: "Create a Subnet (required as parent)"
  infoblox.universal_ddi.ipam_subnet:
    address: "10.0.0.0/16"
    space: "{{ ip_space.id }}"
    state: "present"
  register: subnet

- name: Create an Address
  infoblox.universal_ddi.ipam_address:
    address: "10.0.0.3"
    space: "{{ ip_space.id }}"
    state: "present"
```

### DNS Auth Zone

#### Creation in Bloxone Ansible
In Bloxone Ansible, view is directly referenced by its name where as in Universal DDI Ansible it is referenced by id

```
- name: Create DNS View
  b1_dns_view:
    name: "qa-view-1"
    tags:
      - "org": "Infoblox"
      - "dept": "QA"
    comment: "This is  created by QA"
    api_key: "{{ api }}"
    host: "{{ host }}"
    state: present

- name: Create DNS Authoritative Zone
  b1_dns_auth_zone:
    fqdn: "qa-zone-1"
    view: "qa-view-1"
    primary_type: "cloud"
    internal_secondaries: 
      - "ZTP_NIOS_TEST_4_14_8888544975683345166"
    tags:
      - Name: "QA"
    comment: "This zone is created by QA"
    api_key: "{{ api }}"
    host: "{{ host }}"
    state: present
```

#### Creation in Universal DDI

```
- name: Create a View (required as parent)
  infoblox.universal_ddi.dns_view:
    name: "dns-view"
    state: present
  register: view

- name: Create an Auth Zone
  infoblox.universal_ddi.dns_auth_zone:
    fqdn: "auth-zone"
    primary_type: external
    view: "{{ view.id }}"
  state: present
```

### DNS Record

#### Creation in Bloxone Ansible:
In Bloxone Ansible, managing different types of DNS records required the use of multiple distinct modules. Each record type such as A, CNAME, NS, and PTR had its specialized module. Here's how records were created in Bloxone Ansible:

```
- name: CREATE A Record
  b1_a_record:
    api_key: "{{ portal_key }}"
    host: "{{ host }}"
    zone: "{{ Zone_name }}"
    address: "{{ ip address of A Record }}"
    name: "{{ domain name of A Record }}"
    state: present
```

```
- name: CREATE CNAME Record
  b1_cname_record:
    api_key: "{{ portal_key }}"
    host: "{{ host }}"
    zone: "{{ Zone_name }}"
    can_name: "{{ Canonical name of CNAME record }}"
    name: "{{ Alias of Cname }}"
    state: present
```

```
- name: Create PTR record
  b1_ptr_record:
    api_key: "{{ portal_key }}"
    host: "{{ host }}"
    zone: "{{ Zone_name }}"
    address: "{{ address of PTR record }}"
    name: "{{ domain name of PTR record }"
    state: present
```

```
- name: Create NS
b1_ns_record:
  api_key: "{{ portal_key }}"
  host: "{{ host }}"
  zone: "{{ Zone_name }}"
  ns_server: "{{ Name server of NS record }}"
  name: "amit-test"
  state: present
```

This approach resulted in a large number of modules that essentially performed similar tasks but were tailored to specific DNS record types.

> **_NOTE:_**  In Universal DDI Ansible, support for additional records like AAAA, CAA, DNAME, Generic, MX, NAPTR, SRV, SVCB and TXT is also added

#### Creation in Universal DDI Ansible:

Universal DDI Ansible introduces a significant simplification. A single module, infoblox.universal_ddi.dns_record, is now capable of handling all types of DNS records.The module uses a generic structure with a type field and a flexible rdata dictionary to accommodate data specific to each record type.

```
- name: Create an A Record in the Auth Zone
  infoblox.universal_ddi.dns_record:
    zone: "{{ _auth_zone.id }}"
    rdata:
        address: "192.168.10.10"
    type: "A"
    state: "present"       

- name: Create an AAAA Record in an Auth Zone
  infoblox.universal_ddi.dns_record:
    zone: "{{ _auth_zone.id }}"
    rdata:
        address: "2001:0db8:85a3:0000:0000:8a2e:0370:7334"
    type: "AAAA"
    state: "present"

- name: Create a CAA Record in an Auth Zone
  infoblox.universal_ddi.dns_record:
    zone: "{{ _auth_zone.id }}"
    rdata:
      tag: "issue"
      value: "ca.example.com"
    type: "CAA"
    state: "present"

- name: Create a CNAME Record in an Auth Zone
  infoblox.universal_ddi.dns_record:
    zone: "{{ _auth_zone.id }}"
    name_in_zone: "example_cname_record"
    rdata:
      cname: "example.com"
    type: "CNAME"
    state: "present"

- name: Create a DNAME Record in an Auth Zone
  infoblox.universal_ddi.dns_record:
    zone: "{{ _auth_zone.id }}"
    rdata:
      target: "google.com."
    type: "DNAME"
    state: "present"

- name: Create a Generic Record in an Auth Zone (e.g, TYPE256)
  infoblox.universal_ddi.dns_record:
    zone: "{{ _auth_zone.id }}"
    rdata:
      subfields:
        - type: "PRESENTATION"
          value: "10 1 \"https://example.com\""
    type: "TYPE256"
    state: "present"

- name: Create a MX Record in an Auth Zone
  infoblox.universal_ddi.dns_record:
    zone: "{{ _auth_zone.id }}"
    rdata:
      preference: 10
      exchange: "mail.example.com."
    type: "MX"
    state: "present"
    
- name: Create a NAPTR Record in an Auth Zone
  infoblox.universal_ddi.dns_record:
    zone: "{{ _auth_zone.id }}"
    rdata:
      order: 100
      preference: 10
      replacement: "."
      services: "SIP+D2U"     
    type: "NAPTR"
    state: "present"
    
- name: Create a NS Record in an Auth Zone
  infoblox.universal_ddi.dns_record:
    zone: "{{ _auth_zone.id }}"
    name_in_zone: "example_ns_record"
    rdata:
      dname: "ns.example.com."
    type: "NS"
    state: "present"

- name: Create a PTR Record in an Auth Zone
  infoblox.universal_ddi.dns_record:
    zone: "{{ rmz.id }}" 
    name_in_zone: "1.0.0" # Note: 10.in-addr.arpa is the reverse mapping zone 
    rdata:
      dname: "ptr.example.com."
    type: "PTR"
    state: "present"

- name: Create a SRV Record in an Auth Zone
  infoblox.universal_ddi.dns_record:
    zone: "{{ _auth_zone.id }}"
    rdata:
      priority: 10
      port: 5060
      target: "srv.example.com."
    type: "SRV"
    state: "present"
    
- name: Create a SVCB Record in an Auth Zone
  infoblox.universal_ddi.dns_record:
    zone: "{{ _auth_zone.id }}"
    rdata:
        target_name: "svc.example.com."
    type: "SVCB"
    state: "present"

- name: Create a TXT Record in an Auth Zone
  infoblox.universal_ddi.dns_record:
    zone: "{{ _auth_zone.id }}"
    rdata:
      text: "sample text"
    type: "TXT"
    state: "present"         
```

## Support

If you have any questions or issues, you can reach out to us using the following channels:

- Github Issues:
  - Submit your issues or requests for enhancements on the [Github Issues Page](https://github.com/infobloxopen/universal-ddi-ansible/issues)
- Infoblox Support:
  - For any questions or issues, please contact [Infoblox Support](https://info.infoblox.com/contact-form/).

## Related Information

- Official Infoblox [Documentation](https://docs.infoblox.com/)
- Infoblox API [Documentation](https://csp.infoblox.com/apidoc)

