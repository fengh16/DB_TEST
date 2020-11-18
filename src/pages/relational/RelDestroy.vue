<template>
  <el-row type="flex">
    <el-col :span="10">
      <div class="left-indent">
        <div class="from-left">
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
        >
          <el-table-column
            prop="title"
            label="操作名称"
            align="left"
            width="190"
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
          >
            <template slot-scope="scope">
              <el-button type="primary" size="mini" plain @click="onExecute(scope.row.id)">执行</el-button>
            </template>
          </el-table-column>
        </el-table>
      </div>
    </el-col>
    <el-col :span="12" :offset="1" v-loading="loading">
      <div>
        <div class="title-reserved" v-if="shouldDisplayTableTitle">
          <h1>表： {{currentTableName}}</h1>
        </div>
        <el-table
          v-if="currentFocusOperation === 3"
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
      loading: false
    }
  },
  computed: {
    shouldDisplayTableTitle () {
      return this.currentFocusOperation === 0 | this.currentFocusOperation === 3
    }
  },
  methods: {
    getDatabaseList () {
      this.$http.get('/relational/list-database/', {
        username: ''
      }).then(
        function (response) {
          if (response.status === 200 && response.body.success) {
            console.log(response.body)
            this.databaseList = []
            response.body.result.forEach(e => {
              this.databaseList.push({
                value: e,
                label: e
              })
            })
            // if (response.body.result.length > 0) {
            //   this.currentDatabaseName = response.body.result[0]
            // }
          } else {
            this.$alert('获取数据库列表失败，请稍后再试！')
          }
        }, function (response) {
          this.$alert('获取数据库列表失败，请检查网络连接，稍后再试！')
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
          this.currentTableName = response.body.result.tableName
          this.dataTableSchema = response.body.result.schema
          if (operationId !== undefined) {
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
          if (response.status === 200 && response.body.success) {
            console.log(response.body)
            this.dataTable = response.body.result
            if (operationId !== undefined) {
              this.currentFocusOperation = operationId
              this.loading = false
            }
          } else {
            this.$alert('获取数据表失败，请稍后再试！')
          }
        }, function (response) {
          this.$alert('获取数据表失败，请检查网络连接，稍后再试！')
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
        case 3:
          // select
          this.loading = true
          this.getDisplayTableSchema()
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
.from-left {
  text-align: left;
}
.left-indent {
  margin-left: 40px;
}
</style>
