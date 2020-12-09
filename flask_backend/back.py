
from flask import Flask, request, make_response
from flask_cors import *
import operations as op

app = Flask(__name__)
app.debug = True

operation = op.Operation('166.111.80.113', 9999)

user_list = [
    'administrator',
    'developer1',
    'developer2',
    'developer3',
    'developer4'
]

user_password_check = {
    'administrator': 'administrator',
    'developer1': 'developer1',
    'developer2': 'developer2',
    'developer3': 'developer3',
    'developer4': 'developer4'
}

global_user_privilege = {
    '创建数据库权限': {
        'administrator': True,
        'developer1': True,
        'developer2': False,
        'developer3': True,
        'developer4': False
    },
    '访问数据库权限': {
        'administrator': True,
        'developer1': True,
        'developer2': True,
        'developer3': True,
        'developer4': False
    },
    '删除数据库权限': {
        'administrator': True,
        'developer1': True,
        'developer2': False,
        'developer3': True,
        'developer4': False
    },
}


db_privileges = {
    'industry_database_0_1': {
        '创建表权限': {
            'administrator': True,
            'developer1': True,
            'developer2': False,
            'developer3': True,
            'developer4': False
        },
        '修改表权限': {
            'administrator': True,
            'developer1': True,
            'developer2': False,
            'developer3': True,
            'developer4': False
        },
        '查看表权限': {
            'administrator': True,
            'developer1': True,
            'developer2': False,
            'developer3': True,
            'developer4': False
        },
        '删除表权限': {
            'administrator': True,
            'developer1': True,
            'developer2': False,
            'developer3': True,
            'developer4': False
        },
    }
}

db = {
    0: {
        'db_list': [
            'industry_database_0_1',
            'industry_database_0_2',
            'industry_database_0_3'
        ],
        'industry_database_0_1': {
            'table_list': [
                'industry_table_0_1_1',
                'industry_table_0_1_2',
            ],
            'industry_table_0_1_1': {
                'schema': [{
                    'name': 'car_id',
                    'type': 'integer',
                    'constraint': ['primary key']
                }, {
                    'name': 'car_name',
                    'type': 'varchar(32)',
                    'constraint': []
                }],
                'rows': [{
                    'car_id': 0,
                    'car_name': 'Ford 2009'
                }, {
                    'car_id': 1,
                    'car_name': 'Forge 4'
                }]
            }
        },
        'industry_database_0_2': {
            'table_list': [
                'industry_table_0_2_1',
                'industry_table_0_2_2',
            ]
        },
        'industry_database_0_3': {
            'table_list': [
                'industry_table_0_3_1',
                'industry_table_0_3_2',
            ]
        }
    },
    1: {
        'db_list': [
            'industry_database_1_1',
            'industry_database_1_2',
            'industry_database_1_3'
        ],
        'industry_database_1_1': {
            'table_list': [
                'industry_table_1_1_1',
                'industry_table_1_1_2',
            ]
        },
        'industry_database_1_2': {
            'table_list': [
                'industry_table_1_2_1',
                'industry_table_1_2_2',
            ]
        },
        'industry_database_1_3': {
            'table_list': [
                'industry_table_1_3_1',
                'industry_table_1_3_2',
            ]
        }
    },
}

existing_files = {
    'backup_1.sql'
}

def prepare():
    global user_list, user_password_check, global_user_privilege, db_privileges
    user_list = operation.get_users_list()
    user_password_check = {
        user: user for user in user_list
    }
    global_user_privilege, db_privileges = operation.get_users_privilege()



def is_admin(username):
    return username == 'root'
    # return username.startswith('admin')


# Create, Delete, Update, Retrieve
def have_db_privilege(username, instance_id, access_type):
    cn_name = {
        'C': '创建',
        'D': '删除',
        'R': '访问'
    }[access_type]
    return username in user_list \
        and global_user_privilege[f'{cn_name}数据库权限'][username]


def have_table_privilege(username, instance_id, db_name, access_type):
    cn_name = {
        'C': '创建',
        'D': '删除',
        'U': '修改',
        'R': '查看'
    }[access_type]
    return username in user_list \
        and global_user_privilege['访问数据库权限'][username] \
        and db_privileges[db_name][f'{cn_name}表权限'][username]



