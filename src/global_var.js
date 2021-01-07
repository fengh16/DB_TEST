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

function getFile (_this) {
  // requires:
  // _this.operationTable
  // _this.currentOperationID
  // _this.filenameString
  // _this.fileContent
  // _this.loading
  let filename = _this.operationTable[_this.currentOperationID].filepath
  _this.$http.get('/relational/select-file/', {
    params: {
      username: _this.GLOBAL.username,
      filename: filename
    }
  }).then(
    function (response) {
      console.log(response)
      if (response.status === 200 && response.data.success) {
        console.log(response.data)
        _this.filenameString = filename
        _this.fileString = response.data.result
        _this.fileContent = response.data.result
        _this.loading = false
      } else {
        _this.$alert(`查看文件失败：${response.data.msg}`)
        _this.loading = false
      }
    }, function (response) {
      _this.$alert('查看文件失败，请检查网络连接，稍后再试！')
      _this.loading = false
    })
}

function deleteFile (_this) {
  // requires:
  // _this.operationTable
  // _this.currentOperationID
  let filename = _this.operationTable[_this.currentOperationID].filepath
  _this.$http.post('/relational/delete-file/', {
    username: _this.GLOBAL.username,
    filename: filename
  }).then(response => {
    _this.loading = false
    if (response.status === 200 && response.data.success) {
      console.log(response.data)
      _this.$alert(`删除文件成功`)
    } else {
      _this.$alert(`删除文件失败：${response.data.msg}`)
    }
  }, response => {
    _this.loading = false
    _this.$alert(`删除文件失败：网络错误`)
  })
}

export default {
  systemName,
  username,
  isAdmin,
  userList,
  privilegeList,
  databaseList,
  getFile,
  deleteFile
}
