# 工业系统前后端连接的API文档（图数据管理服务）



### 图数据服务

4. 获取可管理的用户列表

```python
'GET /graph/user-list/'

param = {
    "username": str
}

response = {
    200: {
        "success": bool,
        "result": [str],
        "msg": str
    }
}
```

后端：`result` 每个元素是一个用户名，如 `result = ['admin', 'developer1', 'developer2']`

6. 获取所有用户的所有权限列表

```python
'GET /graph/user-privilege-list/'

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
                "title": "增加权限",
                "granted": {
                    "username1": True,
                    "username2": False
                }
            }, {}]
        }, {}],
        "msg": str
    }
}
```

后端：`result` 是一个列表，第一个元素是全局系列权限（包括查询、增加、删除、修改）；每个元素的字段有：`caseId` 表示元素的id，`title` 表示这个系列的名字，即表头，第一个元素的 `title` 应是 `"全局权限管理"` ；`children` 是一个列表，表示这个系列中包含的权限项，这其中每个孩子的字段有： `itemId` 表示权限的id，`title` 表示权限的名字，即这一行的第一列标题， `granted` 是一个对象，其中对每个用户名有一个bool变量表示授权与否

7. 更新用户权限

```python
'POST /graph/update-user-privilege-list/'

param = {
    "username": str
}

body = {
    "privilege": [{
        "caseId": 1,
        "title": "全局权限管理",
        "children": [{
            "itemId": 1,
            "title": "创建权限",
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
        "result": "",
        "msg": str
    }
}
```

后端：请求的body中包含一个与上一个API返回值相同格式的对象，表示更改后的所有权限，后端接受这个对象并且更新各个权限

9. 结点建模

```python
'POST /graph/node-modeling/'

param = {
    
}

body = {
    "label": str,
    "attr": object,
    "username": str,
    "instanceId": int
}

response = {
    200: {
        "success": bool,
        "result": "",
        "msg": str
    }
}
```

后端：为用户 `username` 的第 `instanceId` 个实例创建一个标签为 `label` 的结点，属性是 `attr` ，JSON格式。如果没有权限则不创建并返回提示

10. 边建模

```python
'POST /graph/edge-modeling/'

param = {
    
}

body = {
    "label": str,
    "attr": object,
    "username": str,
    "instanceId": int
}

response = {
    200: {
        "success": bool,
        "result": "",
        "msg": str
    }
}
```

后端：为用户 `username` 的第 `instanceId` 个实例创建一个标签为 `label` 的边，属性是 `attr` ，JSON格式。如果没有权限则不创建并返回提示

11. 查看数据

```python
'GET /graph/select/'

param = {
    "username": str,
    "instanceId": int
}

body = {
    
}

response = {
    200: {
        "success": bool,
        "result": [object],
        "msg": str
    }
}
```

后端：`result` 是一个列表，每一个元素是一个对象，以属性名：属性值的格式

12. 插入数据

```python
'POST /graph/insert/'

param = {
    
}

body = {
    "username": str,
    "instanceId": int
}

response = {
    200: {
        "success": bool,
        "result": "",
        "msg": str
    }
}
```

后端：为用户 `username` 的第 `instanceId` 个实例插入数据，如果失败，`msg` 表示提示信息

13. 删除数据

```python
'POST /graph/delete/'

param = {
    
}

body = {
    "username": str,
    "instanceId": int
}

response = {
    200: {
        "success": bool,
        "result": "",
        "msg": str
    }
}
```

后端：为用户 `username` 的第 `instanceId` 个实例删除数据，如果失败，`msg` 表示提示信息

14. 查看数据服务信息

```python
'GET /graph/description/'

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

后端：返回图数据服务的信息，字段和名称参照关系数据服务

15. 导入结点和边数据

```python
'POST /graph/import-data/'

param = {}

body = {
    "username": str,
    "instanceId": int,
    "filename": str
}

