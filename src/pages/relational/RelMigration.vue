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
        needParam: false
      }, {
        id: 1,
        title: 'import命令导入数据',
        tableName: '',
        needParam: false
      }, {
        id: 2,
        title: '查询语句导出数据',
        tableName: '',
        needParam: false
      }, {
        id: 3,
        title: 'dump命令导出数据',
        tableName: '',
        needParam: false
      }, {
        id: 4,
        title: '查看表数据',
        tableName: '',
        needParam: false
      }, {
        id: 5,
        title: '查看文件',
        tableName: '',
        needParam: false
      }],
      dataTable: [],
      dataTableSchema: [],
      currentTableName: '',
      currentFocusOperation: 0,
      loading: false
    }
  },
  computed: {
    shouldDisplayTableTitle () {
      return this.currentFocusOperation === 6// 只有查看表数据一项显示表头
    },
    shouldDisplayDataTable () {
      return this.currentFocusOperation === 4
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
            _this.$alert('获取表信息失败：没有权限')
            _this.loading = false
          }
        }, response => {
          _this.$alert('获取表信息失败：网络错误')
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
            _this.$alert('查看数据失败：没有权限')
            _this.loading = false
          }
        }, function (response) {
          _this.$alert('查看数据失败，请检查网络连接，稍后再试！')
          _this.loading = false
        })
    },
    onExecute (operationId) {
      console.log(operationId)
      switch (operationId) {
        case 4:
          // select
          this.loading = true
          this.getDisplayTableSchema(4)
          this.getDisplayTable(4)
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
</style>