# platform
@app.route('/login/', methods=['POST'])
@cross_origin()
def login():
    username = request.json['username']
    password = request.json['password']
    login_success = username in user_list and user_password_check[username] == password
    if login_success:
        response = {
            'success': True,
            'result': '登录成功',
            'usertype': '管理员' if is_admin(username) else '普通用户'
        }
    else:
        response = {
            'success': True,
            'result': '登录失败',
            'usertype': '管理员' if is_admin else '普通用户'
        }
    return make_response(response)


@app.route('/<string:dbtype>/authenticate/', methods=['POST'])
@cross_origin()
def authenticate(dbtype):
    username = request.json['username']
    password = request.json['password']
    auth_success = username in user_list and user_password_check[username] == password
    # print(username, password)
    # auth_success = operation.interface.ident_auth(username, password)
    response = {
        'success': auth_success,
        'result': '认证成功' if auth_success else '认证失败'
    }
    return make_response(response, 200)


@app.route('/<string:dbtype>/user-list/', methods=['GET'])
@cross_origin()
def get_user_list(dbtype):
    username = request.args.get('username', '')
    request_success = username in user_list
    response = {
        'success': request_success,
        'result': user_list if request_success else []
    }
    print(response)
    return make_response(response, 200)


@app.route('/<string:dbtype>/user-privilege-list/', methods=['GET'])
@cross_origin()
def get_user_privilege_list(dbtype):
    username = request.args.get('username', '')
    request_success = username in user_list
    global_privilege = {
        'caseId': 0,
        'title': '全局权限管理',
        'children': [{
            'itemId': i,
            'title': privilege_name,
            'granted': granted
        }
        for i, (privilege_name, granted) in enumerate(global_user_privilege.items())]
    }
    response = {
        'success': request_success,
        'result': [global_privilege] if request_success else []
    }
    print(response)
    return make_response(response, 200)


@app.route('/<string:dbtype>/update-user-privilege-list/', methods=['POST'])
@cross_origin()
def update_user_privilege_list(dbtype):
    global global_user_privilege
    username = request.json['username']
    request_success = username in user_list and is_admin(username)
    if request_success:
        grant_units = []
        revoke_units = []
        new_privilege_list = request.json['privilege']
        # print(new_privilege_list)
        for privilege in new_privilege_list[0]['children']:
            for username in user_list:
                # 创建, root, True
                privilege_unit = (privilege['title'], username, privilege['granted'][username])
                old_state = global_user_privilege[privilege['title']][username]
                if old_state and not privilege_unit[2]:
                    revoke_units.append(privilege_unit)
                elif privilege_unit[2] and not old_state:
                    grant_units.append(privilege_unit)
                # global_user_privilege[privilege['title']][username] = privilege['granted'][username]
        # print(global_user_privilege)
        print('Grant: ', grant_units)
        print('Revoke: ', revoke_units)
    response = {
        'success': request_success,
        'result': '更新成功' if request_success else '更新失败'
    }
    return make_response(response, 200)


@app.route('/<string:dbtype>/create-database/', methods=['POST'])
@cross_origin()
def create_database(dbtype):
    global db
    db_name = request.json['databaseName']
    username = request.json['username']
    instance_id = int(request.json['instanceId'])
    request_success = have_db_privilege(username, instance_id, 'C')
    if request_success:
        create_success = db_name not in db[instance_id]['db_list']
        if create_success:
            db[instance_id]['db_list'].append(db_name)
            db[instance_id][db_name] = {
                'table_list': []
            }
        response = {
            'success': create_success,
            'result': '创建成功' if create_success else '创建失败'
        }
    else:
        response = {
            'success': False,
            'result': '没有权限'
        }
    return make_response(response, 200)


@app.route('/<string:dbtype>/list-database/', methods=['GET'])
@cross_origin()
def list_database(dbtype):
    global db
    username = request.args.get('username', '')
    instance_id = int(request.args.get('instanceId', 0))
    print(username, instance_id)
    request_success = username in user_list and global_user_privilege['访问数据库权限'][username]
    response = {
        'success': request_success,
        'result': db[instance_id]['db_list'] if request_success else []
    }
    return make_response(response, 200)


