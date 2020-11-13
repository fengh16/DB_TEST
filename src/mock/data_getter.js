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
  }
}
