<template>
  <el-row type="flex">
    <el-col :span="10">
      <div class="left-indent">
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
            width="220"
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
        title: 'dump命令备份所有数据库的结构和数据',
        tableName: '',
        needParam: false
      }, {
        id: 1,
        title: 'import命令恢复',
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
          if (response.status === 200 && response.body.success) {
            console.log(response.body)
            this.dataTable = response.body.result
            if (operationId) {
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
        case 2:
          // select
          this.loading = true
          this.getDisplayTableSchema()
          this.getDisplayTable(2)
          break
      }
    }

  }

}
</script>

<style scoped>
.left-indent {
  margin-left: 40px;
}
</style>
