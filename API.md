# 工业系统前后端连接的API文档

V11.13.2



改动：

- 11.13.2：增加了查看日志接口



小说明：

1. 返回结果一律保存在 `result` 字段中，日志保存在 `log` 字段中
2. POST请求大部分参数用 `param` 传输，设计密码的和大量数据的用 `body` 传输
3. 关系数据服务中，后端一律返回200，成功与失败在结果里判断，即使错误后端也不发500等



### 平台

1. 登录测试平台

```python
'POST /login/'

param = {}

body = {
  "username": str,
  "password": str
}

response = {
    200: {
        "result": "登录成功",
        "usertype": "普通用户 | 管理员"
    },
    500: {
        "result": "登录失败"
    }
}
```

2. 退出登录

```python
'POST /logout/'

param = {}

body = {
  "username": str
}

response = {
    200: {
        "result": "退出成功",
    },
    500: {
        "result": "尚未登录"
    }
}
```

### 关系数据服务

3. 身份认证

```python
'POST /relational/authenticate/'

param = {}

body = {
    "username": str,
    "password": str
}

response = {
    200: {
        "success": bool,
        "result": "认证成功",
        "log": [str]
    }
}
```

4. 获取可管理的用户列表

```python
'GET /relational/user-list/'

param = {
    "username": str
}

response = {
    200: {
        "success": bool,
        "result": [str],
        "log": [str]
    }
}
```

5. 获取可管理的权限列表（deprecated）

```python
'GET /relational/prilivege-list/'

param = {
    "username": str
}

response = {
    200: {
        "success": bool,
        "result": [{
            "caseId": 1,
            "title": "全局权限管理",
            "children": [{
                "itemId": 1,
                "title": "创建数据库权限"
            }, {}]
        }, {}],
        "log": [str]
    }
}
```

6. 获取所有用户的所有权限列表

```python
'GET /relational/user-privilege-list/'

param = {
    "username": str
}

response = {
    200: {
        "success": bool,
        "result": [{
            "caseId": 1,
            "title": "全局权限管理",
            "children": [{
                "itemId": 1,
                "title": "创建数据库权限",
                "granted": {
                    "username1": True,
                    "username2": False
                }
            }, {}]
        }, {}],
        "log": [str]
    }
}
```

7. 更新用户权限

```python
'POST /relational/update-user-privilege-list/'

param = {
    "username": str
}

body = {
    "privilege": [{
        "caseId": 1,
        "title": "全局权限管理",
        "children": [{
            "itemId": 1,
            "title": "创建数据库权限",
            "granted": {
                "username1": True,
                "username2": False
            }
        }, {}]
    }, {}]
}

response = {
    200: {
        "success": bool,
        "result": "更新成功 | 格式错误",
        "log": [str]
    }
}
```

8. 创建数据库

```python
'POST /relational/create-database/'

param = {
    "databaseName": str,
    "username": str,
    "instanceId": int  # 数据隔离中需要指定实例1或实例2，如果无需指定，可以默认填0
}

body = {}

response = {
    200: {
        "success": bool,
        "result": "创建成功 | 格式错误 | 没有权限",
        "log": [str]
    }
}
```

9. 创建表

```python
'POST /relational/create-table/'

param = {
    "databaseName": str,
    "tableName": str,
    "username": str,
    "instanceId": int
}

body = {}

response = {
    200: {
        "success": bool,
        "result": "创建成功 | 格式错误 | 没有权限",
        "log": [str]
    }
}
```

10. 查看表结构信息

```python
'GET /relational/view-table-schema'

param = {
    "databaseName": str,
    "tableName": str,
    "username": str,
    "instanceId": int,
    "encryptMethod": "SHA1 | SHA256 | MD2 | MD5"  # 加密方法，空字符串表示不加密
}

response = {
    200: {
        "success": bool,
        "result": {
            "schema": [{
                "columnName": str,
                "dataType": str,
                "constraint": [str]
            }, {}]
        },
        "log": [str]
    }
}
```

11. 插入数据

```python
'POST /relational/insert'

param = {
    "databaseName": str,
    "tableName": str,
    "username": str,
    "instanceId": int
}

body = {}

response = {
    200: {
        "success": bool,
        "result": "插入成功 | 格式错误 | 没有权限",
        "log": [str]
    }
}
```

12. 更新数据

