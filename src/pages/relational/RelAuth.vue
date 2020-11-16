<template>
  <el-row type="flex">
    <el-col :span="20">
      <div class="left-indent">
        <h1>权限管理功能测试</h1>
        <div class="from-left">
          <p v-if="this.GLOBAL.username!=='administrator'">无权查看此页面</p>
<!--          <el-button type="primary" plain @click="onClickCreateDatabase">创建数据库</el-button>-->
          <el-button v-if="this.GLOBAL.username==='administrator'" type="primary" plain @click="onSavePrivilegeSetting">保存</el-button>
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
                v-model="scope.row.userAuth[username]"
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
      userList: ['administrator', 'developer1', 'developer2']
    }
  },
  methods: {
    getUserList () {

    },
    getPrivilegeList () {
      this.$http.get('/relational/user-privilege-list/', {
        params: {username: ''}
      }).then(function (response) {
        if (response.status === 200 && response.body.success) {
          let privileges = response.body.result
          privileges.forEach((board) => {
            let operationBoard = []
            board.children.forEach((child) => {
              let newOperation = {
                id: child.itemId,
                title: child.title,
                userAuth: child.granted
              }
              operationBoard.push(newOperation)
            })

            if (board.title === '全局权限管理') {
              this.operationTable = operationBoard
            }
            this.operationTableTitle = board.title
          })
        }
      })
    },
    onSavePrivilegeSetting () {
      this.GLOBAL.privilegeList = this.operationTable
      this.$alert('保存成功')
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
