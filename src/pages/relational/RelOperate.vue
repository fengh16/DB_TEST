<template>
  <el-row type="flex">
    <el-col :span="10">
      <div class="left-indent">
        <h1>可操作性测试</h1>
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
          <el-button type="primary" plain @click="onClickCreateDatabase">创建数据库</el-button>
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
            width="100"
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
<!--          <el-table-column-->
<!--            prop="param"-->
<!--            label="参数"-->
<!--            align="center"-->
<!--            width="200"-->
<!--          >-->
<!--            <template slot-scope="scope">-->
<!--              <el-input-->
<!--                v-if="scope.row.needParam"-->
<!--                :placeholder="scope.row.paramHint"-->
<!--                v-model="scope.row.param"-->
<!--                clearable>-->
<!--              </el-input>-->
<!--            </template>-->
<!--          </el-table-column>-->
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
      <el-dialog title="创建数据库" :visible.sync="newDatabaseDialogShow">
        <el-form>
          <el-form-item label="数据库名">
            <el-input v-model="newDatabaseName" autocomplete="off" placeholder="输入新数据库名称"></el-input>
          </el-form-item>
        </el-form>
        <div slot="footer" class="dialog-footer">
          <el-button @click="newDatabaseDialogShow=false">取 消</el-button>
          <el-button type="primary" @click="onClickNewDatabaseSubmit">创 建</el-button>
        </div>
      </el-dialog>
      <el-dialog title="信息嵌入" :visible.sync="embeddingDialogShow">
        <el-form>
          <el-form-item label="要嵌入的信息">
            <el-input v-model="embeddingString" autocomplete="off" placeholder="输入要嵌入的信息"></el-input>
          </el-form-item>
        </el-form>
        <div slot="footer" class="dialog-footer">
          <el-button @click="embeddingDialogShow=false">取 消</el-button>
          <el-button type="primary" @click="onClickEmbeddingSubmit">执 行</el-button>
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
          v-if="currentFocusOperation === 1"
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
  name: 'RelOperate',
  data () {
    return {
      databaseList: [],
      currentDatabaseName: '',
      operationTable: [{
        id: 0,
        title: '创建表',
        tableName: '',
        needParam: false,
        param: '',
        paramHint: ''
      }, {
        id: 1,
        title: '查看表信息',
        tableName: '',
        needParam: false
      }, {
        id: 2,
        title: '插入数据',
        tableName: '',
        needParam: false
      }, {
        id: 3,
        title: '更新数据',
        tableName: '',
        needParam: false
      }, {
        id: 4,
        title: '删除数据',
        tableName: '',
        needParam: false
      }, {
        id: 5,
        title: '查看数据',
        tableName: '',
        needParam: false
      }, {
        id: 6,
        title: '信息嵌入',
        tableName: '',
        needParam: true,
        param: '',
        paramHint: '输入要嵌入的信息'
      }],
      dataTable: [],
      dataTableSchema: [],
      currentTableName: '',
      currentFocusOperation: 0,
      loading: false,
      newDatabaseName: '',
      newDatabaseDialogShow: false,
      embeddingString: '',
      embeddingDialogShow: false
    }
  },
  computed: {
    shouldDisplayTableTitle () {
      return this.currentFocusOperation === 1 | this.currentFocusOperation === 5 | this.currentFocusOperation === 6
    },
    shouldDisplayDataTable () {
      return this.currentFocusOperation === 5 || this.currentFocusOperation === 6
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
            if (operationId === 1) {
              _this.currentFocusOperation = operationId
              _this.loading = false
            }
          } else {
            if (operationId === 1) {
              _this.$alert(`获取表信息失败：${response.data.msg}`)
              _this.loading = false
            }
          }
        }, response => {
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
            _this.$alert(`查看数据失败：${response.data.msg}`)
            _this.loading = false
          }
        }, function (response) {
          _this.$alert('查看数据失败，请检查网络连接，稍后再试！')
          _this.loading = false
        })
    },
    onClickNewDatabaseSubmit () {
      let _this = this
      let newDatabaseName = this.newDatabaseName
      console.log(this.newDatabaseName)
      this.newDatabaseDialogShow = false
      this.$http.post('/relational/create-database/', {
        databaseName: newDatabaseName,
        username: this.GLOBAL.username,
        instanceId: 0
      }).then(response => {
        console.log(response)
        if (response.status === 200 && response.data.success) {
          _this.GLOBAL.databaseList.push(newDatabaseName)
          _this.databaseList.push({
            value: newDatabaseName,
            label: newDatabaseName
          })
          _this.$alert('创建数据库成功！')
        } else {
          _this.$alert(`创建数据库失败：${response.data.result}`)
        }
      }, response => {
        _this.$alert('创建数据库失败：网络错误')
      })
    },
    onClickEmbeddingSubmit () {
      this.embeddingDialogShow = false
      this.loading = true
      this.getDisplayTableSchema(6)
      this.$http.get('/relational/select-embedding/', {
        params: {
          username: this.GLOBAL.username,
          databaseName: this.currentDatabaseName,
          tableName: this.operationTable[6].tableName,
          instanceId: 0,
          encrypted: '',
          embedding: this.embeddingString
        }
      }).then((response) => {
        if (response.status === 200 && response.data.success) {
          console.log(response.data)
          this.dataTable = response.data.result
          this.currentFocusOperation = 6
          this.loading = false
          console.log(this.currentFocusOperation, this.dataTable, this.currentTableName)
        } else {
          this.$alert('获取数据表失败，请稍后再试！')
        }
      }, (response) => {
        this.loading = false
        this.$alert('获取数据表失败，请检查网络连接，稍后再试！')
      })
    },
    onClickCreateDatabase () {
      this.newDatabaseDialogShow = true
    },
    onDebug () {
      let tableNames = []
      this.operationTable.forEach(e => {
        tableNames.push(e.tableName)
      })
      console.log(tableNames)
    },
    createTable () {
      let _this = this
      console.log(this.GLOBAL.username, this.currentDatabaseName, this.operationTable[0])
      this.$http.post('/relational/create-table/', {
        username: this.GLOBAL.username,
        databaseName: this.currentDatabaseName,
        tableName: this.operationTable[0].tableName,
        instanceId: 0
      }).then(response => {
        _this.loading = false
        if (response.status === 200 && response.data.success) {
          console.log(response.data)
          _this.$notify({
            // title: '保存成功',
            message: `创建表 ${_this.operationTable[0].tableName} 成功`,
            offset: 200
          })
          // _this.operationTable[0].tableName = ''
        } else {
          _this.$notify({
            // title: '保存成功',
            message: `创建表 ${_this.operationTable[0].tableName} 失败：${response.data.result}`,
            offset: 200
          })
        }
      }, response => {
        this.loading = false
        _this.$notify({
          // title: '保存成功',
          message: `创建表 ${_this.operationTable[0].tableName} 失败：网络错误`,
          offset: 200
        })
      })
    },
    insert () {
      let _this = this
      let tableName = this.operationTable[2].tableName
      this.$http.post('/relational/insert/', {
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
            message: `向表 ${tableName} 插入数据成功`,
            offset: 200
          })
          // _this.operationTable[0].tableName = ''
        } else {
          _this.$notify({
            // title: '保存成功',
            message: `向表 ${tableName} 插入数据失败：${response.data.result}`,
            offset: 200
          })
        }
      }, response => {
        _this.loading = false
        _this.$notify({
          message: `向表 ${tableName} 插入数据失败：网络错误`
        })
      })
    },
    update () {
      let _this = this
      let tableName = this.operationTable[3].tableName
      this.$http.post('/relational/update/', {
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
            message: `更新表 ${tableName} 数据成功`,
            offset: 200
          })
          // _this.operationTable[0].tableName = ''
        } else {
          _this.$notify({
            // title: '保存成功',
            message: `更新表 ${tableName} 数据失败：${response.data.result}`,
            offset: 200
          })
        }
      }, response => {
        _this.loading = false
        _this.$notify({
          message: `更新表 ${tableName} 数据失败：网络错误`
        })
      })
    },
    delete () {
      let _this = this
      let tableName = this.operationTable[4].tableName
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
            message: `删除表 ${tableName} 数据成功`,
            offset: 200
          })
          // _this.operationTable[0].tableName = ''
        } else {
          _this.$notify({
            // title: '保存成功',
            message: `删除表 ${tableName} 数据失败：${response.data.result}`,
            offset: 200
          })
        }
      }, response => {
        _this.loading = false
        _this.$notify({
          message: `删除表 ${tableName} 数据失败：网络错误`
        })
      })
    },
    onExecute (operationId) {
      console.log(operationId)
      switch (operationId) {
        case 0:
          // create table
          this.loading = true
          this.createTable()
          break
        case 1:
          // schema
          this.loading = true
          this.dataTableSchema = []
          this.getDisplayTableSchema(1)
          break
        case 2:
          // insert
          this.loading = true
          this.insert()
          break
        case 3:
          // update
          this.loading = true
          this.update()
          break
        case 4:
          // delete
          this.loading = true
          this.delete()
          break
        case 5:
          // select
          this.loading = true
          this.dataTableSchema = []
          this.dataTable = []
          this.getDisplayTableSchema(5)
          this.getDisplayTable(5)
          break
        case 6:
          // select embedding
          this.embeddingDialogShow = true
          // this.getDisplayTableSchema(6)
          // this.getDisplayTable(6)
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
  .title-reserved {
    height: 60px;
  }
  .header-title {
    display: inline-block;
    border-left: 4px solid #409eff;
    margin-right: 20px;
    padding-left: 8px;
  }
</style>
