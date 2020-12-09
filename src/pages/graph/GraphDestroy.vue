<template>
  <el-row type="flex">
    <el-col :span="10">
      <div class="left-indent">
        <h1>图可销毁性测试</h1>
        <el-table :data="operationTable"
                  ref="operations"
                  stripe
                  row-key="id"
                  default-expand-all
                  class="margin-top"
        >
          <el-table-column
            prop="title"
            label="操作名称"
            align="left"
            width="160"
          ></el-table-column>
          <el-table-column
            prop="fileName"
            label="文件路径"
            align="center"
          >
            <template slot-scope="scope">
            </template>
          </el-table-column>
          <el-table-column
            label="操作"
            align="center"
            width="80"
          >
            <template slot-scope="scope">
              <el-button type="primary" size="mini" plain @click="onExecute(scope.row.id)">执行</el-button>
            </template>
          </el-table-column>
        </el-table>
      </div>
    </el-col>
    <el-col :span="12" :offset="1" v-loading="loading">
      <h1>查看测试结果</h1>
      <div>
        <el-table
          v-if="shouldDisplayDataTable"
          :data="dataTable"
          ref="displayData"
          stripe
          row-key="id"
          default-expand-all
        >
          <el-table-column
            v-for="(columnDef, index) in dataTableSchema"
            :prop="columnDef.columnName"
            :label="columnDef.columnName"
            :key="index"
            align="center"
          >

          </el-table-column>
        </el-table>
        <el-table
          v-if="currentFocusOperation === 0"
          :data="dataTableSchema"
          ref="displayDataSchema"
          stripe
          row-key="id"
          default-expand-all
        >
          <el-table-column
            prop="columnName"
            label="列名"
            align="center"
          ></el-table-column>
          <el-table-column
            prop="columnType"
            label="类型"
            align="left"
          ></el-table-column>
          <el-table-column
            prop="columnConstraint"
            label="约束"
            align="left"
          ></el-table-column>
        </el-table>
      </div>
    </el-col>
  </el-row>
</template>

<script>
export default {
  name: 'RelDestroy',
  data () {
    return {
      databaseList: [],
      operationTable: [{
        id: 0,
        title: '删除结点和边数据',
        tableName: '',
        needParam: false
      }, {
        id: 1,
        title: '查看数据',
        tableName: '',
        needParam: false
      }],
      dataTable: [],
      dataTableSchema: [],
      currentFocusOperation: -1,
      loading: false,
      deleteDatabaseDialogShow: false,
      deleteDatabaseName: ''
    }
  },
  computed: {
    shouldDisplayDataTable () {
      return this.currentFocusOperation === 1
    }
  },
  methods: {
    getDisplayTable () {
      let _this = this
      this.$http.get('/graph/select/', {
        params: {
          username: this.GLOBAL.username,
          instanceId: 0
        }
      }).then(
        function (response) {
          console.log(response)
          if (response.status === 200 && response.data.success) {
            console.log(response.data)
            _this.dataTable = response.data.result.data
            _this.dataTableSchema = response.data.result.schema
            _this.loading = false
          } else {
            _this.$alert('查看数据失败')
            _this.loading = false
          }
        }, function (response) {
          _this.$alert('查看数据失败，请检查网络连接，稍后再试！')
          _this.loading = false
        })
    },
    delete () {
      let _this = this
      this.$http.post('/graph/delete/', {
        username: this.GLOBAL.username,
        instanceId: 0
      }).then(response => {
        _this.loading = false
        if (response.status === 200 && response.data.success) {
          console.log(response.data)
          _this.$notify({
            // title: '保存成功',
            message: `删除成功`,
            offset: 200
          })
          // _this.operationTable[0].tableName = ''
        } else {
          _this.$notify({
            // title: '保存成功',
            message: `删除失败：${response.data.msg}`,
            offset: 200
          })
        }
      }, response => {
        _this.loading = false
        _this.$notify({
          message: `删除失败：网络错误`
        })
      })
    },
    onExecute (operationId) {
      this.currentFocusOperation = operationId
      console.log(operationId)
      switch (operationId) {
        case 0:
          this.delete()
          break
        case 1:
          this.getDisplayTable()
          break
      }
    }
  }
}
</script>

<style scoped>
  .margin-top {
    margin-top: 20px;
  }
  .from-left {
    text-align: left;
  }
  .left-indent {
    margin-left: 40px;
  }
  .header-title {
    display: inline-block;
    border-left: 4px solid #409eff;
    margin-right: 20px;
    padding-left: 8px;
  }
</style>
