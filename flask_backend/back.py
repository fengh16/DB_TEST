
from flask import Flask, request, make_response
from flask_cors import *
import operations as op
import time

app = Flask(__name__)
app.debug = True

operation = op.Operation('166.111.80.113', 9999)
#operation = None

user_list = [
    'root',
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
    'table4.sql'
}

logs = []

tformat='%Y-%m-%d %H:%M:%S'
def logto(s):
    logs.insert(0, f'[{time.strftime(tformat, time.localtime(time.time()))}] {s}')


def prepare():
    global user_list, user_password_check, global_user_privilege, db_privileges, db
    user_list = operation.get_users_list()
    user_password_check = {
        user: user for user in user_list
    }
    global_user_privilege, db_privileges = operation.get_users_privilege()
    db = operation.get_dbs_content('root')


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


def format_schema(raw_schema):
    if len(raw_schema) == 0:
        return []
    key_map = {
        'PRI': 'primary key',
        'MUL': 'foreign key',
        '': ''
    }
    schema_len = len(raw_schema['Field'])
    schema = [{
        'name': raw_schema['Field'][i],
        'type': raw_schema['Type'][i],
        'constraint': key_map[raw_schema['Key'][i]]
        }
        for i in range(schema_len)
    ]
    return schema


def format_table(instance_id, db_name, table_name, rows):
    schema = db[instance_id][db_name][table_name]['schema']
    
    table_rows = [{
        schema[c]['name']: rows[r][c] for c in range(len(rows[0]))
    } for r in range(len(rows))]

    return table_rows


# platform
@app.route('/change-user/', methods=['POST'])
@cross_origin()
def change_user():
    username = request.json['username']
    password = request.json['password']
    login_success = username in user_list
    if login_success:
        response = {
            'success': True,
            'result': '登录成功',
            'usertype': '管理员' if is_admin(username) else '普通用户'
        }
        logto(f'change to user {username}')
    else:
        response = {
            'success': True,
            'result': '登录失败',
            'usertype': '管理员' if is_admin else '普通用户'
        }
        logto(f'change user {username} failed: not in user list')
    return make_response(response)


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
        logto(f'user {username} login')
    else:
        response = {
            'success': True,
            'result': '登录失败',
            'usertype': '管理员' if is_admin else '普通用户'
        }
        logto(f'user {username} login failed')
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
    logto(f'user {username} authenticate {auth_success}')
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
    logto(f'get user list {user_list}')
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
    logto(f'get user privileges')
    print(response)
    return make_response(response, 200)


@app.route('/<string:dbtype>/update-user-privilege-list/', methods=['POST'])
@cross_origin()
def update_user_privilege_list(dbtype):
    global global_user_privilege, db_privileges
    username = request.json['username']
    request_success = username in user_list and is_admin(username)
    privilege_map = {
        '创建': 'create',
        '访问': 'select',
        '删除': 'drop'
    }
    if request_success:
        grant_units = []
        revoke_units = []
        new_privilege_list = request.json['privilege']
        print('old: ')
        print(global_user_privilege)
        print('new: ')
        print(new_privilege_list[0])

        new_global_user_privilege = {
            child['title']: child['granted'] for child in new_privilege_list[0]['children']
        }
        # print(new_privilege_list)
        for title in new_global_user_privilege:
            for username in user_list:
                # 创建, root, True
                old_state = global_user_privilege[title][username]
                new_state = new_global_user_privilege[title][username]
                if old_state and not new_state:
                    revoke_units.append((username, privilege_map[title[:2]], ''))
                elif not old_state and new_state:
                    grant_units.append((username, privilege_map[title[:2]], ''))

        print('Grant: ', grant_units)
        print('Revoke: ', revoke_units)
        for grant in grant_units:
            username, privilege, dbname = grant
            ins_id = 0
            operation.interface.grant_priv(username, privilege, True, dbname, ins_id)
            logto(f'grant privilege {privilege} on {dbname} to {user}')
        for revoke in revoke_units:
            username, privilege, dbname = revoke
            ins_id = 0
            operation.interface.revoke_priv(username, privilege, True, dbname, ins_id)
            logto(f'revoke privilege {privilege} on {dbname} from {user}')
        
        global_user_privilege = new_global_user_privilege
        db_privileges = new_privilege_list[1:] if len(new_privilege_list) > 1 else db_privileges
    response = {
        'success': request_success,
        'result': '更新成功' if request_success else '更新失败'
    }
    return make_response(response, 200)


