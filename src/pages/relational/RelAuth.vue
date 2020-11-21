<template>
  <el-row type="flex">
    <el-col :span="24">
      <h1>权限管理测试</h1>
      <div class="left-indent">
        <div class="from-left">
          <p v-if="this.GLOBAL.username!=='administrator'">无权查看此页面</p>
          <el-button
            v-if="this.GLOBAL.username==='administrator'"
            type="primary"
            plain
            v-loading="isSavingChanges"
            @click="onSavePrivilegeSetting">保存</el-button>
        </div>
        <el-table
          v-if="this.GLOBAL.username==='administrator'"
          :data="operationTable"
                  ref="operations"
                  stripe
                  row-key="id"
                  default-expand-all
        >
          <el-table-column
            prop="title"
            :label="operationTableTitle"
            align="left"
            width="120"
          ></el-table-column>
          <el-table-column
            v-for="(username, index) in userList"
            :label="'用户 '+username"
            :key="index"
            align="center"
          >
            <template slot-scope="scope">
              <el-switch
                :disabled="username === 'administrator'"
                v-model="scope.row.granted[username]"
                active-text="允许"
                inactive-text="禁止"
              >

              </el-switch>
            </template>
          </el-table-column>

        </el-table>
      </div>
    </el-col>
  </el-row>
</template>

<script>
export default {
  name: 'RelAuth',
  data () {
    return {
      operationTable: [],
      operationTableTitle: '',
      isSavingChanges: false,
      userList: ['administrator', 'developer1', 'developer2', 'developer3', 'developer4']
    }
  },
  methods: {
    getUserList () {

    },
    getPrivilegeList () {
      let _this = this
      console.log(this.GLOBAL.username)
      this.$http.get('/relational/user-privilege-list/', {
        params: {
          username: this.GLOBAL.username
        }
      }).then(function (response) {
        console.log(response.data)
        if (response.status === 200 && response.data.success) {
          let privileges = response.data.result
          privileges.forEach((board) => {
            let operationBoard = []
            board.children.forEach((child) => {
              let newOperation = {
                id: child.itemId,
                title: child.title,
                granted: child.granted
              }
              operationBoard.push(newOperation)
            })

            if (board.title === '全局权限管理') {
              _this.operationTable = operationBoard
            }
            _this.operationTableTitle = board.title
          })
        }
      })
    },
    onSavePrivilegeSetting () {
      let _this = this
      this.isSavingChanges = true
      let newPrivilegeList = [{
        caseId: 0,
        title: '全局权限管理',
        children: this.operationTable
      }]
      console.log(this.operationTable)
      this.$http.post('/relational/update-user-privilege-list/', {
        username: this.GLOBAL.username,
        privilege: newPrivilegeList
      }).then(response => {
        console.log(response)
        if (response.status === 200 && response.data.success) {
          _this.$notify({
            // title: '保存成功',
            message: '保存权限更改成功',
            offset: 200
          })
          _this.isSavingChanges = false
        } else {
          _this.$alert('保存权限更改失败，请稍后再试！')
          _this.isSavingChanges = false
        }
      }, response => {
        _this.$alert('保存权限更改失败，请检查网络连接，稍后再试！')
        _this.isSavingChanges = false
      })
    }
  },
  created () {
    this.getPrivilegeList()
  }
}
</script>

<style scoped>
  .from-left {
    text-align: left;
  }
  .left-indent {
    margin-left: 40px;
  }
</style>
