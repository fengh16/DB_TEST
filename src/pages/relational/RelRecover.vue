<template>
  <el-row type="flex">
    <el-col :span="10">
      <div class="left-indent">
        <h1>可恢复性测试</h1>
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
          v-if="currentFocusOperation === 2"
          :data="dataTable"
          ref="displayData"
          stripe
          row-key="id"
          default-expand-all
        >
          <el-table-column
            v-for="(columnDef, index) in dataTableSchema"
            :prop="columnDef.propName"
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
  name: 'RelRecover',
  data () {
    return {
      databaseList: [],
      currentDatabaseName: '',
      operationTable: [{
        id: 0,
        title: 'dump命令备份数据',
        tableName: '',
        needParam: false
      }, {
        id: 1,
        title: 'import命令恢复数据',
        tableName: '',
        needParam: false
      }, {
        id: 2,
        title: '查看表数据',
        tableName: '',
        needParam: false
      }, {
        id: 3,
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
      return this.currentFocusOperation === 2// 只有查看表数据一项显示表头
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
            _this.$alert(`获取数据库列表失败：${response.data.msg}`)
          }
        }, function (response) {
          _this.$alert('获取数据库列表失败，请检查网络连接，稍后再试！')
        })
    },
    getDisplayTableSchema (operationId) {
      this.$http.get('/relational/view-table-schema/', {
        username: '',
        databaseName: '',
        tableName: '',
        instanceId: 0,
        encrypted: false
      }).then(
        function (response) {
          this.currentTableName = response.data.result.tableName
          this.dataTableSchema = response.data.result.schema
          if (operationId) {
            this.currentFocusOperation = operationId
            this.loading = false
          }
        }
      )
    },
    getDisplayTable (operationId) {
      this.$http.get('/relational/select/', {
        username: '',
        databaseName: '',
        tableName: '',
        instanceId: 0,
        encrypted: false
      }).then(
        function (response) {
          if (response.status === 200 && response.data.success) {
            console.log(response.data)
            this.dataTable = response.data.result
            if (operationId) {
              this.currentFocusOperation = operationId
              this.loading = false
            }
          } else {
            this.$alert(`获取数据表失败:${response.data.msg}`)
          }
        }, function (response) {
          this.$alert('获取数据表失败，请检查网络连接，稍后再试！')
        })
    },
    onExecute (operationId) {
      console.log(operationId)
      switch (operationId) {
        case 2:
          // select
          this.loading = true
          this.getDisplayTableSchema()
          this.getDisplayTable(2)
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