@app.route('/<string:dbtype>/create-database/', methods=['POST'])
@cross_origin()
def create_database(dbtype):
    global db, global_user_privilege, db_privileges
    db_name = request.json['databaseName']
    username = request.json['username']
    instance_id = int(request.json['instanceId'])
    request_success = have_db_privilege(username, instance_id, 'C')
    if request_success:
        create_success = operation.interface.create_db(username, db_name, instance_id)
        if create_success:
            db = operation.get_dbs_content('root')
            global_user_privilege, db_privileges = operation.get_users_privilege()
        response = {
            'success': create_success,
            'result': '创建成功' if create_success else '创建失败',
            'msg': '' if create_success else '数据库已经存在'
        }
        logto(f'create database {db_name}')
    else:
        response = {
            'success': False,
            'result': '没有权限'
        }
        logto(f'fail to create database {db_name}: unauthenticated')
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
    logto(f'get database list')
    return make_response(response, 200)


@app.route('/<string:dbtype>/list-table/', methods=['GET'])
@cross_origin()
def list_table(dbtype):
    global db
    username = request.args.get('username', '')
    instance_id = int(request.args.get('instanceId', 0))
    database_name = request.args.get('databaseName', '')
    authed = global_user_privilege['访问数据库权限'][username]
    request_success = username in user_list and authed and instance_id in [0, 1] and database_name in db[instance_id]['db_list']
    table_list = db[instance_id][database_name]['table_list']
    
    if authed:
        response = {
            'success': request_success,
            'result': table_list if request_success else [],
            'msg': '' if request_success else '输入参数有误'
        }
        logto(f'get table list of database {database_name}')
    else:
        response = {
            'success': False,
            'result': [],
            'msg': '没有权限'
        }
        logto(f'fail to get table list of database {database_name}: unauthenticated')
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
        create_success = create_success and operation.interface.create_table(username, db_name, table_name, instance_id)
        if create_success:
            # db[instance_id][db_name]['table_list'].append(table_name)
            # db[instance_id][db_name][table_name] = {}
            db = operation.get_dbs_content('root')
        response = {
            'success': create_success,
            'result': '创建成功' if create_success else '已经存在'
        }
        logto(f'create table {db_name}.{table_name}')
    else:
        response = {
            'success': False,
            'result': '没有权限'
        }
        logto(f'fail to create table {db_name}.{table_name}')
    return make_response(response, 200)


