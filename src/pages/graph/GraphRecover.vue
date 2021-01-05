<template>
  <el-row type="flex">
    <el-col :span="10">
      <div class="left-indent">
        <h1>图可恢复性测试</h1>
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
              <el-input v-if="scope.row.id!==2"
                        placeholder="输入文件路径"
                        v-model="filenameString"
                        clearable>
              </el-input>
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
            align="left"
          >
          </el-table-column>
        </el-table>
      </div>
      <div class="file-text" v-if="shouldDisplayFileData">
        <h>{{fileString}}</h>
      </div>
    </el-col>
  </el-row>
</template>

<script>
export default {
  name: 'RelRecover',
  data () {
    return {
      databaseList: [],
      operationTable: [{
        id: 0,
        title: '备份数据',
        tableName: '',
        needParam: false
      }, {
        id: 1,
        title: '恢复数据',
        tableName: '',
        needParam: false
      }, {
        id: 2,
        title: '查看数据',
        tableName: '',
        needParam: false
      }, {
        id: 3,
        title: '查看文件',
        tableName: '',
        needParam: false
      }, {
        id: 4,
        title: '删除文件',
        tableName: '',
        needParam: false
      }],
      dataTable: [],
      dataTableSchema: [],
      currentFocusOperation: 0,
      loading: false,
      filenameString: '',
      fileString: '',
      method: ''
    }
  },
  computed: {
    shouldDisplayDataTable () {
      return this.currentFocusOperation === 2
    },
    shouldDisplayFileData  () {
      return this.currentFocusOperation === 3
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
    importData () {
      let _this = this
      this.$http.post('/graph/import-data/', {
        username: this.GLOBAL.username,
        filename: this.filenameString,
        instanceId: 0
      }).then(response => {
        _this.loading = false
        if (response.status === 200 && response.data.success) {
          console.log(response.data)
          _this.$notify({
            message: `导入成功`,
            offset: 200
          })
        } else {
          _this.$notify({
            message: `导入失败：${response.data.msg}`,
            offset: 200
          })
        }
      }, response => {
        _this.loading = false
        _this.$notify({
          message: `导入失败：网络错误`
        })
      })
    },
    exportData () {
      let _this = this
      this.$http.post('/graph/export-data/', {
        username: this.GLOBAL.username,
        filename: this.filenameString,
        instanceId: 0
      }).then(response => {
        _this.loading = false
        if (response.status === 200 && response.data.success) {
          console.log(response.data)
          _this.$notify({
            message: `导出成功`,
            offset: 200
          })
        } else {
          _this.$notify({
            message: `导出失败：${response.data.msg}`,
            offset: 200
          })
        }
      }, response => {
        _this.loading = false
        _this.$notify({
          message: `导出失败：网络错误`
        })
      })
    },
    getFile () {
      let _this = this
      this.$http.get('/graph/select-file/', {
        params: {
          username: this.GLOBAL.username,
          filename: this.filenameString
        }
      }).then(
        function (response) {
          console.log(response)
          if (response.status === 200 && response.data.success) {
            console.log(response.data)
            _this.fileString = response.data.result
            _this.loading = false
          } else {
            _this.$alert('查看文件失败：没有权限')
            _this.loading = false
          }
        }, function (response) {
          _this.$alert('查看文件失败，请检查网络连接，稍后再试！')
          _this.loading = false
        })
    },
    deleteFile () {
      let _this = this
      this.$http.post('/graph/delte-file/', {
        username: this.GLOBAL.username,
        filename: this.filenameString
      }).then(response => {
        _this.loading = false
        if (response.status === 200 && response.data.success) {
          console.log(response.data)
          _this.$notify({
            message: ` 删除文件成功`,
            offset: 200
          })
        } else {
          _this.$notify({
            message: `删除文件失败：${response.data.msg}`,
            offset: 200
          })
        }
      }, response => {
        _this.loading = false
        _this.$notify({
          message: `删除文件失败：网络错误`
        })
      })
    },
    onExecute (operationId) {
      this.currentFocusOperation = operationId
      console.log(operationId)
      switch (operationId) {
        case 0:
          this.exportData()
          break
        case 1:
          this.importData()
          break
        case 2:
          this.getDisplayTable()
          break
        case 3:
          this.getFile()
          break
        case 4:
          this.deleteFile()
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
  .left-indent {
    margin-left: 40px;
  }
  .from-left {
    text-align: left;
  }
  .header-title {
    display: inline-block;
    border-left: 4px solid #409eff;
    margin-right: 20px;
    padding-left: 8px;
  }
  .file-text{
    margin-top: 20px;
  }
</style>
