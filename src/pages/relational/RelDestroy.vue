<template>
  <el-row type="flex">
    <el-col :span="10">
      <div class="left-indent">
        <h1>可销毁性测试</h1>
        <div class="from-left">
          <p class="header-title">当前数据库</p>
          <el-select v-model="currentDatabaseName" placeholder="选择数据库">
            <el-option
              v-for="item in databaseList"
              :key="item.value"
              :label="item.label"
              :value="item.value">
            </el-option>
          </el-select>
          <el-button type="primary" plain @click="onClickDeleteDatabase">删除数据库</el-button>
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
            label="表名"
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
      <el-dialog
        title="删除数据库"
        :visible.sync="deleteDatabaseDialogShow"
      >
        <el-form>
          <el-form-item label="数据库名">
            <el-input v-model="deleteDatabaseName" autocomplete="off" placeholder="输入要删除的数据库名称"></el-input>
          </el-form-item>
        </el-form>
        <div slot="footer" class="dialog-footer">
          <el-button @click="deleteDatabaseDialogShow=false">取 消</el-button>
          <el-button type="primary" @click="onDeleteDatabaseSubmit">删 除</el-button>
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
      currentDatabaseName: '',
      operationTable: [{
        id: 0,
        title: '查看表信息',
        tableName: '',
        needParam: false
      }, {
        id: 1,
        title: '删除表中所有数据',
        tableName: '',
        needParam: false
      }, {
        id: 2,
        title: '删除表',
        tableName: '',
        needParam: false
      }, {
        id: 3,
        title: '查看数据',
        tableName: '',
        needParam: false
      }],
      dataTable: [],
      dataTableSchema: [],
      currentTableName: '',
      currentFocusOperation: -1,
      loading: false,
      deleteDatabaseDialogShow: false,
      deleteDatabaseName: ''
    }
  },
  computed: {
    shouldDisplayTableTitle () {
      return this.currentFocusOperation === 0 | this.currentFocusOperation === 3
    },
    shouldDisplayDataTable () {
      return this.currentFocusOperation === 3
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
            if (operationId === 0) {
              _this.currentFocusOperation = operationId
              _this.loading = false
            }
          } else {
            if (operationId === 0) {
              _this.$alert(`获取表信息失败：${response.data.msg}`)
            }
            _this.loading = false
          }
        }, response => {
          if (operationId === 0) {
            _this.$alert('获取表信息失败：网络错误')
          }
          _this.loading = false
        })
    },
    getDisplayTable (operationId) {
      let _this = this
      this.$http.get('http://localhost:5000/relational/select/', {
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
            _this.$alert(`查看数据失败：${response.data.msg}`)
            _this.loading = false
          }
        }, function (response) {
          _this.$alert('查看数据失败，请检查网络连接，稍后再试！')
          _this.loading = false
        })
    },
    delete () {
      let _this = this
      let tableName = this.operationTable[1].tableName
      this.$http.post('/relational/delete/', {
        username: this.GLOBAL.username,
        databaseName: this.currentDatabaseName,
        tableName: tableName,
        instanceId: 0
      }).then(response => {
        _this.loading = false
        if (response.status === 200 && response.data.success) {
          console.log(response.data)
          _this.$notify({
            // title: '保存成功',
            message: `删除表 ${tableName} 全部数据成功`,
            offset: 200
          })
          // _this.operationTable[0].tableName = ''
        } else {
          _this.$notify({
            // title: '保存成功',
            message: `删除表 ${tableName} 全部数据失败：${response.data.msg}`,
            offset: 200
          })
        }
      }, response => {
        _this.loading = false
        _this.$notify({
          message: `删除表 ${tableName} 全部数据失败：网络错误`
        })
      })
    },
    dropTable () {
      let _this = this
      let tableName = this.operationTable[2].tableName
      this.$http.post('/relational/drop-table/', {
        username: this.GLOBAL.username,
        databaseName: this.currentDatabaseName,
        tableName: tableName,
        instanceId: 0
      }).then(response => {
        _this.loading = false
        if (response.status === 200 && response.data.success) {
          console.log(response.data)
          _this.$notify({
            // title: '保存成功',
            message: `删除表 ${tableName} 成功`,
            offset: 200
          })
          // _this.operationTable[0].tableName = ''
        } else {
          _this.$notify({
            // title: '保存成功',
            message: `删除表 ${tableName} 失败：${response.data.msg}`,
            offset: 200
          })
        }
      }, response => {
        _this.loading = false
        _this.$notify({
          message: `删除表 ${tableName} 失败：网络错误`
        })
      })
    },
    onClickDeleteDatabase () {
      this.deleteDatabaseDialogShow = true
    },
    onDeleteDatabaseSubmit () {
      let _this = this
      let databaseName = this.deleteDatabaseName
      this.deleteDatabaseDialogShow = false
      this.$http.post('/relational/drop-database/', {
        username: this.GLOBAL.username,
        databaseName: databaseName,
        instanceId: 0
      }).then(response => {
        if (response.status === 200 && response.data.success) {
          _this.getDatabaseList()
          _this.$alert('删除数据库成功')
        } else {
          _this.$alert(`删除数据库失败：${response.data.msg}`)
        }
      }, response => {
        _this.$alert('删除数据库失败：网络错误')
      })
    },
    onExecute (operationId) {
      console.log(operationId)
      switch (operationId) {
        case 0:
          // schema
          this.loading = true
          this.getDisplayTableSchema(0)
          break
        case 1:
          // delete data
          this.loading = true
          this.delete()
          break
        case 2:
          // drop table
          this.loading = true
          this.dropTable()
          break
        case 3:
          // select
          this.loading = true
          this.getDisplayTableSchema(3)
          this.getDisplayTable(3)
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