# 10. 查看表信息
@app.route('/<string:dbtype>/view-table-schema/', methods=['GET'])
@cross_origin()
def view_table_schema(dbtype):
    username = request.args.get('username', '')
    instance_id = int(request.args.get('instanceId', '0'))
    db_name = request.args.get('databaseName', '')
    table_name = request.args.get('tableName', '')
    encrypt_method = request.args.get('encrypted', '')
    if db_name not in db[instance_id]:
        response = {
            'success': False,
            'result': {},
            'msg': '该数据库不存在'
        }
        logto(f'fail to get schema of {db_name}.{table_name}: database does not exist')
    elif table_name not in db[instance_id][db_name]:
        response = {
            'success': False,
            'result': {},
            'msg': '该表不存在'
        }
        logto(f'fail to get schema of {db_name}.{table_name}: table does not exist')
    else:
        print(username, instance_id, db_name)
        request_success = have_table_privilege(username, instance_id, db_name, 'R')
        if request_success:
            if encrypt_method == '':
                schema = db[instance_id][db_name][table_name]['schema']
            else:
                schema = operation.interface.get_table_schema(username, db_name, table_name, instance_id, encrypt_method)
                schema = format_schema(schema)
            response = {
                'success': True,
                'result': {
                    'tableName': table_name,
                    'schema': [{
                        'id': i,
                        'columnName': column['name'],
                        'columnType': column['type'],
                        'columnConstraint': column['constraint']
                    } for i, column in enumerate(schema)]
                }
            }
            logto(f'get schema of {db_name}.{table_name}')
        else:
            response = {
                'success': False,
                'result': {},
                'msg': '没有权限'
            }
            logto(f'fail to get schema of {db_name}.{table_name}: unauthenticated')
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
        insert_success = insert_success & operation.interface.insert_data(username, db_name, table_name, instance_id)
        if insert_success:
            db[instance_id][db_name][table_name] = operation.refresh_table(username, db_name, table_name, instance_id)
        response = {
            'success': insert_success,
            'result': '插入成功' if insert_success else '不存在该表'
        }
        if insert_success:
            logto(f'insert into {db_name}.{table_name}')
        else:
            logto(f'fail to insert into {db_name}.{table_name}: table does not exist')
    else:
        response = {
            'success': False,
            'result': '没有权限'
        }
        logto(f'fail to insert into {db_name}.{table_name}: unauthenticated')
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
        update_success = update_success and operation.interface.update_data(username, db_name, table_name, instance_id)
        if update_success:
            db[instance_id][db_name][table_name] = operation.refresh_table(username, db_name, table_name, instance_id)
        response = {
            'success': update_success,
            'result': '更新成功' if update_success else '不存在该表'
        }
        if update_success:
            logto(f'update {db_name}.{table_name}')
        else:
            logto(f'fail to update {db_name}.{table_name}: table does not exist')
    else:
        response = {
            'success': False,
            'result': '没有权限'
        }
        logto(f'fail to update {db_name}.{table_name}: unauthenticated')
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
        delete_success = delete_success and operation.interface.delete_data(username, db_name, table_name, instance_id)
        db[instance_id][db_name][table_name] = operation.refresh_table(username, db_name, table_name, instance_id)
        response = {
            'success': delete_success,
            'result': '删除成功' if delete_success else '不存在该表'
        }
        if delete_success:
            logto(f'delete from {db_name}.{table_name}')
        else:
            logto(f'fail to delete from {db_name}.{table_name}: table does not exist')
    else:
        response = {
            'success': False,
            'result': '没有权限'
        }
        logto(f'fail to delete from {db_name}.{table_name}: unauthenticated')
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
    encrypt_method = request.args.get('encrypted', '')
    if db_name not in db[instance_id]:
        response = {
            'success': False,
            'result': [],
            'msg': '该数据库不存在'
        }
        logto(f'fail to get table data {db_name}.{table_name}: database does not exist')
    elif table_name not in db[instance_id][db_name]['table_list']:
        response = {
            'success': False,
            'result': [],
            'msg': '该表不存在'
        }
        logto(f'fail to get table data {db_name}.{table_name}: table does not exist')
    else:
        authed = have_table_privilege(username, instance_id, db_name, 'R')
        if authed:
            if encrypt_method == '':
                rows = db[instance_id][db_name][table_name]['rows']
                print(rows)
                response = {
                    'success': True,
                    'result': rows
                }
                logto(f'get table data {db_name}.{table_name}')
            else:
                rows = operation.interface.get_table_data(username, db_name, table_name, instance_id, encrypt_method)
                response = {
                    'success': True,
                    'result': format_table(instance_id, db_name, table_name, rows)
                }
                logto(f'get table data {db_name}.{table_name} encrypted using {encrypt_method}')
            # for i, row in enumerate(rows):
            #     if encrypt_method == '':
            #         new_row = {column_name: value for (column_name, value) in row.items()}
            #     else:
            #         new_row = {column_name: '[enc]' + value for (column_name, value) in row.items()}
            #     new_row['id'] = i
            #     response['result'].append(new_row)
        else:
            response = {
                'success': False,
                'result': [],
                'msg': '没有权限'
            }
            logto(f'fail to get table data {db_name}.{table_name}: unauthenticated')
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
            rows = operation.interface.embed_table_data(username, db_name, table_name, embedding, instance_id, encrypt_method)
            table_rows = format_table(instance_id, db_name, table_name, rows)
            response = {
                'success': True,
                'result': table_rows
            }
            logto(f'get table data {db_name}.{table_name} embedded {embedding}')
            print(response)
        else:
            response = {
                'success': False,
                'result': []
            }
            logto(f'fail to get table data {db_name}.{table_name} embedded {embedding}')
    else:
        response = {
            'success': False,
            'result': []
        }
        logto(f'fail to get table data {db_name}.{table_name} embedded {embedding}')
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
        logto(f'fail to drop table {db_name}.{table_name}: database does not exist')
    elif table_name not in db[instance_id][db_name]['table_list']:
        response = {
            'success': False,
            'result': [],
            'msg': '该表不存在'
        }
        logto(f'fail to drop table {db_name}.{table_name}: table does not exist')
    else:
        authed = have_table_privilege(username, instance_id, db_name, 'D')
        if authed:
            drop_success = operation.interface.drop_table(username, db_name, table_name, instance_id)
            if drop_success:
                db = operation.get_dbs_content('root')
            
                response = {
                    'success': True,
                    'result': '',
                    'msg': ''
                }
                logto(f'drop table {db_name}.{table_name}')
            else:
                response = {
                    'success': False,
                    'result': '',
                    'msg': '格式错误'
                }
                logto(f'fail to drop table {db_name}.{table_name}: error occurs')
        else:
            response = {
                'success': False,
                'result': '删除失败',
                'msg': '没有权限'
            }
            logto(f'fail to drop table {db_name}.{table_name}: unauthenticated')
    return make_response(response, 200)


