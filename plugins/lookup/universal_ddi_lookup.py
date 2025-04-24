# -*- coding: utf-8 -*-
# Copyright (c) 2021 Infoblox, Inc.
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type


DOCUMENTATION = """
---
name: universal_ddi_lookup
author: Infoblox Inc. (@infobloxopen)
short_description: Query Universal DDI objects using the Universal DDI APIs
version_added: "1.1.0"
description:
  - Uses the Universal DDI APIs to fetch specific objects.  This lookup
    supports adding additional keywords to filter the return data and specify
    the desired set of returned fields.
requirements:
  - requests

options:
    _terms:
      description: The name of the object to returned from Universal DDI API
      required: True
      type: str
    fields:
      description:
        - The list of field names to return for the specified object.
    filters:
      description:
        - A dict object that is used to filter the return objects.
      type: dict
    tfilters:
      description:
        - A dict object containing tags that are used to filter the return objects.
      type: dict
    provider:
      description:
        - A dict object containing Universal DDI Portal URL and Key for authentication.
        - The portal URL and key can be set in the environment variables using `portal_url` and `portal_key` respectively.
        - Default value for portal_url is "https://csp.infoblox.com".
"""

EXAMPLES = """
- name: List all IP Spaces
  ansible.builtin.set_fact:
    ip_space: "{{ lookup('infoblox.universal_ddi.universal_ddi','ipam/ip_space', provider={'portal_url': 'https://csp.infoblox.com', 'portal_key': 'portal_key'}) }}"
    
- name: List all IP Spaces and output specific fields
  ansible.builtin.set_fact:
    ip_space: "{{ lookup('infoblox.universal_ddi.universal_ddi','ipam/ip_space', fields=['id', 'name', 'comment'] , provider={'portal_url': 'https://csp.infoblox.com', 'portal_key': 'portal_key'}) }}"

- name: Get an IP Space using name as a filter using environment variables
  ansible.builtin.set_fact:
    ip_space: "{{ lookup('infoblox.universal_ddi.universal_ddi','ipam/ip_space', filters={'name': 'hostname.ansible.com'} , provider={'portal_url': 'https://csp.infoblox.com', 'portal_key': 'portal_key'}) }}"

- name: Get all IP Spaces using tag filters
  ansible.builtin.set_fact:
    ip_space: "{{ lookup('infoblox.universal_ddi.universal_ddi','ipam/ip_space', tfilters={'location': 'site-1'} , provider={'portal_url': 'https://csp.infoblox.com', 'portal_key': 'portal_key'}) }}"

"""  # noqa: E501

RETURN = """
results:
    description:
     - The result of the lookup call or the error provided by the API.
"""

import os
import traceback

from ansible.errors import AnsibleError
from ansible.plugins.lookup import LookupBase

try:
    import requests
except ImportError:
    HAS_REQUESTS_LIB = False
    REQUESTS_LIB_IMP_ERR = traceback.format_exc()
else:
    HAS_REQUESTS_LIB = True
    REQUESTS_LIB_IMP_ERR = None


def return_base_url(obj_type):
    """Returns the base URL for the object type"""
    base_obj_type = obj_type.split("/")[0]
    if base_obj_type == "anycast":
        return "/api/anycast/v1"
    elif base_obj_type == "cloud_discovery":
        return "/api/cloud_discovery/v2"
    elif (
        base_obj_type == "dns_config"
        or base_obj_type == "dns_data"
        or base_obj_type == "ipam"
        or base_obj_type == "dhcp"
        or base_obj_type == "ipam_federation"
        or base_obj_type == "keys"
    ):
        return "/api/ddi/v1"
    elif base_obj_type == "infra_mgmt":
        return "/api/infra/v1"
    elif base_obj_type == "infra_provision":
        return "/api/host-activation/v1"
    else:
        raise AnsibleError(f"Invalid object type: {obj_type}")


def get_object(obj_type, provider, filters, tfilters, fields):
    """Creating the GET API request for lookup"""
    try:

        if len(provider) > 0:
            portal_url = provider["portal_url"]
            portal_key = provider["portal_key"]
        else:
            portal_url = os.getenv("portal_url", "https://csp.infoblox.com")
            portal_key = os.getenv("portal_key", None)

    except KeyError:
        return (
            {
                "status": "400",
                "response": "Invalid Syntax for provider",
                "provider": provider,
            },
        )
    endpoint = f"{return_base_url(obj_type)}/{obj_type}"
    flag = 0
    if fields is not None and isinstance(fields, list):
        temp_fields = ",".join(fields)
        endpoint = endpoint + "?_fields=" + temp_fields
        flag = 1

    if filters != {} and isinstance(filters, dict):
        temp_filters = []
        for k, v in filters.items():
            if str(v).isdigit():
                temp_filters.append(f"{k}=={v}")
            else:
                temp_filters.append(f"{k}=='{v}'")
        res = " and ".join(temp_filters)
        if flag == 1:
            endpoint = endpoint + "&_filter=" + res
        else:
            endpoint = endpoint + "?_filter=" + res
            flag = 1

    if tfilters != {} and isinstance(tfilters, dict):
        temp_tfilters = []
        for k, v in tfilters.items():
            if str(v).isdigit():
                temp_tfilters.append(f"{k}=={v}")
            else:
                temp_tfilters.append(f"{k}=='{v}'")
        res = " and ".join(temp_tfilters)
        if flag == 1:
            endpoint = endpoint + "&_tfilter=" + res
        else:
            endpoint = endpoint + "?_tfilter=" + res

    # reproduced module_utils. Replace once published
    try:
        headers = {"Authorization": f"Token {portal_key}"}
        url = f"{portal_url}{endpoint}"
        result = requests.get(url, headers=headers)
    except Exception:
        raise Exception("API request failed")

    if result.status_code in [200, 201, 204]:
        return [result.json()]
    elif result.status_code == 401:
        return [result.content]
    else:
        meta = {"status": result.status_code, "response": result.json()}
        return [meta]


class LookupModule(LookupBase):
    def run(self, terms, variables=None, **kwargs):
        if not HAS_REQUESTS_LIB:
            raise AnsibleError("The 'universal_ddi' lookup cannot be run without the 'requests' library installed.")(
                REQUESTS_LIB_IMP_ERR
            )
        try:
            obj_type = terms[0]
        except IndexError:
            raise AnsibleError("the object_type must be specified")

        fields = kwargs.pop("fields", None)
        filters = kwargs.pop("filters", {})
        tfilters = kwargs.pop("tfilters", {})
        provider = kwargs.pop("provider", {})
        res = get_object(obj_type, provider, filters, tfilters, fields)
        return res
