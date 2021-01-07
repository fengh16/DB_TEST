# -*- coding: utf-8 -*-
# python 3
from vars import user_list, user_password_check, global_user_privilege, db_privileges, db

from socket import socket
from typing import List, Dict
import time


# Interface Class (socket to Java procedure)
class Interface(object):
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.DEBUG = True
        self.buffer_size = 1024
        self.row_sep = '\n'
        self.col_sep = ';'
        self.system_dbs = set(['information_schema', 'performance_schema', 'mysql', 'my_blob'])

    def send_and_recv(self, send_info: str) -> str:
        client = socket()
        client.connect((self.host, self.port))
        if self.DEBUG:
            print('Send info: {}'.format(send_info))
        client.send(send_info.encode('utf-8'))
        res = ''
        res += client.recv(self.buffer_size).decode('utf-8')
        while not res.endswith('END'):
            res += client.recv(self.buffer_size).decode('utf-8')
        res = res[:-3]
        if self.DEBUG:
            print('Recv info: {}'.format(res))
        return res

    def get_logs(self, ins_id: int=0) -> str:
        send_info = self.col_sep.join(['1', str(ins_id)])
        recv_info = self.send_and_recv(send_info)
        return recv_info

    def ident_auth(self, username: str, password: str, ins_id: int=0) -> bool:
        send_info = self.col_sep.join(['2', username, password, str(ins_id)])
        recv_info = self.send_and_recv(send_info)
        return (len(recv_info) > 0) and (recv_info[0] == '1')

    def get_users_list(self, username: str, ins_id: int=0) -> List[str]:
        send_info = self.col_sep.join(['3', username, str(ins_id)])
        recv_info = self.send_and_recv(send_info)
        recv_info = recv_info.strip().split(self.col_sep)
        return [_ for _ in recv_info if len(_) > 0]

    def get_dbs_list(self, username: str, ins_id: int=0, b_sys: bool=False) -> List[str]:
        send_info = self.col_sep.join(['4', username, str(ins_id)])
        recv_info = self.send_and_recv(send_info)
        recv_info = recv_info.strip().split(self.col_sep)
        if b_sys: # Contain system databases
            return [_ for _ in recv_info if len(_) > 0]
        else: # Omit system databases
            return [_ for _ in recv_info if len(_) > 0 and _ not in self.system_dbs]

    def get_tables_list(self, username: str, dbname: str, ins_id: int=0) -> List[str]:
        send_info = self.col_sep.join(['5', username, dbname, str(ins_id)])
        recv_info = self.send_and_recv(send_info)
        recv_info = recv_info.strip().split(self.col_sep)
        return [_ for _ in recv_info if len(_) > 0 and _ != 'bigdata']

    def get_table_count(self, username: str, dbname: str, tablename: str, ins_id: int=0) -> int:
        send_info = self.col_sep.join(['6', username, dbname, tablename, str(ins_id)])
        recv_info = self.send_and_recv(send_info)
        recv_info = recv_info.strip()
        ans = -1
        try:
            ans = int(recv_info)
        except ValueError:
            pass
        return ans

    def get_user_priv(self, username: str, ins_id: int=0) -> List:
        '''
        [ ... , ...]
        '''
        send_info = self.col_sep.join(['7', username, str(ins_id)])
        recv_info = self.send_and_recv(send_info)
        recv_info = recv_info.strip().split(self.col_sep)
        ans = [_ for _ in recv_info if len(_.strip()) > 0]
        return ans

    def grant_priv(self, username: str, privilege: str, b_dblevel: bool, dbname: str, ins_id: int=0) -> bool:
        send_info = self.col_sep.join(['8', username, privilege, '1' if b_dblevel else '0', dbname, str(ins_id)])
        recv_info = self.send_and_recv(send_info)
        recv_info = recv_info.strip()
        return (len(recv_info) > 0) and (recv_info[0] == '1')

    def revoke_priv(self, username: str, privilege: str, b_dblevel: bool, dbname: str, ins_id: int=0) -> bool:
        send_info = self.col_sep.join(['9', username, privilege, '1' if b_dblevel else '0', dbname, str(ins_id)])
        recv_info = self.send_and_recv(send_info)
        recv_info = recv_info.strip()
        return (len(recv_info) > 0) and (recv_info[0] == '1')

    def create_db(self, username: str, dbname: str, ins_id: int=0) -> bool:
        send_info = self.col_sep.join(['10', username, dbname, str(ins_id)])
        recv_info = self.send_and_recv(send_info)
        recv_info = recv_info.strip()
        return (len(recv_info) > 0) and (recv_info[0] == '1')

    def create_table(self, username: str, dbname: str, tablename: str, ins_id: int=0) -> bool:
        send_info = self.col_sep.join(['11', username, dbname, tablename, str(ins_id)])
        recv_info = self.send_and_recv(send_info)
        recv_info = recv_info.strip()
        return (len(recv_info) > 0) and (recv_info[0] == '1')

    def get_table_schema(self, username: str, dbname: str, tablename: str, ins_id: int=0, encrypt_alg: str='') -> Dict:
        '''
        { 'Field': [], 'Type': [], 'Key': [] }
        '''
        send_info = self.col_sep.join(['12', username, dbname, tablename, str(ins_id), encrypt_alg])
        recv_info = self.send_and_recv(send_info)
        recv_info = recv_info.strip().split(self.row_sep)
        if len(recv_info) < 2:
            return {}
        if len(recv_info) == 2:
            res = {
                'Field': recv_info[0].strip().split(self.col_sep),
                'Type': recv_info[1].strip().split(self.col_sep)
            }
            res['Key'] = ['' for _ in range(len(res['Field']))]
            return res
        return {
            'Field': recv_info[0].strip().split(self.col_sep),
            'Type': recv_info[1].strip().split(self.col_sep),
            'Key': recv_info[2].strip().split(self.col_sep)
        }

    def insert_data(self, username: str, dbname: str, tablename: str, ins_id: int=0) -> bool:
        send_info = self.col_sep.join(['13', username, dbname, tablename, str(ins_id)])
        recv_info = self.send_and_recv(send_info)
        recv_info = recv_info.strip()
        return (len(recv_info) > 0) and (recv_info[0] == '1')

    def update_data(self, username: str, dbname: str, tablename: str, ins_id: int=0) -> bool:
        send_info = self.col_sep.join(['14', username, dbname, tablename, str(ins_id)])
        recv_info = self.send_and_recv(send_info)
        recv_info = recv_info.strip()
        return (len(recv_info) > 0) and (recv_info[0] == '1')

    def delete_data(self, username: str, dbname: str, tablename: str, ins_id: int=0) -> bool:
        send_info = self.col_sep.join(['15', username, dbname, tablename, str(ins_id)])
        recv_info = self.send_and_recv(send_info)
        recv_info = recv_info.strip()
        return (len(recv_info) > 0) and (recv_info[0] == '1')

    def get_table_data(self, username: str, dbname: str, tablename: str, ins_id: int=0, encrypt_alg: str='') -> List:
        '''
        [ [row0_list], ...]
        '''
        send_info = self.col_sep.join(['16', username, dbname, tablename, str(ins_id), encrypt_alg])
        recv_info = self.send_and_recv(send_info)
        recv_info = recv_info.strip().split(self.row_sep)
        return [_.strip().split(self.col_sep) for _ in recv_info]

    def embed_table_data(self, username: str, dbname: str, tablename: str, embed_info: str, ins_id: int=0, encrypt_alg: str='') -> str:
        '''
        [ [row0_list], ...]
        '''
        send_info = self.col_sep.join(['17', username, dbname, tablename, str(ins_id), embed_info, encrypt_alg])
        recv_info = self.send_and_recv(send_info)
        recv_info = recv_info.strip().split(self.row_sep)
        return [_.strip().split(self.col_sep) for _ in recv_info]

    def drop_table(self, username: str, dbname: str, tablename: str, ins_id: int=0) -> bool:
        send_info = self.col_sep.join(['18', username, dbname, tablename, str(ins_id)])
        recv_info = self.send_and_recv(send_info)
        recv_info = recv_info.strip()
        return (len(recv_info) > 0) and (recv_info[0] == '1')

    def drop_db(self, username: str, dbname: str, ins_id: int=0) -> bool:
        send_info = self.col_sep.join(['19', username, dbname, str(ins_id)])
        recv_info = self.send_and_recv(send_info)
        recv_info = recv_info.strip()
        return (len(recv_info) > 0) and (recv_info[0] == '1')

    def drop_user(self, username: str, ins_id: int=0) -> bool:
        send_info = self.col_sep.join(['20', username, str(ins_id)])
        recv_info = self.send_and_recv(send_info)
        recv_info = recv_info.strip()
        return (len(recv_info) > 0) and (recv_info[0] == '1')

    def import_data(self, username: str, dbname: str, tablename: str, ins_id: int=0, b_shell: bool=False) -> bool:
        send_info = self.col_sep.join(['21', username, dbname, tablename, str(ins_id), '1' if b_shell else '0'])
        recv_info = self.send_and_recv(send_info)
        recv_info = recv_info.strip()
        return (len(recv_info) > 0) and (recv_info[0] == '1')

    def export_data(self, username: str, dbname: str, tablename: str, filename: str, ins_id: int=0, b_shell: bool=False) -> bool:
        send_info = self.col_sep.join(['22', username, dbname, tablename, filename, str(ins_id), '1' if b_shell else '0'])
        recv_info = self.send_and_recv(send_info)
        recv_info = recv_info.strip()
        return (len(recv_info) > 0) and (recv_info[0] == '1')

    def export_schema(self, username: str, dbname: str, tablename: str, filename: str, ins_id: int=0) -> bool:
        send_info = self.col_sep.join(['23', username, dbname, tablename, filename, str(ins_id)])
        recv_info = self.send_and_recv(send_info)
        recv_info = recv_info.strip()
        return (len(recv_info) > 0) and (recv_info[0] == '1')

    def file_content(self, username: str, filename: str) -> str:
        send_info = self.col_sep.join(['24', username, filename])
        recv_info = self.send_and_recv(send_info)
        recv_info = recv_info.strip()
        return recv_info


