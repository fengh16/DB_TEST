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
后端：如果用户名和密码匹配，返回登录成功，同时 `usertype` 中体现用户级别，否则失败

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

后端：退出登录，设置该用户的登录状态为离线

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

后端：根据保存的用户名和密码进行认证，无需返回log

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

后端：`result` 每个元素是一个用户名，如 `result = ['admin', 'developer1', 'developer2']`

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

后端：`result` 是一个列表，第一个元素是全局系列权限（包括创建、访问、更改、删除数据库），后面每个元素是一个数据库中的系列权限（如在数据库a中创建、访问、更改、删除表）；每个元素的字段有：`caseId` 表示元素的id，`title` 表示这个系列的名字，即表头，第一个元素的 `title` 应是 `"全局权限管理"` ；`children` 是一个列表，表示这个系列中包含的权限项，这其中每个孩子的字段有： `itemId` 表示权限的id，`title` 表示权限的名字，即这一行的第一列标题， `granted` 是一个对象，其中对每个用户名有一个bool变量表示授权与否

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

后端：请求的body中包含一个与上一个API返回值相同格式的对象，表示更改后的所有权限，后端接受这个对象并且更新各个权限

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

后端：为用户 `username` 的第 `instanceId` 个实例创建一个名为 `databaseName` 的数据库，如果没有权限则不创建并返回提示

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

后端：为用户 `username` 的第 `instanceId` 个实例的名为 `databaseName` 的数据库创建一个名为 `tableName` 的表，表的字段后端可以预设，如果没有权限则不创建并返回提示

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

后端：返回用户 `username` 的第 `instanceId` 个实例的名为 `databaseName` 的数据库的名为 `tableName` 的表的schema信息，存储在 `result.schema` 字段中，这是一个列表，每个元素是一个对象，对象包括三个字段：`columnName` 表示该列的列名，`dataType` 表示该类的类型，字符串格式，`constraint` 为该列的约束，如primary key，not null等，是一个字符串的列表，如果没有约束则为空列表

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

后端：为用户 `username` 的第 `instanceId` 个实例的名为 `databaseName` 的数据库的名为 `tableName` 的表插入一行数据，数据内容后端可以预设，如果没有权限则不创建并返回提示

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

后端：为用户 `username` 的第 `instanceId` 个实例的名为 `databaseName` 的数据库的名为 `tableName` 的表更新一列数据，数据内容后端可以预设，如果没有权限则不更新并返回提示

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

后端：为用户 `username` 的第 `instanceId` 个实例的名为 `databaseName` 的数据库的名为 `tableName` 的表删除一行数据，删除的行内容后端可以预设，如果没有权限则不删除并返回提示

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
        "result": [{
            "id": 0,
            "prop1": "value1",
            "prop2": "value2"
        }],
        "log": [str]
    }
}
```

后端：返回用户 `username` 的第 `instanceId` 个实例的名为 `databaseName` 的数据库的名为 `tableName` 的表的数据，保存在 `result` 中， `result` 是一个对象的列表，每个元素是一行数据，包含 `id` 表示该行的id，这个 `id` 不是数据库中的属性，可以后端来指定，其余的键值对是数据库中的 `列名: 值` 的形式，列名和API 10中返回的应该保持一致，如果没有权限则不返回并提示。此外，如果请求 `body` 中 `encrypted` 不为空串，返回用 `encrpyted` 值的算法进行加密后的结果（不清楚这个加密后的结果是否还是对象的格式，或者是一个二进制串，如果是后者，就直接返回也可以，无需改成对象）

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
        "result": [{}],
        "log": [str]
    }
}
```

后端：对用户 `username` 的第 `instanceId` 个实例的名为 `databaseName` 的数据库的名为 `tableName` 的表的数据进行嵌入，要嵌入的信息是 `embedding` 字段的字符串，返回嵌入后的表，格式与上一个API相同。如果用户没有被授予表修改权限，也不执行嵌入

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

后端：删除用户 `username` 的第 `instanceId` 个实例的名为 `databaseName` 的数据库的名为 `tableName` 的表，如果没有权限则不删除并返回提示

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

