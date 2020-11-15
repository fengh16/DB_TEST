<template>
  <el-row type="flex">
    <el-col :span="10">
      <div class="left-indent">
        <h1>权限管理功能测试</h1>
        <div class="from-left">
          <el-button type="primary" plain @click="onClickCreateDatabase">创建数据库</el-button>
          <el-button type="primary" plain @click="onDebug">DEBUG</el-button>
        </div>
        <el-table :data="operationTable"
                  ref="operations"
                  stripe
                  row-key="id"
                  default-expand-all
        >
          <el-table-column
            prop="title"
            label="全局权限管理"
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
      operationTable: [{
        id: 0,
        title: '创建数据库权限',
        userAuth: {
          username1: true,
          username2: false
        }
      }],
      userList: ['username1', 'username2']
    }
  },
  methods: {
    getUserList () {

    }
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