# Operation Class
class Operation(object):
    def __init__(self, host, port):
        self.interface = Interface(host, port)
        self.admin_user = 'root'

    def get_users_list(self, ins_id: int=0) -> List[str]:
        '''
        获取用户列表，默认是 实例0
        @return    res: [user_0, ...]
        '''
        return self.interface.get_users_list(self.admin_user, ins_id)

    def get_users_privilege(self, ins_id: int=0) -> List[Dict]:
        '''
        获取所有用户的权限，默认是 实例0
        @return    two dicts, [db privileges, table privileges]
        db: {
            create: { user_0: True/False, user_1: T/F, ... },
            access: { ... },
            drop: { ... }
        }
        table: {
            db_0: {
                create: { user_0: True/False, user_1: T/F, ... },
                modify: { user_0: ... },
                access: { ... },
                drop: { ... }
            },
            db_1: ...
        }
        '''
        ## name map
        db_priv_map = {
            'create': '创建数据库权限',
            'access': '访问数据库权限',
            'drop': '删除数据库权限'
        }
        tbl_priv_map = {
            'create': '创建表权限',
            'modify': '修改表权限',
            'access': '查看表权限',
            'drop': '删除表权限'
        }
        ## db privilege
        ans_db = dict()
        ans_db[db_priv_map['create']] = dict()
        ans_db[db_priv_map['access']] = dict()
        ans_db[db_priv_map['drop']] = dict()
        ul = self.get_users_list(ins_id)
        for _ in ul:
            ans_db[db_priv_map['create']][_] = False
            ans_db[db_priv_map['drop']][_] = False
        # user -> db set
        u_db_set = dict()
        for one_user in ul:
            u_db_set[one_user] = set()
            # need to login
            b_auth = self.interface.ident_auth(one_user, user_password_check[one_user], ins_id)
            if not b_auth:
                print('{} login failed.'.format(one_user))
                continue
            udb_list = self.interface.get_dbs_list(one_user, ins_id)
            for _ in udb_list:
                if len(_) > 0:
                    u_db_set[one_user].add(_)
            if len(u_db_set[one_user]) > 0:
                ans_db[db_priv_map['access']][one_user] = True
        # user -> privileges list
        u_priv_list = dict()
        for one_user in ul:
            u_priv_list[one_user] = self.interface.get_user_priv(one_user, ins_id)
            for _ in u_priv_list[one_user]:
                if '*.*' in _ and 'ALL' in _:
                    ans_db[db_priv_map['create']][one_user] = True
                    ans_db[db_priv_map['drop']][one_user] = True
                    break
                if '*.*' in _ and 'CREATE' in _:
                    ans_db[db_priv_map['create']][one_user] = True
                if '*.*' in _ and 'DROP' in _:
                    ans_db[db_priv_map['drop']][one_user] = True
        ## table privilege
        ans_table = dict()
        dbl = self.interface.get_dbs_list(self.admin_user, ins_id)
        for one_db in dbl:
            ans_table[one_db] = dict()
            ans_table[one_db][tbl_priv_map['create']] = dict()
            ans_table[one_db][tbl_priv_map['modify']] = dict()
            ans_table[one_db][tbl_priv_map['access']] = dict()
            ans_table[one_db][tbl_priv_map['drop']] = dict()
            # init
            for one_user in ul:
                ans_table[one_db][tbl_priv_map['create']][one_user] = False
                ans_table[one_db][tbl_priv_map['modify']][one_user] = False
                ans_table[one_db][tbl_priv_map['access']][one_user] = False
                ans_table[one_db][tbl_priv_map['drop']][one_user] = False
        # access, u_db_set
        for one_user in ul:
            for u_db in u_db_set[one_user]:
                ans_table[u_db][tbl_priv_map['access']][one_user] = True
        # other privs
        for one_user in ul:
            b_special = False
            for one_priv in u_priv_list[one_user]:
                if ('*.*' in one_priv) and ('ALL' in one_priv):
                    b_special = True
                    break
                for one_db in dbl:
                    if 'CREATE' in one_priv and \
                    ((one_db in one_priv and '.*' in one_priv) or ('*.*' in one_priv)):
                        ans_table[one_db][tbl_priv_map['create']][one_user] = True
                    if 'UPDATE' in one_priv and 'DELETE' in one_priv and \
                    ((one_db in one_priv and '.*' in one_priv) or ('*.*' in one_priv)):
                        ans_table[one_db][tbl_priv_map['modify']][one_user] = True
                    if 'DROP' in one_priv and \
                    ((one_db in one_priv and '.*' in one_priv) or ('*.*' in one_priv)):
                        ans_table[one_db][tbl_priv_map['drop']][one_user] = True
            if b_special:
                for one_db in dbl:
                    ans_table[one_db][tbl_priv_map['create']][one_user] = True
                    ans_table[one_db][tbl_priv_map['modify']][one_user] = True
                    ans_table[one_db][tbl_priv_map['access']][one_user] = True
                    ans_table[one_db][tbl_priv_map['drop']][one_user] = True
        return [ans_db, ans_table]

    def refresh_table(self, user: str, dbname: str, tablename: str, ins_id: int=0):
        key_map = {
            'PRI': 'primary key',
            'MUL': 'foreign key',
            '': ''
        }
        table = {
            'schema': [],
            'rows': []
        }
        _tbl_schema = self.interface.get_table_schema(user, dbname, tablename, ins_id)
        if len(_tbl_schema) == 0:
            return table
        _schema_len = len(_tbl_schema['Field'])
        table['schema'] = [{
            'name': _tbl_schema['Field'][_],
            'type': _tbl_schema['Type'][_],
            'constraint': key_map[_tbl_schema['Key'][_]]
            }
            for _ in range(_schema_len)
        ]
        _tbl_rows = self.interface.get_table_data(user, dbname, tablename, ins_id)
        # if dbname == 'deve_x':
        #     print(user, dbname, tablename, ins_id)
        #     print(_tbl_rows)
        #     input()
        _rows_len = len(_tbl_rows)
        if _rows_len == 0:
            table['rows'] = []
            return table
        __row_col = len(_tbl_rows[0])
        if __row_col != _schema_len:
            table['rows'] = []
            return table
        table['rows'] = [
            {
                _tbl_schema['Field'][_]: _tbl_rows[__][_]
                for _ in range(_schema_len)
            }
            for __ in range(_rows_len)
        ]
        return table

    def get_dbs_content(self, user: str='root') -> Dict:
        '''
        获取数据库所有内容，默认是 root 用户所能访问的 实例 0 和 1 的数据，即所有数据
        @return    db = {
            0 (ins): {
                db_list: [ ... ],
                db_0: {
                    table_list: [ ... ],
                    table_0: {
                        schema: [ { name: .., type: .., constraint: .. }, { ... } ],
                        rows: [ { field_0: .., field_1: .., .. }, { ... } ]
                    },
                    ...
                },
                ...
            },
            1 (ins): ...
        }
        '''
        self.interface.ident_auth(user, user_password_check[user], 0)
        self.interface.ident_auth(user, user_password_check[user], 1)
        ans = dict()
        def get_one_db_content(user: str, ins_id: int) -> Dict:
            res = dict()
            dbl = self.interface.get_dbs_list(user, ins_id)
            res['db_list'] = dbl
            key_map = {
                'PRI': 'primary key',
                'MUL': 'foreign key',
                '': ''
            }
            for one_db in dbl:
                res[one_db] = dict()
                tbl_list = self.interface.get_tables_list(user, one_db, ins_id)
                res[one_db]['table_list'] = tbl_list
                for one_tbl in tbl_list:
                    res[one_db][one_tbl] = self.refresh_table(user, one_db, one_tbl, ins_id)
                    # res[one_db][one_tbl] = dict()
                    # _tbl_schema = self.interface.get_table_schema(user, one_db, one_tbl, ins_id)
                    # if len(_tbl_schema) == 0:
                    #     res[one_db][one_tbl]['schema'] = []
                    #     res[one_db][one_tbl]['rows'] = []
                    #     continue
                    # _schema_len = len(_tbl_schema['Field'])
                    # res[one_db][one_tbl]['schema'] = [{
                    #     'name': _tbl_schema['Field'][_],
                    #     'type': _tbl_schema['Type'][_],
                    #     'constraint': key_map[_tbl_schema['Key'][_]]
                    #     }
                    #     for _ in range(_schema_len)
                    # ]
                    # _tbl_rows = self.interface.get_table_data(user, one_db, one_tbl, ins_id)
                    # _rows_len = len(_tbl_rows)
                    # if _rows_len == 0:
                    #     res[one_db][one_tbl]['rows'] = []
                    #     continue
                    # __row_col = len(_tbl_rows[0])
                    # if __row_col != _schema_len:
                    #     res[one_db][one_tbl]['rows'] = []
                    #     continue
                    # res[one_db][one_tbl]['rows'] = [
                    #     {
                    #         _tbl_schema['Field'][_]: _tbl_rows[__][_]
                    #         for _ in range(_schema_len)
                    #     }
                    #     for __ in range(_rows_len)
                    # ]
            return res
        ans[0] = get_one_db_content(user, 0)
        ans[1] = get_one_db_content(user, 1)
        return ans

    def init(self):
        '''
        初始化 back/views 中用到的全局变量
        TODO
        '''
        self.get_users_list()
        self.get_users_privilege()
        self.get_dbs_content()


