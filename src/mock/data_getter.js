export default {
  'post|/login': option => {
    return {
      status: 200,
      result: '登录成功',
      usertype: '普通用户'
    }
  }
}
