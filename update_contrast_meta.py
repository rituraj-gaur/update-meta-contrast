#Use this program to update the meta-data for a given application(s)

import requests
import json
import sys

app_id = input('Enter Application ID : ')
org_id = <YOUR ORG ID HERE>
auth = '#############'     # Replace this Auth token
API = '##############'   # Replace this with API-key


def getSquad(org_id, app_id):
    url_squad = ('https://app.contrastsecurity.com/Contrast/api/ng/' + org_id + '/applications/' + str(
        app_id) + '/?expand=metadata')
    # Create data for request
    headers_1 = {'Authorization': auth, 'API-Key': API}
    r_squad = requests.get(url=url_squad, headers=headers_1)
    st_code = r_squad.status_code
    if st_code == 401:
        print('Invalid Authorization token or API-Key. Aborted.....')
        sys.exit(1)
    elif st_code != 200:
        print('Cannot get current Squad for this app id. Please review the app id entered.')
        sys.exit(1)

    # extracting data in json format
    data_squad = r_squad.json()
    try:
        curr_squad = (data_squad['application']["metadataEntities"][0]["fieldValue"])
        print('Current squad value :' + curr_squad)
    except IndexError as e:
        print('Current squad value : NULL')
    # print(data_squad)
    app_name = data_squad["application"]['name']
    print('Application Name : ' + app_name)
    return app_name


getSquad(org_id, app_id)

#Get new values from user
new_squad = input('Enter new squad value : ')
len_sq=len(new_squad)
payload = [{"organization_id": org_id, "application_id": app_id, "key": "squadName", "value": new_squad}]

if len_sq > 32:
    print('Squad nme value too lengthy. Aborting operation.....')
    sys.exit(1)

try:
    con_url = ('https://app.contrastsecurity.com/Contrast/api/ng/' + org_id + '/applications/' + str(
        app_id) + '/metadata/user')
    headers_2 = {'Authorization': auth, 'API-Key': API, 'accept': 'application/json',
                 'content-type': 'application/json'}

    r = requests.put(con_url, data=json.dumps(payload), headers=headers_2)
    status = r.status_code
    if status == 200:
        print('Updated Squad name  : ' + new_squad + '\n')
    else:
        print('Failed with error code : ', status)

except Exception as err:
    print('Aborted with error : ', err)
    sys.exit(1)
