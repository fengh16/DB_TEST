# -*- coding: utf-8 -*-

# global databases:
# develop_xx ...
# test
# tpch
# IGNORE: inofrmation_schema, performance_schema, mysql, my_blob

# CHECK db privileges
# create: create database to test
# access: show databases to test
# drop: all *.*/[db].* ; drop *.*/[db].* ; drop database to test

# CHECK table privileges
# create: create table to test
# modify: delete & update table to test
# access: show tables to test
# drop: all *.*/[db].*/[db].[table] ; update [db].*/[db].[table]

# global variables
user_list = [
    'administrator',
    'developer1',
    'developer2',
    'developer3',
    'developer4',
    'root'
]

user_password_check = {
    'administrator': 'administrator',
    'developer_1': 'pass_1',
    'developer_2': 'pass_2',
    'developer_3': 'pass_3',
    'developer_4': 'pass_4',
    'root': 'toor'
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
