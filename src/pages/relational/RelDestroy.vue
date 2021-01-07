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
          <el-button type="primary" plain @click="onClickCreateDatabase">创建数据库</el-button>
          <el-button type="primary" plain @click="onClickDropDatabase">删除数据库</el-button>
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
              <el-select v-model="scope.row.tableName" placeholder="选择表名" v-if="scope.row.id !== 0">
                <el-option
                  v-for="table in tableList"
                  :key="table.label"
                  :label="table.label"
                  :value="table.value"
                ></el-option>
              </el-select>
              <el-input
                v-else
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
          v-if="currentOperationID === 1"
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
        title: '创建表',
        tableName: ''
      },{
        id: 1,
        title: '查看表信息',
        tableName: ''
      }, {
        id: 2,
        title: '删除表中所有数据',
        tableName: ''
      }, {
        id: 3,
        title: '删除表',
        tableName: ''
      }, {
        id: 4,
        title: '查看数据',
        tableName: ''
      }],
      tableList: [],
      dataTable: [],
      dataTableSchema: [],
      currentTableName: '',
      currentOperationID: -1,
      loading: false,
      deleteDatabaseDialogShow: false,
      deleteDatabaseName: '',
      schemaOperationID: 0,
      instanceID: 0,
      encodeMode: '',
      newDatabaseDialogShow: false,
      newDatabaseName: ''
    }
  },
  computed: {
    shouldDisplayTableTitle () {
      return this.currentOperationID === 1 | this.currentOperationID === 4
    },
    shouldDisplayDataTable () {
      return this.currentOperationID === 4
    }
  },
  methods: {
    dropTable () {
      let _this = this
      let tableName = this.operationTable[this.currentOperationID].tableName
      this.$http.post('/relational/drop-table/', {
        username: this.GLOBAL.username,
        databaseName: this.currentDatabaseName,
        tableName: tableName,
        instanceId: this.instanceID
      }).then(response => {
        _this.loading = false
        if (response.status === 200 && response.data.success) {
          console.log(response.data)
          _this.Relational.getTableList(_this)
          _this.operationTable.forEach((e) => {
            e.tableName = ''
          })
          _this.$alert(`删除表 ${tableName} 成功`)
          // _this.operationTable[0].tableName = ''
        } else {
          _this.$alert(`删除表 ${tableName} 失败：${response.data.msg}`)
        }
      }, response => {
        _this.loading = false
        _this.$alert(`删除表 ${tableName} 失败：网络错误`)
      })
    },
    onClickCreateDatabase () {
      this.newDatabaseDialogShow = true
    },
    onClickNewDatabaseSubmit () {
      let _this = this
      let newDatabaseName = this.newDatabaseName
      console.log(this.newDatabaseName)
      this.newDatabaseDialogShow = false
      this.$http.post('/relational/create-database/', {
        databaseName: newDatabaseName,
        username: this.GLOBAL.username,
        instanceId: this.instanceID
      }).then(response => {
        console.log(response)
        if (response.status === 200 && response.data.success) {
          // _this.GLOBAL.databaseList.push(newDatabaseName)
          // _this.databaseList.push({
          //   value: newDatabaseName,
          //   label: newDatabaseName
          // })
          _this.Relational.getDatabaseList(_this)
          _this.$alert('创建数据库成功！')
        } else {
          _this.$alert(`创建数据库失败：${response.data.msg}`)
        }
      }, response => {
        _this.$alert('创建数据库失败：网络错误')
      })
    },
    onClickDropDatabase () {
      this.Relational.dropDatabase(this)
    },
    onExecute (operationID) {
      console.log(operationID)
      this.currentOperationID = operationID
      switch (operationID) {
        case 0:
          // create table
          this.Relational.createTable(this)
          break
        case 1:
          // schema
          // this.loading = true
          this.Relational.getDisplayTableSchema(this, operationID)
          break
        case 2:
          // delete data
          // this.loading = true
          this.Relational.deleteData(this)
          break
        case 3:
          // drop table
          // this.loading = true
          this.dropTable()
          break
        case 4:
          // select
          // this.loading = true
          this.Relational.getDisplayTableSchema(this, operationID)
          this.Relational.getDisplayTable(this)
          break
      }
    }
  },
  watch: {
    currentDatabaseName: function (val) {
      this.Relational.getTableList(this)
      this.operationTable.forEach((e) => {
        e.tableName = ''
      })
    }
  },
  created () {
    this.Relational.getDatabaseList(this, true)
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