response = {
    200: {
        "success": bool,
        "result": "",
        "msg": str
    }
}
```

后端：将名为 `filename` 的文件中的数据导入到用户 `username` 的第 `instanceId` 个实例数据服务中，如果失败，`msg` 是失败提示信息

16. 导出结点和边数据

```python
'POST /graph/export-data/'

param = {}

body = {
    "username": str,
    "instanceId": int,
    "filename": str
}

response = {
    200: {
        "success": bool,
        "result": "",
        "msg": str
    }
}
```

后端：将名为 `filename` 的文件中的数据导出到用户 `username` 的第 `instanceId` 个实例数据服务中，如果失败，`msg` 是失败提示信息

17. 查看一个文件的内容

```python
'GET /graph/select-file/'

param = {
    "username": str,
    "filename": str
}

response = {
    200: {
        "success": bool,
        "result": [str],  # 每个元素是一行
        "msg": str
    }
}
```

后端：查看文件 `filename` 的内容，存储于 `result` 字段中，是一个字符串的列表，每个元素表示文件中的一行，返回文本即可，如果失败，`msg` 是失败提示信息

18. 删除文件

```python
'POST /graph/delete-file/'

body = {
    "username": str,
    "filename": str
}

response = {
    200: {
        "success": bool,
        "result": "",
        "msg": "删除成功 | 文件不存在"
    }
}
```

后端：删除用户 `username` 的名为 `filename` 的文件，如果失败，`msg` 是失败提示信息

19. 查看日志

```python
'GET /graph/log'

param = {
    "username": str
}

response = {
    200: {
        "success": bool,
        "result": [str],  # 每个元素是一行日志
        "msg": str
    }
}
```

后端：查看当前用户的日志

## 平台验证方案

### 1 身份认证

1. 选择用户root
2. 执行“设置密码”，设置一个密码root2
3. 执行“身份认证”，用错误的密码root1登录（登录失败）
4. 执行“身份认证”，用正确的密码root2登录（登录成功）

### 2 权限管理

1. 选择用户root
2. 进入权限管理，设置用户developer_1的查询权限为允许
3. 选择用户developer_1
4. 进入可操作性，执行“查看数据”（有内容）
5. 选择用户root
6. 进入权限管理，设置用户developer_1的查询权限为禁止
7. 选择用户developer_1
8. 进入可操作性，执行“查看数据”（无内容）

### 3 数据隔离

1. 选择用户root
2. 进入数据隔离，选择实例一，执行“查看数据”，无表名（有内容）
3. 选择实例二，执行“查看数据”，无表名（无内容）
4. 选择实例二，执行“插入数据”，无表名
5. 选择实例二，执行“查看数据”（有内容）
6. 选择实例一，执行“查看数据”（内容不变）

### 4 安全控制

1. 暂且跳过

### 5 可操作性

1. 选择用户root
2. 进入可操作性，执行“结点建模”，可选有/无标签，有/无属性
3. 执行“边建模”，可选有/无标签，有/无属性
4. 执行“查看数据”（有内容）
5. 执行“删除数据”
6. 执行“查看数据”（无内容）

### 6 知情权

1. 选择用户root
2. 进入知情权，查看数据服务的信息

### 7 可迁移性

1. 选择用户root
2. 进入可迁移性，执行“查看文件”（有内容）
3. 执行“查看数据”（无内容）
4. 执行“导入结点和边数据”
5. 执行“查看数据”（有内容）
6. 执行“删除文件”
7. 执行“查看文件”（无内容）
8. 执行“导出数据”
9. 执行“查看文件”（有内容）

### 8 可恢复性

1. 选择用户root
2. 进入可恢复性，执行查看文件（无内容）
3. 执行“查看数据”（有内容）
4. 执行“导出结点和边数据”
5. 执行“查看文件”（有内容）
6. 执行“删除数据”
7. 执行“查看数据”（无内容）
8. 执行“导入结点和边数据”
9. 执行“查看数据”（有内容）

### 9 可销毁性

1. 选择用户root
2. 进入可销毁性，执行“查看数据”（有内容）
3. 执行“删除结点和边数据”
4. 执行“查看数据”（无内容）
5. 执行“查看日志”（有删除日志）