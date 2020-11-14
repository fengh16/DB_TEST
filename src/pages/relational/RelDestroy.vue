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
    <el-col :span="12" :offset="1">
      <h1>{{displayTableTitle}}</h1>
      <el-table :data="dataTable"
                ref="displayData"
                stripe
                row-key="id"
                default-expand-all
      >
        <el-table-column
          v-for="(columnDef) in dataTableSchema"
          :prop="columnDef.propName"
          :label="columnDef.columnName"
          :key="columnDef.id"
          align="left"
        >

        </el-table-column>
      </el-table>
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
      dataTableSchema: [{
        id: 0,
        columnName: 'column1',
        propName: 'prop1'
      }, {
        id: 1,
        columnName: 'column2',
        propName: 'prop2'
      }],
      displayTableTitle: 'industry_table_2'
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
          } else {
            this.$alert('获取数据库列表失败，请稍后再试！')
          }
        }, function (response) {
          this.$alert('获取数据库列表失败，请检查网络连接，稍后再试！')
        })
    },
    /*    getDisplayTable () {
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
          } else {
            this.$alert('获取数据表失败，请稍后再试！')
          }
        }, function (response) {
          this.$alert('获取数据表失败，请检查网络连接，稍后再试！')
        })
    }, */
    onClickDeleteDatabase () {

    },
    onExecute (operationId) {
      console.log(operationId)
      switch (operationId) {
        /*        case 5:
          this.getDisplayTable() */
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
