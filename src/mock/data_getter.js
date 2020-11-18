export default {
  'post|/login': function (option) {
    let body = JSON.parse(option.body)
    if ('username' in body && 'password' in body && body['username'] && body['username'] === body['password']) {
      return {
        status: 200,
        result: '登录成功',
        usertype: '管理员'
      }
    }
    return {
      status: 500,
      result: '登录失败'
    }
  },
  'post|/relational/authenticate': function (option) {
    let body = JSON.parse(option.body)
    if ('username' in body && 'password' in body && body['username'] && body['username'] === body['password']) {
      return {
        status: 200,
        success: true,
        result: '认证成功'
      }
    }
    return {
      status: 200,
      success: false,
      result: '认证失败'
    }
  },
  'get|/relational/log': option => {
    return {
      status: 200,
      success: true,
      result: ['2020年10月10日往表ABC插入两条数据', '2020年11月11日删库跑路', '2020年11月12日恢复成功'] // 每个元素是一行日志
    }
  },
  'get|/relational/description': optipon => {
    return {
      status: 200,
      success: true,
      result: {
        'IP地址': '166.111.80.113',
        'mac地址': '80:18:44:f4:07:6e',
        '...': '...'
      },
      log: ['log1 of relational description', 'log2 of relational description']
    }
  },
  'get|/relational/list-database/': option => {
    return {
      status: 200,
      success: true,
      result: ['industry_database_1', 'industry_database_2', 'industry_database_3']
    }
  },
  'get|/relational/select/': option => {
    return {
      status: 200,
      success: true,
      result: [{
        id: 0,
        prop1: 'row1, col1',
        prop2: 'row1, col2'
      }, {
        id: 1,
        prop1: 'row2, col1',
        prop2: 'row2, col2'
      }]
    }
  },
  'post|/relational/create-database': option => {
    return {
      status: 200,
      success: true,
      result: ['创建成功'],
      log: ['log1 of create-database', 'log2 of create-database']
    }
  },
  'post|/relational/create-table': option => {
    return {
      status: 200,
      success: true,
      result: '创建成功',
      log: ['log1 of create-table', 'log2 of create-table']
    }
  },
  'get|/relational/view-table-schema': option => {
    return {
      status: 200,
      success: true,
      result: {
        'tableName': 'industry_table_1',
        'schema': [{
          id: 0,
          columnName: 'column1',
          propName: 'prop1',
          columnType: 'integer',
          columnConstraint: 'primary key'
        }, {
          id: 1,
          columnName: 'column2',
          propName: 'prop2',
          columnType: 'varchar(32)',
          columnConstraint: ''
        }]
      },
      log: ['log of view-table-schema']
    }
  },
  'post|/relational/insert': option => {
    return {
      status: 200,
      success: true,
      result: '插入大失败',
      log: ['log of insert']
    }
  },
  'post|/relational/update': option => {
    return {
      status: 200,
      success: true,
      result: '更新成功',
      log: ['log of update']
    }
  },
  'post|/relational/delete': option => {
    return {
      status: 200,
      success: true,
      result: '删除成功',
      log: ['log of delete']
    }
  }

}
