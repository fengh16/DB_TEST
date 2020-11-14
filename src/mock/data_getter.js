export default {
  'post|/login': option => {
    return {
      status: 200,
      result: '登录成功',
      usertype: '管理员'
    }
  },
  'post|/relational/authenticate': option => {
    return {
      status: 200,
      success: true,
      result: '认证成功'
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
        'result1': 'i don\'t know what to write',
        'result2': 'a result of description'
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
  }
}
