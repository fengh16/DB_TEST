let systemName = '工业互联网可信服务数据管理测试平台'
let username = '未登录'
let isAdmin = false
let userList = []
let privilegeList = []
let databaseList = []

// function userList () {
//   return JSON.parse(localStorage.getItem('userList'))
// }
//
// function isAdmin () {
//   return JSON.parse(localStorage.getItem('isAdmin')) === true
// }

function createTable (_this) {
  console.log(_this.GLOBAL.username, _this.currentDatabaseName, _this.operationTable[0])
  let tableName = _this.operationTable[_this.currentOperationID].tableName
  _this.$http.post('/relational/create-table/', {
    username: _this.GLOBAL.username,
    databaseName: _this.currentDatabaseName,
    tableName: tableName,
    instanceId: _this.instanceID
  }).then(response => {
    _this.loading = false
    if (response.status === 200 && response.data.success) {
      console.log(response.data)
      _this.$alert(`创建表 ${tableName} 成功`)
      _this.getTableList()
      // _this.operationTable[0].tableName = ''
    } else {
      _this.$alert(`创建表 ${tableName} 失败：${response.data.result}`)
    }
  }, response => {
    _this.loading = false
    _this.$alert(`创建表 ${tableName} 失败：网络错误`)
  })
}

function insert (_this) {
  let tableName = _this.operationTable[_this.currentOperationID].tableName
  _this.$http.post('/relational/insert/', {
    username: _this.GLOBAL.username,
    databaseName: _this.currentDatabaseName,
    tableName: tableName,
    instanceId: _this.instanceID
  }).then(response => {
    _this.loading = false
    if (response.status === 200 && response.data.success) {
      console.log(response.data)
      _this.$alert(`向表 ${tableName} 插入数据成功`)
      // _this.operationTable[0].tableName = ''
    } else {
      _this.$alert(`向表 ${tableName} 插入数据失败：${response.data.result}`)
    }
  }, response => {
    _this.loading = false
    _this.$alert(`向表 ${tableName} 插入数据失败：网络错误`)
  })
}

function update (_this) {
  let tableName = _this.operationTable[_this.currentOperationID].tableName
  _this.$http.post('/relational/update/', {
    username: _this.GLOBAL.username,
    databaseName: _this.currentDatabaseName,
    tableName: tableName,
    instanceId: _this.instanceID
  }).then(response => {
    _this.loading = false
    if (response.status === 200 && response.data.success) {
      console.log(response.data)
      _this.$alert(`更新表 ${tableName} 数据成功`)
      // _this.operationTable[0].tableName = ''
    } else {
      _this.$alert(`更新表 ${tableName} 数据失败：${response.data.result}`)
    }
  }, response => {
    _this.loading = false
    _this.$alert(`更新表 ${tableName} 数据失败：网络错误`)
  })
}

function deleteData (_this) {
  let tableName = _this.operationTable[_this.currentOperationID].tableName
  _this.$http.post('/relational/delete/', {
    username: _this.GLOBAL.username,
    databaseName: _this.currentDatabaseName,
    tableName: tableName,
    instanceId: _this.instanceID
  }).then(response => {
    _this.loading = false
    if (response.status === 200 && response.data.success) {
      console.log(response.data)
      _this.$alert(`删除表 ${tableName} 数据成功`)
      // _this.operationTable[0].tableName = ''
    } else {
      _this.$alert(`删除表 ${tableName} 数据失败：${response.data.result}`)
    }
  }, response => {
    _this.loading = false
    _this.$alert(`删除表 ${tableName} 数据失败：网络错误`)
  })
}

function getDisplayTableSchema (_this, operationId) {
  _this.$http.get('/relational/view-table-schema/', {
    params: {
      username: _this.GLOBAL.username,
      databaseName: _this.currentDatabaseName,
      tableName: _this.operationTable[operationId].tableName,
      instanceId: _this.instanceID,
      encrypted: _this.encodeMode
    }
  }).then(
    function (response) {
      if (response.status === 200 && response.data.success) {
        _this.currentTableName = response.data.result.tableName
        _this.dataTableSchema = response.data.result.schema
        if (operationId === _this.schemaOperationID) {
          _this.currentFocusOperation = operationId
          _this.loading = false
        }
      } else {
        if (operationId === _this.schemaOperationID) {
          _this.$alert(`获取表信息失败：${response.data.msg}`)
          _this.loading = false
        }
      }
    }, response => {
      _this.$alert('获取表信息失败：网络错误')
      _this.loading = false
    })
}

function getDisplayTable (_this) {
  _this.$http.get('/relational/select/', {
    params: {
      username: _this.GLOBAL.username,
      databaseName: _this.currentDatabaseName,
      tableName: _this.operationTable[_this.currentOperationID].tableName,
      instanceId: _this.instanceID,
      encrypted: _this.encodeMode
    }
  }).then(
    function (response) {
      console.log(response)
      if (response.status === 200 && response.data.success) {
        console.log(response.data)
        _this.dataTable = response.data.result
        _this.loading = false
      } else {
        _this.$alert(`查看数据失败：${response.data.msg}`)
        _this.loading = false
      }
    }, function (response) {
      _this.$alert('查看数据失败，请检查网络连接，稍后再试！')
      _this.loading = false
    })
}

function getTableList (_this) {
  _this.$http.get('/relational/list-table/', {
    params: {
      username: _this.GLOBAL.username,
      instanceId: _this.instanceID,
      databaseName: _this.currentDatabaseName
    }
  }).then(
    function (response) {
      if (response.status === 200 && response.data.success) {
        console.log(response.data)
        _this.tableList = []
        response.data.result.forEach(e => {
          _this.tableList.push({
            value: e,
            label: e
          })
        })
      } else {
        _this.$alert(`获取数据表列表失败：${response.data.msg}`)
      }
    }, function (response) {
      _this.$alert(`获取数据表列表失败：${response.data.msg}`)
    })
}

function getDatabaseList (_this, cascade) {
  _this.$http.get('/relational/list-database/', {
    params: {
      username: _this.GLOBAL.username,
      instanceId: _this.instanceID
    }
  }).then(
    function (response) {
      if (response.status === 200 && response.data.success) {
        console.log(response.data)
        _this.databaseList = []
        response.data.result.forEach(e => {
          _this.databaseList.push({
            value: e,
            label: e
          })
        })
        if (response.data.result.length > 0) {
          _this.currentDatabaseName = _this.databaseList[_this.databaseList.length - 1].value
        }
        if (cascade) {
          getTableList(_this)
        }
      } else {
        _this.$alert('获取数据库列表失败：没有权限')
      }
    }, function (response) {
      _this.$alert('获取数据库列表失败，请检查网络连接，稍后再试！')
    })
}

export default {
  systemName,
  username,
  isAdmin,
  userList,
  privilegeList,
  databaseList,
  createTable,
  insert,
  update,
  getDisplayTableSchema,
  getDisplayTable,
  getTableList,
  getDatabaseList,
  deleteData
}
