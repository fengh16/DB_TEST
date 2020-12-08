# -*- coding: utf-8 -*-
# python 3
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
        self.col_sep = ';'
        self.row_sep = '\n'

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

    def get_logs(self, ins_id: int=0) -> str:  #0
        send_info = self.col_sep.join(['0', str(ins_id)])
        recv_info = self.send_and_recv(send_info)
        return recv_info

    def login(self, username: str, password: str, ins_id: int=0) -> bool:  #1
        send_info = self.col_sep.join(['1', str(ins_id), username, password])
        recv_info = self.send_and_recv(send_info)
        return (len(recv_info) > 0) and (recv_info[0] == '1')

    def get_users_list(self, ins_id: int=0) -> List[str]:  #2
        send_info = self.col_sep.join(['2', str(ins_id)])
        recv_info = self.send_and_recv(send_info)
        recv_info = recv_info.strip().split(self.row_sep)
        return [_ for _ in recv_info if len(_) > 0]

    def get_role_of_user(self, username: str, ins_id: int=0) -> List[str]:  #3
        send_info = self.col_sep.join(['3', str(ins_id), username])
        recv_info = self.send_and_recv(send_info)
        recv_info = recv_info.strip().split(self.row_sep)
        return [_ for _ in recv_info if len(_) > 0]

    def get_number_of_nodes(self, username: str='', ins_id: int=0) -> int:  #4
        send_info = self.col_sep.join(['4', str(ins_id)])
        if len(username) > 0:
            send_info += self.col_sep + username
        recv_info = self.send_and_recv(send_info)
        recv_info = recv_info.strip()
        ans = -1
        try:
            ans = int(recv_info)
        except ValueError:
            pass
        return ans

    def get_number_of_edges(self, username: str='', ins_id: int=0) -> int:  #5
        send_info = self.col_sep.join(['5', str(ins_id)])
        if len(username) > 0:
            send_info += self.col_sep + username
        recv_info = self.send_and_recv(send_info)
        recv_info = recv_info.strip()
        ans = -1
        try:
            ans = int(recv_info)
        except ValueError:
            pass
        return ans

    def get_graph_data(self, username: str='', ins_id: int=0) -> List[List[str]]:  #6
        send_info = self.col_sep.join(['6', str(ins_id)])
        if len(username) > 0:
            send_info += self.col_sep + username
        recv_info = self.send_and_recv(send_info)
        recv_info = recv_info.strip().split(self.row_sep)
        return [_.strip().split(self.col_sep) for _ in recv_info]

    def grant_user_privilege(self, username: str, priv: str, ins_id: int=0) -> bool:   #7
        send_info = self.col_sep.join(['7', str(ins_id), username, priv])
        recv_info = self.send_and_recv(send_info)
        return (len(recv_info) > 0) and (recv_info[0] == '1')

    def remove_user_privilege(self, username: str, priv: str, ins_id: int=0) -> bool:  #8
        send_info = self.col_sep.join(['8', str(ins_id), username, priv])
        recv_info = self.send_and_recv(send_info)
        return (len(recv_info) > 0) and (recv_info[0] == '1')

    def create_node(self, username: str, ins_id: int=0) -> bool:   #9
        send_info = self.col_sep.join(['9', str(ins_id), username])
        recv_info = self.send_and_recv(send_info)
        return (len(recv_info) > 0) and (recv_info[0] == '1')

    def create_edge(self, username: str, ins_id: int=0) -> bool:   #10
        send_info = self.col_sep.join(['10', str(ins_id), username])
        recv_info = self.send_and_recv(send_info)
        return (len(recv_info) > 0) and (recv_info[0] == '1')

    def delete_node(self, username: str, ins_id: int=0) -> bool:   #11
        send_info = self.col_sep.join(['11', str(ins_id), username])
        recv_info = self.send_and_recv(send_info)
        return (len(recv_info) > 0) and (recv_info[0] == '1')

    def delete_edge(self, username: str, ins_id: int=0) -> bool:   #12
        send_info = self.col_sep.join(['12', str(ins_id), username])
        recv_info = self.send_and_recv(send_info)
        return (len(recv_info) > 0) and (recv_info[0] == '1')

    def modify_node_edge(self, username: str, ins_id: int=0) -> bool:  #13
        send_info = self.col_sep.join(['13', str(ins_id), username])
        recv_info = self.send_and_recv(send_info)
        return (len(recv_info) > 0) and (recv_info[0] == '1')

    def query_path(self, username: str, ins_id: int=0) -> List[List[str]]: #14
        send_info = self.col_sep.join(['14', str(ins_id), username])
        recv_info = self.send_and_recv(send_info)
        recv_info = recv_info.strip().split(self.row_sep)
        return [_.strip().split(self.col_sep) for _ in recv_info]

    def import_graph(self, username: str, ins_id: int=0) -> bool:  #15
        send_info = self.col_sep.join(['15', str(ins_id), username])
        recv_info = self.send_and_recv(send_info)
        return (len(recv_info) > 0) and (recv_info[0] == '1')

    def export_graph(self, username: str, ins_id: int=0) -> bool:  #16
        send_info = self.col_sep.join(['16', str(ins_id)])
        recv_info = self.send_and_recv(send_info)
        return (len(recv_info) > 0) and (recv_info[0] == '1')


