<template>

  <el-row type="flex">
    <el-col :span="10">
      <div class="left-indent">
        <h1>可迁移性测试</h1>
        <div class="from-left">
          <p class="header-title">当前数据库</p>
          <el-select v-model="currentDatabaseName" placeholder="选择数据库" default-first-option>
            <el-option
              v-for="item in databaseList"
              :key="item.value"
              :label="item.label"
              :value="item.value">
            </el-option>
          </el-select>
<!--          <el-button type="primary" plain @click="onClickCreateDatabase">创建数据库</el-button>-->
        </div>
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
            prop="tableName"
            label="表名/文件名"
            align="center"
          >
            <template slot-scope="scope">
              <el-input
                placeholder="输入表名"
                v-model="scope.row.tableName"
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
      <el-dialog title="查询语句导入数据" :visible.sync="filenameDialogShow_0">
        <el-form>
          <el-form-item label="文件路径">
            <el-input v-model="filenameString" autocomplete="off" placeholder="输入文件路径"></el-input>
          </el-form-item>
        </el-form>
        <div slot="footer" class="dialog-footer">
          <el-button @click="filenameDialogShow_0=false">取 消</el-button>
          <el-button type="primary" @click="importDataSql">执 行</el-button>
        </div>
      </el-dialog>
      <el-dialog title="import命令导入数据" :visible.sync="filenameDialogShow_1">
        <el-form>
          <el-form-item label="文件路径">
            <el-input v-model="filenameString" autocomplete="off" placeholder="输入文件路径"></el-input>
          </el-form-item>
        </el-form>
        <div slot="footer" class="dialog-footer">
          <el-button @click="filenameDialogShow_1=false">取 消</el-button>
          <el-button type="primary" @click="importDataShell">执 行</el-button>
        </div>
      </el-dialog>
      <el-dialog title="查询语句导出数据" :visible.sync="filenameDialogShow_2">
        <el-form>
          <el-form-item label="文件路径">
            <el-input v-model="filenameString" autocomplete="off" placeholder="输入文件路径"></el-input>
          </el-form-item>
        </el-form>
        <div slot="footer" class="dialog-footer">
          <el-button @click="filenameDialogShow_2=false">取 消</el-button>
          <el-button type="primary" @click="exportDataSql">执 行</el-button>
        </div>
      </el-dialog>
      <el-dialog title="dump命令导出数据" :visible.sync="filenameDialogShow_3">
        <el-form>
          <el-form-item label="文件路径">
            <el-input v-model="filenameString" autocomplete="off" placeholder="输入文件路径"></el-input>
          </el-form-item>
        </el-form>
        <div slot="footer" class="dialog-footer">
          <el-button @click="filenameDialogShow_3=false">取 消</el-button>
          <el-button type="primary" @click="exportDataShell">执 行</el-button>
        </div>
      </el-dialog>
      <el-dialog title="查看文件" :visible.sync="filenameDialogShow_5">
        <el-form>
          <el-form-item label="文件路径">
            <el-input v-model="filenameString" autocomplete="off" placeholder="输入文件路径"></el-input>
          </el-form-item>
        </el-form>
        <div slot="footer" class="dialog-footer">
          <el-button @click="filenameDialogShow_5=false">取 消</el-button>
          <el-button type="primary" @click="getFile">执 行</el-button>
        </div>
      </el-dialog>
      <el-dialog title="删除文件" :visible.sync="filenameDialogShow_6">
        <el-form>
          <el-form-item label="文件路径">
            <el-input v-model="filenameString" autocomplete="off" placeholder="输入文件路径"></el-input>
          </el-form-item>
        </el-form>
        <div slot="footer" class="dialog-footer">
          <el-button @click="filenameDialogShow_6=false">取 消</el-button>
          <el-button type="primary" @click="deleteFile">执 行</el-button>
        </div>
      </el-dialog>
    </el-col>
    <el-col :span="12" :offset="1" v-loading="loading">
      <h1>查看测试结果</h1>
      <div>
        <div class="title-reserved" v-if="shouldDisplayTableTitle">
          <h1>表： {{currentTableName}}</h1>
        </div>
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
        <el-input type="textarea"
                  :rows="20"
                  placeholder=""
                  v-model="fileContent"
                  readonly="true"
                  autosize="false"
                  resize="none">
        </el-input>
      </div>
      <div class="file-text" v-if="shouldDisplayFileData">
        <h>{{fileString}}</h>
      </div>
    </el-col>
  </el-row>
</template>