# 17. 删除数据库
@app.route('/<string:dbtype>/drop-database/', methods=['POST'])
@cross_origin()
def drop_database(dbtype):
    global db
    username = request.json['username']
    instance_id = int(request.json['instanceId'])
    db_name = request.json['databaseName']

    authed = have_db_privilege(username, instance_id, 'D')
    if authed:
        drop_success = operation.interface.drop_db(username, db_name, instance_id)
        if drop_success:
            db = operation.get_dbs_content('root')
        response = {
            'success': drop_success,
            'result': '删除成功' if drop_success else '删除失败',
            'msg': '' if drop_success else '数据库不存在'
        }
        if drop_success:
            logto(f'drop database {db_name}')
        else:
            logto(f'fail to drop database {db_name}: database does not exist')
    else:
        response = {
            'success': False,
            'result': '删除失败',
            'msg': '没有权限'
        }
        logto(f'fail to drop database {db_name}: unauthenticated')
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
            import_success = filename in existing_files and operation.interface.import_data(username, db_name, filename, instance_id, import_method == 'shell')
            if import_success:
                db[instance_id][db_name][table_name] = operation.refresh_table(username, db_name, table_name, instance_id)
                response = {
                    'success': True,
                    'result': '',
                    'msg': '导入成功'
                }
                logto(f'import from {filename} to {db_name}.{table_name}')
            elif filename not in existing_files:
                response = {
                    'success': False,
                    'result': '',
                    'msg': '文件不存在'
                }
                logto(f'fail to import from {filename} to {db_name}.{table_name}: file does not exist')
            else:
                response = {
                    'success': False,
                    'result': '',
                    'msg': '格式错误'
                }
                logto(f'fail to import from {filename} to {db_name}.{table_name}: error occurs')
        else:
            response = {
                'success': False,
                'result': '导入失败',
                'msg': '没有权限'
            }
            logto(f'fail to import from {filename} to {db_name}.{table_name}: unauthenticated')
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
        export_method = request.json['method']
        authed = have_table_privilege(username, instance_id, db_name, 'R')
        if authed:
            export_success = operation.interface.export_data(username, db_name, table_name, filename, instance_id, export_method == 'shell')
            if export_success:
                existing_files.add(filename)
                response = {
                    'success': True,
                    'result': '',
                    'msg': '导出成功'
                }
                logto(f'export from {db_name}.{table_name} to {filename}')
            else:
                response = {
                    'success': False,
                    'result': '',
                    'msg': '格式错误'
                }
                logto(f'fail to export from {db_name}.{table_name} to {filename}: error occurs')
        else:
            response = {
                'success': False,
                'result': '导出失败',
                'msg': '没有权限'
            }
            logto(f'fail to export from {db_name}.{table_name} to {filename}: authenticated')
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
    request_success = filename in existing_files
    if request_success:
        content = operation.interface.file_content(username, filename)
        response = {
            'success': True,
            'result': content,
            'msg': ''
        }
        logto(f'get content of {filename}')
    else:
        response = {
            'success': False,
            'result': '',
            'msg': '文件不存在'
        }
        logto(f'fail to get content of {filename}: file does not exist')
    return make_response(response, 200)


@app.route('/<string:dbtype>/log/', methods=['GET'])
@cross_origin()
def select_log(dbtype):
    username = request.args.get('username', '')
    logto(f'select recent logs')
    response = {
        'success': True,
        'result': logs[:10]
    }
    
    return make_response(response, 200)


@app.route('/<string:dbtype>/delete-file/', methods=['POST'])
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
        logto(f'delete file {filename}')
    else:
        response = {
            'success': False,
            'result': '',
            'msg': '文件不存在'
        }
        logto(f'fail to delte file {filename}: file does not exist')
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
        logto(f'reset password for user {username}')
    else:
        response = {
            'success': False,
            'result': '',
            'msg': '用户不存在'
        }
        logto(f'fail to reset password for user {username}: user does not exist')
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
