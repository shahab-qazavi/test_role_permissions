from openpyxl import Workbook
from publics import db
col_permissions = db()['users_roles']
wb = Workbook()
ws = wb.active
ws.append(['role', 'module', 'get','post','put','delete'])

for item in col_permissions.find():

    permissions = {}
    permissions['get'] = '✓' if 'get' in item['permissions']['allow'] else '✘'
    permissions['post'] = '✓' if 'post' in item['permissions']['allow'] else '✘'
    permissions['put'] = '✓' if 'put' in item['permissions']['allow'] else '✘'
    permissions['delete'] = '✓' if 'delete' in item['permissions']['allow'] else '✘'

    ws.append([item['name'], item['module'], permissions['get'], permissions['post'], permissions['put'], permissions['delete']])
wb.save('permissions.xlsx')