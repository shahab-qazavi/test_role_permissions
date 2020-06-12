import sys
import os
sys.path.append(os.getcwd())

from xlrd import open_workbook
from general_functions_roles import init_database_without_user, get_admin_token, get_user_token, get_complex_token,\
    get_operator_token, get_guest_token
import requests
from public_role import consts

wb = open_workbook('permissions.xlsx')

init_database_without_user()

# Variables
html = '''<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta http-equiv="X-UA-Compatible" content="ie=edge">
    <title>Permissions Role</title>
    <style>
        body {
            margin: 0;
            padding: 0;
            font-size: 100%%;
            background-color: #121212;
        }
        * {
            margin: 0;
            padding: 0;
            font-size: 100%%;
        }
        table {
            width: 100%%;
            border-collapse: collapse;
            max-width: 1500px;
            margin: 70px auto;
            background-color: #262626;
            box-shadow: 0px 0px 15px 2px #ffffff2c;
            position: relative;
        }
        table tr {
            display: flex;
        }
        
        table td, table th {
            flex: 1;
        }
        table thead tr th {
            font-size: 1.4rem;
            padding: 10px 15px;
            flex: 1;
        }
        table thead tr {
            display: flex;
            max-width: 1500px;
            margin: auto;
        }
        table thead {
            position: fixed;
            width: 100%%;
            left: 0;
            right: 0;
            top: 0;
            padding: 5px 0;
            background-color: #444444;
        }
        table thead th {
            color: #e2e2e2;
        }
        table tbody tr td {
            text-align: center;
            color: #a8a8a8;
            font-size: 1.4rem;
            padding: 15px;
        }

        table tbody tr td,
        table tbody tr {
            transition: all linear .2s;
            -webkit-transition: all linear .2s;
            -o-transition: all linear .2s;
            -moz-transition: all linear .2s;
            -ms-transition: all linear .2s;
        }

        table tbody tr td:hover {
            font-size: 1.8rem;
        }

        table tbody tr:hover {
            background-color: #b3b3b321;
            transform: scale(1.02);
        }
    </style>
</head>
<body>
    <div class="">
        <table>
            <thead>
                <tr>
                    <th>Role</th>
                    <th>API</th>
                    <th>Get Method</th>
                    <th>Post Method</th>
                    <th>Put Method</th>
                    <th>Delete Method</th>
                </tr>
            </thead>
            <tbody>
                %s
            </tbody>
        </table>
    </div>
</body>
</html>
'''
admin_token = get_admin_token()['token']
user_token = get_user_token()
guest_token = get_guest_token()
complex_token = get_complex_token()
operator_token = get_operator_token()
color_get = 'gray'
color_post = 'gray'
color_put = 'gray'
color_delete = 'gray'
get_sign = "-"
post_sign = "-"
put_sign = "-"
delete_sign = "-"
permission_message = "You do not have permission to access this section!"
rows = ""
get_status = "shit error!"
post_status = "shit error!"
put_status = "shit error!"
delete_status = "shit error!"
values = []
# End Variables

for s in wb.sheets():
    values = []
    for row in range(s.nrows):
        col_value = []
        for col in range(s.ncols):
            value = s.cell(row, col).value
            try:
                value = str(int(value))
            except:
                pass
            col_value.append(value)
        values.append(col_value)