<script>
export default {
  name: 'RelMigration',
  data () {
    return {
      databaseList: [],
      currentDatabaseName: '',
      operationTable: [{
        id: 0,
        title: '查询语句导入数据',
        tableName: '',
        needParam: true,
        param: '',
        paramHint: '输入文件路径'
      }, {
        id: 1,
        title: 'import命令导入数据',
        tableName: '',
        needParam: true,
        param: '',
        paramHint: '输入文件路径'
      }, {
        id: 2,
        title: '查询语句导出数据',
        tableName: '',
        needParam: true,
        param: '',
        paramHint: '输入文件路径'
      }, {
        id: 3,
        title: 'dump命令导出数据',
        tableName: '',
        needParam: true,
        param: '',
        paramHint: '输入文件路径'
      }, {
        id: 4,
        title: '查看表数据',
        tableName: '',
        needParam: false
      }, {
        id: 5,
        title: '查看文件',
        tableName: '',
        needParam: true,
        param: '',
        paramHint: '输入文件路径'
      }, {
        id: 6,
        title: '删除文件',
        tableName: '',
        needParam: true,
        param: '',
        paramHint: '输入文件路径'
      }],
      dataTable: [],
      dataTableSchema: [],
      currentTableName: '',
      currentFocusOperation: 0,
      loading: false,
      filenameDialogShow_0: false, // 每个对话框的显示由单独的变量控制
      filenameDialogShow_1: false,
      filenameDialogShow_2: false,
      filenameDialogShow_3: false,
      filenameDialogShow_5: false,
      filenameDialogShow_6: false,
      filenameString: '',
      fileString: '',
      method: '',
      fileContent: 'asdddddddddddddddddd\nddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddd'
    }
  },
  computed: {
    shouldDisplayTableTitle () {
      return this.currentFocusOperation === 4
    },
    shouldDisplayDataTable () {
      return this.currentFocusOperation === 4
    },
    shouldDisplayFileData  () {
      return this.currentFocusOperation === 5
    }
  },
  methods: {
    getDatabaseList () {
      let _this = this
      this.$http.get('/relational/list-database/', {
        params: {
          username: this.GLOBAL.username,
          instanceId: 0
        }
      }).then(
        function (response) {
          if (response.status === 200 && response.data.success) {
            console.log(response.data)
            _this.databaseList = []
            response.data.result.forEach(e => {
              _this.databaseList.push({
                value: e,
                label: e
              })
            })
            if (response.data.result.length > 0) {
              _this.currentDatabaseName = _this.databaseList[0].value
            }
          } else {
            _this.$alert('获取数据库列表失败：没有权限')
          }
        }, function (response) {
          _this.$alert('获取数据库列表失败，请检查网络连接，稍后再试！')
        })
    },
    getDisplayTableSchema (operationId) {
      let _this = this
      this.$http.get('/relational/view-table-schema/', {
        params: {
          username: this.GLOBAL.username,
          databaseName: this.currentDatabaseName,
          tableName: this.operationTable[operationId].tableName,
          instanceId: 0,
          encrypted: ''
        }
      }).then(
        function (response) {
          if (response.status === 200 && response.data.success) {
            _this.currentTableName = response.data.result.tableName
            _this.dataTableSchema = response.data.result.schema
            if (operationId === -1) {
              _this.currentFocusOperation = operationId
              _this.loading = false
            }
          } else {
            if (operationId === 4) { // 查看数据功能出现问题时，显示表信息这里的提示不再重复显示
              return
            }
            _this.$alert('获取表信息失败：没有权限')
            _this.loading = false
          }
        }, response => {
          if (operationId === 4) {
            return
          }
          _this.$alert('获取表信息失败：网络错误')
          _this.loading = false
        })
    },
    getDisplayTable (operationId) {
      let _this = this
      this.$http.get('/relational/select/', {
        params: {
          username: this.GLOBAL.username,
          databaseName: this.currentDatabaseName,
          tableName: this.operationTable[operationId].tableName,
          instanceId: 0,
          encrypted: ''
        }
      }).then(
        function (response) {
          console.log(response)
          if (response.status === 200 && response.data.success) {
            console.log(response.data)
            _this.dataTable = response.data.result
            if (operationId) {
              _this.currentFocusOperation = operationId
              _this.loading = false
            }
          } else {
            _this.$alert('查看数据失败：没有权限')
            _this.loading = false
          }
        }, function (response) {
          _this.$alert('查看数据失败，请检查网络连接，稍后再试！')
          _this.loading = false
        })
    },
    importDataSql () {
      let _this = this
      let tableName = this.operationTable[0].tableName
      this.filenameDialogShow_0 = false
      this.$http.post('/relational/import-data/', {
        username: this.GLOBAL.username,
        databaseName: this.currentDatabaseName,
        tableName: tableName,
        filename: this.filenameString,
        instanceId: 0,
        method: 'sql'
      }).then(response => {
        _this.loading = false
        if (response.status === 200 && response.data.success) {
          console.log(response.data)
          _this.$notify({
            message: `导入表 ${tableName} 成功`,
            offset: 200
          })
        } else {
          _this.$notify({
            message: `导入表 ${tableName} 失败：${response.data.msg}`,
            offset: 200
          })
        }
      }, response => {
        _this.loading = false
        _this.$notify({
          message: `导入表 ${tableName} 失败：网络错误`
        })
      })
    },
    importDataShell () {
      let _this = this
      let tableName = this.operationTable[1].tableName
      this.filenameDialogShow_1 = false
      this.$http.post('/relational/import-data/', {
        username: this.GLOBAL.username,
        databaseName: this.currentDatabaseName,
        tableName: tableName,
        filename: this.filenameString,
        instanceId: 0,
        method: 'shell'
      }).then(response => {
        _this.loading = false
        if (response.status === 200 && response.data.success) {
          console.log(response.data)
          _this.$notify({
            message: `导入表 ${tableName} 成功`,
            offset: 200
          })
        } else {
          _this.$notify({
            message: `导入表 ${tableName} 失败：${response.data.msg}`,
            offset: 200
          })
        }
      }, response => {
        _this.loading = false
        _this.$notify({
          message: `导入表 ${tableName} 失败：网络错误`
        })
      })
    },
    exportDataSql () {
      let _this = this
      let tableName = this.operationTable[2].tableName
      this.filenameDialogShow_2 = false
      this.$http.post('/relational/export-data/', {
        username: this.GLOBAL.username,
        databaseName: this.currentDatabaseName,
        tableName: tableName,
        filename: this.filenameString,
        instanceId: 0,
        method: 'sql'
      }).then(response => {
        _this.loading = false
        if (response.status === 200 && response.data.success) {
          console.log(response.data)
          _this.$notify({
            message: `导出表 ${tableName} 成功`,
            offset: 200
          })
        } else {
          _this.$notify({
            message: `导出表 ${tableName} 失败：${response.data.msg}`,
            offset: 200
          })
        }
      }, response => {
        _this.loading = false
        _this.$notify({
          message: `导出表 ${tableName} 失败：网络错误`
        })
      })
    },
    exportDataShell () {
      let _this = this
      let tableName = this.operationTable[3].tableName
      this.filenameDialogShow_3 = false
      this.$http.post('/relational/export-data/', {
        username: this.GLOBAL.username,
        databaseName: this.currentDatabaseName,
        tableName: tableName,
        filename: this.filenameString,
        instanceId: 0,
        method: 'shell'
      }).then(response => {
        _this.loading = false
        if (response.status === 200 && response.data.success) {
          console.log(response.data)
          _this.$notify({
            message: `导出表 ${tableName} 成功`,
            offset: 200
          })
        } else {
          _this.$notify({
            message: `导出表 ${tableName} 失败：${response.data.msg}`,
            offset: 200
          })
        }
      }, response => {
        _this.loading = false
        _this.$notify({
          message: `导出表 ${tableName} 失败：网络错误`
        })
      })
    },
    getFile () {
      let _this = this
      this.filenameDialogShow_5 = false
      this.$http.get('/relational/select-file/', {
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
      this.filenameDialogShow_6 = false
      this.$http.post('/relational/delte-file/', {
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
      console.log(operationId)
      switch (operationId) {
        case 0:
          this.currentFocusOperation = operationId
          this.filenameDialogShow_0 = true
          break
        case 1:
          this.currentFocusOperation = operationId
          this.filenameDialogShow_1 = true
          break
        case 2:
          this.currentFocusOperation = operationId
          this.filenameDialogShow_2 = true
          break
        case 3:
          this.currentFocusOperation = operationId
          this.filenameDialogShow_3 = true
          break
        case 4:
          // select
          this.loading = true
          this.getDisplayTableSchema(4)
          this.getDisplayTable(4)
          break
        case 5:
          this.currentFocusOperation = operationId
          this.filenameDialogShow_5 = true
          break
        case 6:
          this.currentFocusOperation = operationId
          this.filenameDialogShow_6 = true
          break
      }
    }
  },
  created () {
    this.getDatabaseList()
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