# Test Class
class Test(object):
    def __init__(self):
        host = '166.111.80.113'
        port = 9999
        self.interface = Interface(host, port)
        self.operation = Operation(host, port)
        # self.users = ['root', 'developer_1', 'developer_2', 'developer_3', 'developer_4']
        # self.passw = ['toor', 'pass_1', 'pass_2', 'pass_3', 'pass_4']
        self.users = ['root', 'developer_1', 'developer_2']
        self.passw = ['toor', 'pass_1', 'pass_2']

    def get_timestamp(self) -> str:
        return str(int(time.time()))

    def test_interface(self):
        num_users = len(self.users)
        for _ in range(num_users):
            one_user = self.users[_]
            one_pass = self.passw[_]
            print('Test user: {}'.format(one_user))
            print('Identity authentication: {}'.format(
                self.interface.ident_auth(one_user, one_pass)
            ))
            print('Users List: {}'.format(
                self.interface.get_users_list(one_user)
            ))
            print('Databases List: {}'.format(
                self.interface.get_dbs_list(one_user)
            ))
            print('Tables List: {}'.format(
                self.interface.get_tables_list(one_user, 'test')
            ))
            print('test.user Table Count: {}'.format(
                self.interface.get_table_count(one_user, 'test', 'user')
            ))
            print('User Privileges: {}'.format(
                self.interface.get_user_priv(one_user)
            ))
            print('Grant User Privileges: {}'.format(
                self.interface.grant_priv(one_user, 'create', False, 'deve_x')
            ))
            print('Revoke User Privileges: {}'.format(
                self.interface.revoke_priv(one_user, 'create', False, 'deve_x')
            ))
            self.interface.grant_priv(one_user, 'create', False, 'deve_x')
            print('Create Database: {}'.format(
                self.interface.create_db(one_user, 'deve_x')
            ))
            print('Databases List: {}'.format(
                self.interface.get_dbs_list(one_user)
            ))
            print('Create Table: {}'.format(
                self.interface.create_table(one_user, 'deve_x', 'tbl_x')
            ))
            print('Tables List: {}'.format(
                self.interface.get_tables_list(one_user, 'deve_x')
            ))
            print('Get Table Schema: {}'.format(
                self.interface.get_table_schema(one_user, 'deve_x', 'tbl_x')
            ))
            print('Import Data: {}'.format(
                self.interface.import_data(one_user, 'deve_x', 'tbl_x')
            ))
            print('deve_x.tbl_x Table Count: {}'.format(
                self.interface.get_table_count(one_user, 'deve_x', 'tbl_x')
            ))
            print('Export Schema: {}'.format(
                self.interface.export_schema(one_user, 'deve_x', 'tbl_x', 'tbl_x.ddl')
            ))
            print('Get Table Data: {}'.format(
                self.interface.get_table_data(one_user, 'deve_x', 'tbl_x')
            ))
            # Embed, high overhead
            print('Get Embed Table Data: {}'.format(
                self.interface.embed_table_data(one_user, 'deve_x', 'tbl_x', 'embed')
            ))
            print('Insert Data: {}'.format(
                self.interface.insert_data(one_user, 'deve_x', 'tbl_x')
            ))
            print('deve_x.tbl_x Table Count: {}'.format(
                self.interface.get_table_count(one_user, 'deve_x', 'tbl_x')
            ))
            print('Update Data: {}'.format(
                self.interface.update_data(one_user, 'deve_x', 'tbl_x')
            ))
            print('deve_x.tbl_x Table Count: {}'.format(
                self.interface.get_table_count(one_user, 'deve_x', 'tbl_x')
            ))
            print('Delete Data: {}'.format(
                self.interface.delete_data(one_user, 'deve_x', 'tbl_x')
            ))
            print('deve_x.tbl_x Table Count: {}'.format(
                self.interface.get_table_count(one_user, 'deve_x', 'tbl_x')
            ))
            print('Export Data: {}'.format(
                self.interface.export_data(one_user, 'deve_x', 'tbl_x', 'tbl_x.sql')
            ))
            print('Get File Content: {}'.format(
                self.interface.file_content(one_user, 'tbl_x.ddl')
            ))
            print('Drop table: {}'.format(
                self.interface.drop_table(one_user, 'deve_x', 'tbl_x')
            ))
            print('Drop Database: {}'.format(
                self.interface.drop_db(one_user, 'deve_x')
            ))
            print('=' * 30)
        # TODO: root Drop User

    def test_operation(self, user):
        print('Instance 0 User List: {}'.format(
            self.operation.get_users_list()
        ))
        print('Instance 1 User List: {}'.format(
            self.operation.get_users_list(1)
        ))
        print('Instance 0 User Privilege: {}'.format(
            self.operation.get_users_privilege()
        ))
        print('Instance 1 User Privilege: {}'.format(
            self.operation.get_users_privilege(1)
        ))
        print('Database Content: {}'.format(
            self.operation.get_dbs_content(user)
        ))

    def test_all(self):
        # print('=' * 10 + ' Interface Class Test ' + '=' * 10)
        # self.test_interface()
        print('=' * 10 + ' Operation Class Test ' + '=' * 10)
        user = 'root'
        self.test_operation(user)


def main():
    test = Test()
    test.test_all()


if __name__ == '__main__':
    main()
