# Migration Guide: Bloxone Ansible to Universal DDI Ansible 

This document provides a step-by-step guide to assist users in migrating from `Bloxone Ansible` to `Universal DDI Ansible`. It highlights breaking changes, new features, and important modifications to ensure a smooth transition.

## Overview of Changes

- The collection has been renamed from `b1ddi_modules` to `universal_ddi`.
- The modules are renamed to follow the Universal DDI naming conventions. The old module names are deprecated and will be removed in the next major release.
- The modules are rewritten to use the [Universal DDI Python client](https://github.com/infobloxopen/universal-ddi-python-client) library. This provides a more consistent experience across the modules and supports a wider range of BloxOne services.

### Module Renaming
Some modules have been renamed for consistency:

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

#### A single module dns_record is now capable of handling all types of DNS records

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

### New Modules Added

- `dns_auth_nsg`
- `dns_auth_nsg_info`
- `dns_forward_nsg`
- `dns_forward_nsg_info`
- `dns_forward_zone`
- `dns_forward_zone_info`
- `dns_delegation`
- `dns_delegation_info`
- `dns_host`
- `dns_host_info`
- `dns_server`
- `dns_server_info`
- `ipam_next_available_address_block_info`
- `ipam_next_available_subnet_info`
- `ipam_next_available_ip_info`
- `ipam_range`
- `ipam_range_info`
- `tsig_key`
- `tsig_key_info`
- `kerberos_key_info`
- `dns_acl`
- `dns_acl_info`
- `infra_host`
- `infra_host_info`
- `infra_join_token`
- `infra_join_token_info`
- `infra_service`
- `infra_service_info`


[//]: # (### Not yet migrated)

[//]: # (- `dhcp_option_sapce`)

[//]: # (- `dhcp_option_space_info`)

[//]: # (- `dhcp_fixed_address`)

[//]: # (- `dhcp_fixed_address_info`)

### Enhanced Documentation in Ansible Modules

Our latest update to the Ansible modules introduces a significant enhancement: the addition of a **Return** section. Building on the existing documentation and examples, this new section details the types of data and values returned by module execution.
####
In the current version of our Ansible modules, every example required explicit declaration of portal_key and host under the task parameters to establish connectivity and authentication details for operations. Here's how parameters were defined and used in earlier versions:

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

However, in the latest version, we have streamlined this setup by introducing module_defaults. This enhancement allows portal_key and portal_url to be set once for all modules in a block, eliminating redundancy and simplifying the configuration for all tasks within the block. This provides a cleaner, more maintainable setup:

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

In the update from Bloxone Ansible to Universal DDI Ansible of the Ansible modules, there's been a simplification of the options available for the state parameter, which is used to define the desired state of the resource being managed by the playbook.

### Bloxone Ansible State Options:
In .py files
- `present` : Ensures that the resource exists.
- `absent` : Ensures that the resource does not exist.
- `get` : Retrieves the resource details without making any changes.

In _gather.py files
- `present` : Ensures that the resource exists.
- `absent` : Ensures that the resource does not exist.
- `gather` : Retrieves the resource details without making any changes.

### Universal DDI Ansible State Options:

- `present`: Ensures that the resource exists.
- `absent`: Ensures that the resource does not exist.

> **_NOTE:_**  The new `_info` files do not use a state parameter because they are designed solely for retrieval purposes
### Support for Check Mode Added in Universal DDI Ansible

One of the significant enhancements in Universal DDI Ansible of our Ansible modules is the addition of support for **Check Mode**. This feature allows users to run playbooks in a dry-run mode, enabling them to review the potential changes and effects without making any actual modifications to the target environment.

#### Example Usage:

``` 
- name: "Create an IP space (check mode)"
  infoblox.universal_ddi.ipam_ip_space:
    name: "{{ name }}"
    state: "present"
  check_mode: true
```
### Migrating from Bloxone Ansible to Universal DDI Ansible
### IPAM Subnet 

#### In Bloxone Ansible
In Bloxone Ansible, when creating a subnet, you directly specify the space name as a string:

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
    state: present
```

#### In Universal DDI Ansible
Universal DDI Ansible uses the IP space id, which is a more precise and programmatically robust method of referencing the IP space when creating a subnet:

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

### DNS Record Management
### In Bloxone Ansible:
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

### In Universal DDI Ansible:

Universal DDI Ansible introduces a significant simplification. A single module, infoblox.universal_ddi.dns_record, is now capable of handling all types of DNS records.The module uses a generic structure with a type field and a flexible rdata dictionary to accommodate data specific to each record type.
> **_NOTE:_**  In Universal DDI Ansible, support for additional records like AAAA, CAA, DNAME, Generic, MX, NAPTR, SRV, SVCB and TXT is also added

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


#### Address Block 

In Bloxone Ansible, IP Spaces were directly referenced by their names where as in Universal DDI Ansible it is referenced by id

### Create Address Block in Bloxone Ansible
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

### Create Address Block in Universal DDI Ansible
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

### Next Available Address Block

#### In Bloxone Ansible : 

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
    api_key: "{{ api }}"
    host: "{{ host }}"
    state: present
        
- name: Create Address Block using next-available subnet
  b1_ipam_address_block:
    space: "qa-space-1"
    address: '{"next_available_address_block": {"cidr": "28", "count": "5", "parent_block": "40.0.0.0/24"}}'
    name: "qa-nextAvailable"
    comment: "Created by QA using nextavailable"
    api_key: "{{ api }}"
    host: "{{ host }}"
    state: present
```
#### In Universal DDI Ansible
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
### DNS Auth Zone

#### In Bloxone Ansible
In Bloxone Ansible, View is directly referenced by their names where as in Universal DDI Ansible it is referenced by id

```
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

#### In Universal DDI

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

#### DNS View

#### In Bloxone Ansible

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
```

#### In Universal DDI Ansible

```
- name: Create a view
  infoblox.universal_ddi.dns_view:
    name: "view1"
    state: "present"
```

#### IPAM Address

#### In Bloxone Ansible

It was ipv4 reservation

```
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
#### In Universal DDI Ansible

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