# 9. 创建表
@app.route('/<string:dbtype>/create-table/', methods=['POST'])
@cross_origin()
def create_table(dbtype):
    global db
    db_name = request.json['databaseName']
    table_name = request.json['tableName']
    username = request.json['username']
    instance_id = int(request.json['instanceId'])
    request_success = username in user_list \
        and global_user_privilege['访问数据库权限'][username] \
        and db_privileges[db_name]['创建表权限'][username]
    if request_success:
        create_success = table_name not in db[instance_id][db_name]['table_list']
        if create_success:
            db[instance_id][db_name]['table_list'].append(table_name)
            db[instance_id][db_name][table_name] = {}
        response = {
            'success': create_success,
            'result': '创建成功' if create_success else '已经存在'
        }
    else:
        response = {
            'success': False,
            'result': '没有权限'
        }
    return make_response(response, 200)


# 10. 查看表信息
@app.route('/<string:dbtype>/view-table-schema/', methods=['GET'])
@cross_origin()
def view_table_schema(dbtype):
    username = request.args.get('username', '')
    instance_id = int(request.args.get('instanceId', '0'))
    db_name = request.args.get('databaseName', '')
    table_name = request.args.get('tableName', '')
    encrypt_method = request.args.get('encryptMethod', '')
    if db_name not in db[instance_id]:
        response = {
            'success': False,
            'result': {},
            'msg': '该数据库不存在'
        }
    elif table_name not in db[instance_id][db_name]:
        response = {
            'success': False,
            'result': {},
            'msg': '该表不存在'
        }
    else:
        print(username, instance_id, db_name)
        request_success = have_table_privilege(username, instance_id, db_name, 'R')
        if request_success:
            schema = db[instance_id][db_name][table_name]['schema']
            response = {
                'success': True,
                'result': {
                    'tableName': table_name,
                    'schema': [{
                        'id': i,
                        'columnName': column['name'] if encrypt_method == '' else '[enc]' + column['name'],
                        'columnType': column['type'],
                        'columnConstraint': column['constraint']
                    } for i, column in enumerate(schema)]
                }
            }
        else:
            response = {
                'success': False,
                'result': {},
                'msg': '没有权限'
            }
    return make_response(response, 200)


# 11. 插入数据
@app.route('/<string:dbtype>/insert/', methods=['POST'])
@cross_origin()
def insert(dbtype):
    username = request.json['username']
    instance_id = int(request.json['instanceId'])
    db_name = request.json['databaseName']
    table_name = request.json['tableName']
    authed = have_table_privilege(username, instance_id, db_name, 'U')
    if authed:
        insert_success = table_name in db[instance_id][db_name]['table_list']
        response = {
            'success': insert_success,
            'result': '插入成功' if insert_success else '不存在该表'
        }
    else:
        response = {
            'success': False,
            'result': '没有权限'
        }
    return make_response(response, 200)

# 12. 更新数据
@app.route('/<string:dbtype>/update/', methods=['POST'])
@cross_origin()
def update(dbtype):
    username = request.json['username']
    instance_id = int(request.json['instanceId'])
    db_name = request.json['databaseName']
    table_name = request.json['tableName']
    authed = have_table_privilege(username, instance_id, db_name, 'U')
    if authed:
        update_success = table_name in db[instance_id][db_name]['table_list']
        response = {
            'success': update_success,
            'result': '更新成功' if update_success else '不存在该表'
        }
    else:
        response = {
            'success': False,
            'result': '没有权限'
        }
    return make_response(response, 200)


# 13. 删除数据
@app.route('/<string:dbtype>/delete/', methods=['POST'])
@cross_origin()
def delete(dbtype):
  if dbtype == 'relational':
    username = request.json['username']
    instance_id = int(request.json['instanceId'])
    db_name = request.json['databaseName']
    table_name = request.json['tableName']
    authed = have_table_privilege(username, instance_id, db_name, 'U')
    if authed:
        delete_success = table_name in db[instance_id][db_name]['table_list']
        response = {
            'success': delete_success,
            'result': '删除成功' if delete_success else '不存在该表'
        }
    else:
        response = {
            'success': False,
            'result': '没有权限'
        }
    return make_response(response, 200)

  elif dbtype=='graph':
    username = request.json['username']
    instance_id = int(request.json['instanceId'])
    response = {
      'success': True,
      'result': '删除成功'
    }

    return make_response(response, 200)

