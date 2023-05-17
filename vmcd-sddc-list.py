#!/usr/bin/env python3

import argparse
import requests                         # need this for Get/Post/Delete
import json
import sys
from prettytable import PrettyTable



ap = argparse.ArgumentParser(
                prog = 'VMware Cloud on Dell SDDC list utility',
                description = 'A Command-line utility to be used to list the SDDCs for VMware Cloud on Dell SDDC.',
                )

# ============================
# define arguments
# ============================
ap.add_argument('-oid', '--org_id', required=True, help="The ID of the VMware Cloud Organization.")
ap.add_argument('-t', '--refresh_token', required=True, help="The user's refresh token for the VMware Cloud org.  User must be an Org Member, and be assigned the VMC on Dell Administrator role.")
ap.add_argument('-sid', '--sddc_id', help="The ID of the VMware Cloud on Dell SDDC to be renamed.")

# ============================
# Parse arguments
# ============================
args = ap.parse_args()

# ============================
# instantiate variables
# ============================
my_token = args.refresh_token
orgid = args.org_id
if args.sddc_id is not None:
    sddcid = args.sddc_id
else:
    pass

# get an access token
token_params = {'refresh_token': my_token}
token_headers = {'Content-Type': 'application/x-www-form-urlencoded'}
token_response = requests.post('https://console.cloud.vmware.com/csp/gateway/am/api/auth/api-tokens/authorize',params=token_params, headers=token_headers)
token_json = token_response.json()
access_token = token_json['access_token']

# rename the SDDC
myheader = {'csp-auth-token': access_token}
if args.sddc_id is not None:
    myurl = f'https://vmc.vmware.com/vmc/fractal/api/orgs/{orgid}/edges/{sddcid}'
    response = requests.get(myurl, headers=myheader)
    if response.status_code == 200:
        json_response = response.json()
        # print(json.dumps(json_response, indent=2))
        print(f'SDDC Name: {json_response["name"]}')
        print(f'Status: {json_response["edge_sddc_resource_config"]["customer_status"]}')
        print(f'OEM: {json_response["edge_sddc_resource_config"]["oem_name"]}')
        print(f'vCenter FQDN: {json_response["edge_sddc_resource_config"]["vcenter_config"]["public_fqdn"]}')
        print(f'SDDC Version: {json_response["edge_sddc_resource_config"]["software_bundle_config"]["dimension_sddc_version"]}')
    else:
        print("There was an error. Check the syntax.")
        print(f'API call failed with status code {response.status_code}. URL: {myurl}.')
        print(response)
        sys.exit()
else:
    myurl = f'https://vmc.vmware.com/vmc/fractal/api/orgs/{orgid}/edges/detailed'
    response = requests.get(myurl, headers=myheader)
    if response.status_code == 200:
        json_response = response.json()
        table = PrettyTable(['Name', 'ID', 'Host Count', 'City', 'State'])
        for i in json_response:
            table.add_row([i['name'],i['id'],i['num_hosts'],i['city'],i['state']])
        print(table)
    else:
        print("There was an error. Check the syntax.")
        print(f'API call failed with status code {response.status_code}. URL: {myurl}.')
        print(response)
        sys.exit()