后端：删除用户 `username` 的第 `instanceId` 个实例的名为 `databaseName` 的数据库，如果没有权限则不删除并返回提示

18. 查看数据服务信息

```python
'GET /relational/description'

param = {}

response = {
    200: {
        "success": bool,
        "result": {
            "IP": str,
            "MAC": str,
            "serviceDir": str,
            "dataDir": str,
            "dataAmount": str,
            "space": str
        },
        "log": [str]
    }
}
```

后端：返回关系数据服务的信息，目前暂时约定包括上面字段：IP地址，MAC地址，服务程序目录，数据存储位置，数据量，服务器可用空间，全部用字符串的格式返回

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

后端：将名为 `filename` 的文件中的数据导入到用户 `username` 的第 `instanceId` 个实例的名为 `databaseName` 的数据库的名为 `tableName` 的表中，导入的方式有 `sql` 和 `shell` 两种，在请求的 `method` 字段中指定，如果没有修改权限则不导入并报错

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

后端：将用户 `username` 的第 `instanceId` 个实例的名为 `databaseName` 的数据库的名为 `tableName` 的表的数据导出到名为 `filename` 的文件中，导出的方式有 `sql` 和 `shell` 两种，在请求的 `method` 字段中指定，如果没有查看权限则不导出并报错

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

后端：将用户 `username` 的第 `instanceId` 个实例的名为 `databaseName` 的数据库的名为 `tableName` 的表的schema导出到名为 `filename` 的文件中，导出的方式只有 `shell` 一种，在请求的 `method` 字段中指定，如果没有查看权限则不导出并报错

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

后端：查看文件 `filename` 的内容，存储于 `result` 字段中，是一个字符串的列表，每个元素表示文件中的一行，返回文本即可

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

后端：这个接口暂且弃用

24. 列出当前所有数据库

```python
'GET /relational/list-database'

param = {
    "username": str,
    "instanceId": str
}

response = {
    200: {
        "success": bool,
        "result": [str],
        "log": [str]
    }
}
```

后端：列出用户 `username` 的第 `instanceId` 个实例的所有数据库，存储于 `result` 字段中，是一个字符串的列表，每个元素是一个数据库名

## 平台验证方案

### 可迁移性
条款：平台应支持数据迁移，能够提供镜像、数据和应用的迁入和迁出服务。

验证方案：
1. 使用测试账户登录被测平台；
2. 使用测试系统模拟进行数据迁出，检验平台的数据迁入能力；
3. 使用测试系统模拟进行数据迁入，检验平台的数据迁出能力。



本系统验证流程：
1. 选择用户administrator
2. 执行查看文件（有内容）
3. 执行查看表数据（无内容）
4. 执行import导入
5. 执行查看表数据（有内容），迁入验证完成
6. 执行删除文件
7. 执行查看文件（无内容）
8. 执行dump导出
9. 执行查看文件（有内容），迁出验证完成

### 可恢复性
条款：应提供数据备份与恢复功能，应定期对重要数据进行备份，并在灾难情况下及时恢复，保持业务连续运行。

验证方案：
1. 使用测试账户登录被测平台；
2. 使用测试系统模拟进行数据攻击；
3. 使用测试系统模拟进行数据恢复，检验平台的数据可恢复能力。

本系统验证流程：
1. 选择用户administrator
2. 执行查看文件（无内容）
3. 执行查看表数据（有内容）
4. 执行dump导出
5. 执行查看文件（有内容）
6. 执行删除表数据
7. 执行查看表数据（无内容），攻击完成
8. 执行import导入
9. 执行查看表数据（有内容），恢复完成

### 可销毁性
条款：如用户终止服务、用户提出数据删除，除非有特殊约定，应立即删除所有数据，且无法复原

验证方案：
1. 使用测试账户登录被测平台；
2. 使用测试系统模拟进行数据删除操作；
2. 使用测试系统模拟进行数据查询操作并查看操作日志，检验平台的数据销毁能力


本系统验证流程：
1. 选择用户administrator
2. 执行查看表数据（有内容）
3. 执行删除表数据
4. 执行查看表数据（无内容）
5. 执行查看日志（有删除日志），删除完成
6. 执行删除表
7. 执行查看表数据（没有这个表），删除完成
