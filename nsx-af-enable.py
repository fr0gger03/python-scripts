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
ap.add_argument('-sid', '--sddc_id', required=True, help="The ID of the VMware Cloud on Dell SDDC to be renamed.")
ap.add_argument('-state', '--state', required = True, choices=['on','off'],type=str.lower, help="The desired state of the NSX AF service.")

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
if args.state == 'on':
    nsxaf_state = True
else:
    nsxaf_state = False

# get an access token
token_params = {'refresh_token': my_token}
token_headers = {'Content-Type': 'application/x-www-form-urlencoded'}
token_response = requests.post('https://console.cloud.vmware.com/csp/gateway/am/api/auth/api-tokens/authorize',params=token_params, headers=token_headers)
token_json = token_response.json()
access_token = token_json['access_token']

# enable the NSX AF firewall
myheader = {'csp-auth-token': access_token}
myurl = f'https://vmc.vmware.com/vmc/skynet/api/orgs/{orgid}/sddcs/{sddcid}/nsx-advanced-addon?enable={nsxaf_state}'
response = requests.post(myurl, headers=myheader)
if response.status_code == 202:
    print(f'NSX Advanced Firewall modified - set to {args.state}')
else:
    print("There was an error. Check the syntax.")
    print(f'API call failed with status code {response.status_code}. URL: {myurl}.')
    print(response)
    sys.exit()