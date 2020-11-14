<template>
  <el-row type="flex">
    <el-col :span="10">
      <div class="left-indent">
        <h1>身份认证功能测试</h1>
        <div class="from-left">
          <el-select v-model="currentDatabaseName" placeholder="选择数据库">
            <el-option
              v-for="item in databaseList"
              :key="item.value"
              :label="item.label"
              :value="item.value">
            </el-option>
          </el-select>
          <el-button type="primary" plain @click="onClickCreateDatabase">创建数据库</el-button>
          <el-button type="primary" plain @click="onDebug">DEBUG</el-button>
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
            width="120"
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
            prop="param"
            label="参数"
            align="center"
          >
            <template slot-scope="scope">
              <el-input
                v-if="scope.row.needParam"
                :placeholder="scope.row.paramHint"
                v-model="scope.row.param"
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
      <h1>查看测试结果</h1>
      <div class="title-reserved">
        <h1>{{displayTitle}}</h1>
      </div>
      <el-table
        v-if="currentFocusOperation === 5"
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
    </el-col>
  </el-row>
</template>

<script>
export default {
  name: 'RelManipulation',
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
        title: '查看表元数据',
        tableName: '',
        needParam: false
      }, {
        id: 2,
        title: '插入数据',
        tableName: '',
        needParam: false
      }, {
        id: 3,
        title: '删除数据',
        tableName: '',
        needParam: false
      }, {
        id: 4,
        title: '更新数据',
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
      displayTableTitle: ' ',
      currentFocusOperation: 0
    }
  },
  computed: {
    displayTitle () {
      return this.currentFocusOperation === 1 ? this.displayTableTitle : ''
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
    getDisplayTableSchema () {
      this.$http.get('/relational/view-table-schema/', {
        username: '',
        databaseName: '',
        tableName: '',
        instanceId: 0,
        encrypted: false
      }).then(
        function (response) {
          this.dataTableSchema = response.body.result
        }
      )
    },
    getDisplayTable () {
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
    },
    onClickCreateDatabase () {

    },
    onDebug () {
      let tableNames = []
      this.operationTable.forEach(e => {
        tableNames.push(e.tableName)
      })
      console.log(tableNames)
    },
    onExecute (operationId) {
      console.log(operationId)
      this.currentFocusOperation = operationId
      switch (operationId) {
        case 1:
          // schema
          this.getDisplayTableSchema()
          break
        case 5:
          // select
          this.displayTableTitle = this.operationTable[5].tableName
          this.getDisplayTableSchema()
          this.getDisplayTable()
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
  .title-reserved {
    height: 60px;
  }
</style>