class Test(object):
    def __init__(self):
        host = '166.111.80.159'
        port = 9998
        self.interface = Interface(host, port)

    def test_interface(self, user: str, passwd: str, ins_id: int=0):
        print('Test user: {}'.format(user))
        print('Login: {}'.format(
            self.interface.login(user, passwd, ins_id)
        ))
        print('User List: {}'.format(
            self.interface.get_users_list(ins_id)
        ))
        a_user = 'reader_test'
        user_list = ['reader_test', 'editor_test', 'publisher_test', 'architect_test', 'norole_test']
        print('Role of Users: ')
        for _ in user_list:
            print('{} -> {}'.format(_,
                self.interface.get_role_of_user(_, ins_id)
            ))
        print('Role of user ({}): {}'.format(a_user,
            self.interface.get_role_of_user(a_user, ins_id)
        ))
        print('#Nodes: {}'.format(
            self.interface.get_number_of_nodes(user, ins_id)
        ))
        print('#Edges: {}'.format(
            self.interface.get_number_of_edges(user, ins_id)
        ))
        print('Graph Content: {}'.format(
            self.interface.get_graph_data(user, ins_id)
        ))
        a_priv = 'publisher'
        print('Grant Privilege: {}'.format(
            self.interface.grant_user_privilege(a_user, a_priv, ins_id)
        ))
        print('Role of user ({}): {}'.format(a_user,
            self.interface.get_role_of_user(a_user, ins_id)
        ))
        print('Remove Privilege: {}'.format(
            self.interface.remove_user_privilege(a_user, a_priv, ins_id)
        ))
        print('Role of user ({}): {}'.format(a_user,
            self.interface.get_role_of_user(a_user, ins_id)
        ))
        print('Create Node: {}'.format(
            self.interface.create_node(user, ins_id)
        ))
        print('Create Edge: {}'.format(
            self.interface.create_edge(user, ins_id)
        ))
        print('Delete Node: {}'.format(
            self.interface.delete_node(user, ins_id)
        ))
        print('Delete Node: {}'.format(
            self.interface.delete_edge(user, ins_id)
        ))
        print('Modify Node and Edge: {}'.format(
            self.interface.modify_node_edge(user, ins_id)
        ))
        print('Query Path: {}'.format(
            self.interface.query_path(user, ins_id)
        ))
        print('Import Graph: {}'.format(
            self.interface.import_graph(user, ins_id)
        ))
        print('Export Graph: {}'.format(
            self.interface.export_graph(user, ins_id)
        ))

    def test_all(self):
        user = 'neo4j'
        passwd = 'neo4j-tests'
        ins_id = 0
        self.test_interface(user, passwd, ins_id)


def main():
    test = Test()
    test.test_all()


if __name__ == '__main__':
    main()