```python
'POST /relational/update'

param = {
    "databaseName": str,
    "tableName": str,
    "username": str,
    "instanceId": int
}

body = {}

response = {
    200: {
        "success": bool,
        "result": "更新成功 | 格式错误 | 没有权限",
        "log": [str]
    }
}
```

13. 删除数据

```python
'POST /relational/delete'

param = {
    "databaseName": str,
    "tableName": str,
    "username": str,
    "instanceId": int
}

body = {}

response = {
    200: {
        "success": bool,
        "result": "删除成功 | 格式错误 | 没有权限",
        "log": [str]
    }
}
```

14. 查看数据

```python
'GET /relational/select'

param = {
    "databaseName": str,
    "tableName": str,
    "username": str,
    "instanceId": int,
    "encrypted": "SHA1 | SHA256 | MD2 | MD5"  # 加密方法，空字符串表示不加密
}

response = {
    200: {
        "success": bool,
        "result": [tuple],
        "log": [str]
    }
}
```

15. 对数据进行嵌入，查看嵌入后的数据

```python
'GET /relational/select-embedding'

param = {
    "databaseName": str,
    "tableName": str,
    "username": str,
    "instanceId": int,
    "embedding": str,  # 要嵌入的信息
    "encrypted": "SHA1 | SHA256 | MD2 | MD5"  # 加密方法，空字符串表示不加密
}

response = {
    200: {
        "success": bool,
        "result": [tuple],
        "log": [str]
    }
}
```

16. 删除表

```python
'POST /relational/drop-table'

param = {
    "databaseName": str,
    "tableName": str,
    "username": str,
    "instanceId": int
}

body = {}

response = {
    200: {
        "success": bool,
        "result": "删除成功 | 格式错误 | 没有权限",
        "log": [str]
    }
}
```

17. 删除数据库

```python
'POST /relational/drop-database'

param = {
    "databaseName": str,
    "username": str,
    "instanceId": int
}

body = {}

response = {
    200: {
        "success": bool,
        "result": "删除成功 | 格式错误 | 没有权限",
        "log": [str]
    }
}
```

18. 查看数据服务信息

```python
'GET /relational/description'

param = {}

response = {
    200: {
        "success": bool,
        "result": {
            "...": str,
        },
        "log": [str]
    }
}
```

19. 数据导入到一个表

```python
'POST /relational/import-data'

param = {
    "databaseName": str,
    "tableName": str,  # 如果表不存在，后端应当创建表
    "username": str,
    "instanceId": int,
    "filename": str,
    "method": "sql | shell"  # 导入的方式，有执行SQL和shell命令两种
}

body = {}

response = {
    200: {
        "success": bool,
        "result": "导入成功 | 格式错误 | 没有权限",
        "log": [str]
    }
}
```

20. 数据导出到一个文件

```python
'POST /relational/export-data'

param = {
    "databaseName": str,
    "tableName": str,
    "username": str,
    "instanceId": int,
    "filename": str,
    "method": "sql | shell"  # 导入的方式，有执行SQL和shell命令两种
}

body = {}

response = {
    200: {
        "success": bool,
        "result": "导出成功 | 格式错误 | 没有权限",
        "log": [str]
    }
}
```

21. 表结构导出到一个文件

```python
'POST /relational/export-schema'

param = {
    "databaseName": str,
    "tableName": str,
    "username": str,
    "instanceId": int,
    "filename": str,
    "method": "shell"  # 导入的方式，只有shell命令一种
}

body = {}

response = {
    200: {
        "success": bool,
        "result": "导出成功 | 格式错误 | 没有权限",
        "log": [str]
    }
}
```

22. 查看一个文件的内容（文件存储的是一个表的数据）

```python
'GET /relational/select-file'

param = {
    "username": str,
    "filename": str
}

response = {
    200: {
        "success": bool,
        "result": [str],  # 每个元素是一行
        "log": [str]
    }
}
```

23. 查看日志

```python
'GET /relational/log'

param = {
    "username": str
}

response = {
    200: {
        "success": bool,
        "result": [str],  # 每个元素是一行日志
        "log": [str]
    }
}
```

24. 列出当前所有数据库

```python
'GET /relational/list-database'

param = {
    "username": str
}

response = {
    200: {
        "success": bool,
        "result": [str],
        "log": [str]
    }
}
```