# 14. 查看数据
@app.route('/<string:dbtype>/select/', methods=['GET'])
@cross_origin()
def select(dbtype):
  if dbtype=='relational':
    username = request.args.get('username', '')
    instance_id = int(request.args.get('instanceId', '0'))
    db_name = request.args.get('databaseName', '')
    table_name = request.args.get('tableName', '')
    encrypt_method = request.args.get('encryptMethod', '')
    if db_name not in db[instance_id]:
        response = {
            'success': False,
            'result': [],
            'msg': '该数据库不存在'
        }
    elif table_name not in db[instance_id][db_name]['table_list']:
        response = {
            'success': False,
            'result': [],
            'msg': '该表不存在'
        }

    else:
        authed = have_table_privilege(username, instance_id, db_name, 'R')
        if authed:
            rows = db[instance_id][db_name][table_name]['rows']
            response = {
                'success': True,
                'result': []
            }
            for i, row in enumerate(rows):
                if encrypt_method == '':
                    new_row = {column_name: value for (column_name, value) in row.items()}
                else:
                    new_row = {column_name: '[enc]' + value for (column_name, value) in row.items()}
                new_row['id'] = i
                response['result'].append(new_row)
        else:
            response = {
                'success': False,
                'result': [],
                'msg': '没有权限'
            }
    return make_response(response, 200)

  elif dbtype=='graph':
    username = request.args.get('username', '')
    instance_id = int(request.args.get('instanceId', '0'))
    response = {
      'success': True,
      'result': {
        "schema":[{
          "id":0,
          "columnName":"user_id",
          "columnType":"integer"
        },{
          "id":1,
          "columnName":"name",
          "columnType":"string"
        }],
        "data":[{
          "id":0,
          "user_id":1,
          "name":"Alice"
        },{
          "id":1,
          "user_id":2,
          "name":"Bob"
        }]
      },
      'msg': '查找成功'
    }
    return make_response(response, 200)

# 15. 查看嵌入后数据信息
@app.route('/<string:dbtype>/select-embedding/', methods=['GET'])
@cross_origin()
def select_embedding(dbtype):
    username = request.args.get('username', '')
    instance_id = int(request.args.get('instanceId', '0'))
    db_name = request.args.get('databaseName', '')
    table_name = request.args.get('tableName', '')
    embedding = request.args.get('embedding', '')
    encrypt_method = request.args.get('encryptMethod', '')
    request_success = have_table_privilege(username, instance_id, db_name, 'R')
    if request_success:
        select_success = table_name in db[instance_id][db_name]['table_list']
        if select_success:
            rows = db[instance_id][db_name][table_name]['rows']
            response = {
                'success': True,
                'result': []
            }
            for i, row in enumerate(rows):
                if encrypt_method == '':
                    new_row = {column_name: f'[{embedding}]' + str(value) for (column_name, value) in row.items()}
                else:
                    new_row = {column_name: '[enc]' + f'[{embedding}]' + str(value) for (column_name, value) in row.items()}
                new_row['id'] = i
                response['result'].append(new_row)
        else:
            response = {
                'success': False,
                'result': []
            }
    else:
        response = {
            'success': False,
            'result': []
        }
    print(response)
    return make_response(response, 200)


# 16. 删除表
@app.route('/<string:dbtype>/drop-table/', methods=['POST'])
@cross_origin()
def drop_table(dbtype):
    global db
    db_name = request.json['databaseName']
    table_name = request.json['tableName']
    username = request.json['username']
    instance_id = int(request.json['instanceId'])
    if db_name not in db[instance_id]:
        response = {
            'success': False,
            'result': [],
            'msg': '该数据库不存在'
        }
    elif table_name not in db[instance_id][db_name]['table_list']:
        response = {
            'success': False,
            'result': [],
            'msg': '该表不存在'
        }
    else:
        authed = have_table_privilege(username, instance_id, db_name, 'D')
        if authed:
            db[instance_id][db_name]['table_list'].remove(table_name)
            del db[instance_id][db_name][table_name]
            response = {
                'success': True,
                'result': '删除成功'
            }
        else:
            response = {
                'success': False,
                'result': '删除失败',
                'msg': '没有权限'
            }
    return make_response(response, 200)