for j in values:
    print(j)
    if j[0] == 'admin':
        token = admin_token
    elif j[0] == 'user':
        token = user_token
    elif j[0] == 'guest':
        token = guest_token
    elif j[0] == 'complex':
        token = complex_token
    elif j[0] == 'operator':
        token = operator_token
    else:
        token = ''
    if token != '':

        data = {'token': token, 'locale':'en'}
        get = requests.get(consts.SERVER_ADDRESS+'/%s' % j[1], data=data)

        post = requests.post(consts.SERVER_ADDRESS+'/%s' % j[1], json=data)

        put = requests.put(consts.SERVER_ADDRESS+'/%s' % j[1], json=data)

        delete = requests.delete(consts.SERVER_ADDRESS+'/%s' % j[1], json=data)

        if get.status_code != 404 or post.status_code != 404 or put.status_code != 404 or delete.status_code != 404:
            try:
                get_status = get.json()['note']
            except:
                get_status = get.text
            try:
                post_status = post.json()['note']
            except:
                post_status = post.text
            try:
                put_status = put.json()['note']
            except:
                put_status = put.text
            try:
                delete_status = delete.json()['note']
            except:
                delete_status = delete.text

            print('before print')
            print(get)
            print(post)
            print(put)
            print(delete)
            postcode = post.status_code
            getcode = get.status_code
            putcode = put.status_code
            deletecode = delete.status_code
            try:
                print(get.json())
            except:
                print(get.text)
            for cell in range(2,6):
                if j[cell] == '✓':
                    if cell == 2 and getcode != 403:
                        if getcode == 500:
                            color_get = "yellow"
                        else:
                            color_get = "green"
                        get_sign = '✓'
                    elif cell == 2 and getcode == 403:
                        color_get = "red"
                        get_sign = '✓'

                    if cell == 3 and postcode != 403:
                        if postcode == 500:
                            color_post = "yellow"
                        else:
                            color_post = "green"
                        post_sign = '✓'
                    elif cell == 3 and postcode == 403:
                        color_post = "red"
                        post_sign = '✓'

                    if cell == 4 and putcode != 403:
                        if putcode == 500:
                            color_put = "yellow"
                        else:
                            color_put = "green"
                        put_sign = '✓'
                    elif cell == 4 and putcode == 403:
                        color_put = "red"
                        put_sign = '✓'

                    if cell == 5 and deletecode != 403:
                        if deletecode == 500:
                            color_delete = "yellow"
                        else:
                            color_delete = "green"
                        delete_sign = '✓'
                    elif cell == 5 and deletecode == 403:
                        color_delete = "red"
                        delete_sign = '✓'

                elif j[cell] == '✘':
                    if cell == 2 and getcode == 403:
                        color_get = "green"
                        get_sign = '✘'
                    elif cell == 2 and getcode != 403:
                        if getcode == 500:
                            color_get = "purple"
                        else:
                            color_get = "red"
                        get_sign = '✘'

                    if cell == 3 and getcode == 403:
                        color_get = "green"
                        get_sign = '✘'
                    elif cell == 3 and getcode != 403:
                        if getcode == 500:
                            color_get = "purple"
                        else:
                            color_get = "red"
                        get_sign = '✘'

                    if cell == 4 and getcode == 403:
                        color_get = "green"
                        get_sign = '✘'
                    elif cell == 4 and getcode != 403:
                        if getcode == 500:
                            color_get = "purple"
                        else:
                            color_get = "red"
                        get_sign = '✘'

                    if cell == 5 and getcode == 403:
                        color_get = "green"
                        get_sign = '✘'
                    elif cell == 5 and getcode != 403:
                        if getcode == 500:
                            color_get = "purple"
                        else:
                            color_get = "red"
                        get_sign = '✘'

            rows += "<tr style='text-align: center;'><td>%s</td><td>%s</td>" \
                    "<td style='color: %s;' title='%s'> %s</td>" \
                    "<td style='color: %s;' title='%s'>%s</td>" \
                    "<td style='color: %s;' title='%s'> %s</td>" \
                    "<td style='color: %s;' title='%s'>%s</td></tr>" % (
                        j[0],
                        j[1],
                        color_get,
                        get_status,
                        get_sign,
                        color_post,
                        post_status,
                        post_sign,
                        color_put,
                        put_status,
                        put_sign,
                        color_delete,
                        delete_status,
                        delete_sign)

file = open('role-permissions.html', 'wb',)
file.write((html % rows).encode('utf-8'))
file.close()