# 17. 删除数据库
@app.route('/<string:dbtype>/drop-database/', methods=['POST'])
@cross_origin()
def drop_database(dbtype):
    global db
    username = request.json['username']
    instance_id = int(request.json['instanceId'])
    db_name = request.json['databaseName']
    if db_name not in db[instance_id]['db_list']:
        response = {
            'success': False,
            'result': '删除失败',
            'msg': '不存在该数据库'
        }
    else:
        authed = have_db_privilege(username, instance_id, 'D')
        if authed:
            db[instance_id]['db_list'].remove(db_name)
            del db[instance_id][db_name]
            response = {
                'success': True,
                'result': '删除成功'
            }
        else:
            response = {
                'success': False,
                'result': '删除失败',
                'msg': '没有权限'
            }
    print(db[instance_id])
    return make_response(response, 200)


@app.route('/<string:dbtype>/import-data/', methods=['POST'])
@cross_origin()
def import_data(dbtype):
  if dbtype == 'relational':
    username = request.json['username']
    instance_id = int(request.json['instanceId'])
    db_name = request.json['databaseName']
    table_name = request.json['tableName']
    filename = request.json['filename']
    import_method = request.json['method']
    authed = have_table_privilege(username, instance_id, db_name, 'U')
    if authed:
        response = {
            'success': True,
            'result': '导入成功'
        }
    else:
        response = {
            'success': False,
            'result': '导入失败',
            'msg': '没有权限'
        }
    return make_response(response, 200)

  elif dbtype=='graph':
    username = request.json['username']
    instance_id = int(request.json['instanceId'])
    filename = request.json['filename']
    response = {
      'success': True,
      'result': '导入成功'
    }
    return make_response(response, 200)


@app.route('/<string:dbtype>/export-data/', methods=['POST'])
@cross_origin()
def export_data(dbtype):
  if dbtype == 'relational':
    username = request.json['username']
    instance_id = int(request.json['instanceId'])
    db_name = request.json['databaseName']
    table_name = request.json['tableName']
    filename = request.json['filename']
    import_method = request.json['method']
    authed = have_table_privilege(username, instance_id, db_name, 'R')
    if authed:
        existing_files.add(filename)
        response = {
            'success': True,
            'result': '导出成功'
        }
    else:
        response = {
            'success': False,
            'result': '导出失败',
            'msg': '没有权限'
        }
    return make_response(response, 200)

  elif dbtype=='graph':
    username = request.json['username']
    instance_id = int(request.json['instanceId'])
    filename = request.json['filename']
    response = {
      'success': True,
      'result': '导出成功'
    }
    return make_response(response, 200)

@app.route('/<string:dbtype>/select-file/', methods=['GET'])
@cross_origin()
def select_file(dbtype):
    username = request.args.get('username', '')
    filename = request.args.get('filename', '')
    response = {
        'success': True,
        'result': [
            'create table car (',
            '  car_id   integer primary key,',
            '  car_name varchar(32),',
            ');',
            'insert into car values (0, \'Ford 2009\');'
        ]
    }
    return make_response(response, 200)


@app.route('/<string:dbtype>/log/', methods=['GET'])
@cross_origin()
def select_log(dbtype):
    username = request.args.get('username', '')
    response = {
        'success': True,
        'result': [
            '[2020-11-22 01:09:46] [developer1] drop table industry_table_0_1_1;',
            '[2020-11-22 01:09:47] [developer1] drop database industry_database_0_1;'
        ]
    }
    return make_response(response, 200)


@app.route('/<string:dbtype>/delte-file/', methods=['POST'])
@cross_origin()
def delete_file(dbtype):
    username = request.json['username']
    filename = request.json['filename']

    if filename in existing_files:
        existing_files.remove(filename)
        response = {
            'success': True,
            'result': '',
            'msg': '删除成功'
        }
    else:
        response = {
            'success': False,
            'result': '',
            'msg': '文件不存在'
        }
    return make_response(response, 200)


@app.route('/set-password/', methods=['POST'])
@cross_origin()
def set_password():
    username = request.json['username']
    password = request.json['password']
    request_success = username in user_password_check
    if request_success:
        user_password_check[username] = password
        response = {
            'success': True,
            'result': '',
            'msg': '更改成功'
        }
    else:
        response = {
            'success': False,
            'result': '',
            'msg': '用户不存在'
        }
    return make_response(response, 200)


if __name__ == '__main__':
    prepare()
    app.run(host='localhost',port=5000,debug=True)
    # host = '166.111.80.113'
    # port = 9999
    # import operations as op
    # operation = op.Operation(host, port)
    # print(operation.get_users_list())
    # print(operation.get_users_privilege())
