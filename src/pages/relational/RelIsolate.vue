<template>
  <el-row type="flex">
    <el-col :span="10">
      <h1>数据隔离测试</h1>
      <div class="left-indent from-left margin-top">
        <el-select v-model="instanceID" placeholder="选择实例">
          <el-option
            v-for="item in instanceList"
              :key="item.value"
              :label="item.label"
              :value="item.value">
          </el-option>
        </el-select>
      </div>
        <div class="from-left left-indent margin-top">
          <el-table :data="operationTable"
                    class="margin-top"
                    stripe
                    default-expand-all>
            <el-table-column
              property="operationName"
              label="操作名称"
              align="left"
            ></el-table-column>
            <el-table-column
              property="table"
              label="表名"
              align="center">
              <template slot-scope="scope">
                <el-input v-model="tableName[scope.$index]" type="text" placeholder="输入表名"></el-input>
              </template>
            </el-table-column>
            <el-table-column
              property="operate"
              label="操作"
              align="center">
              <template slot-scope="scope">
                <el-button @click="operate(scope.$index)" type="primary" size="mini" plain>执行</el-button>
              </template>
            </el-table-column>
          </el-table>
        </div>
    </el-col>
    <el-col :span="12">
      <h1>查看测试结果</h1>
      <div>
        <div class="title-reserved" v-if="shouldDisplayTableTitle">
          <h1>表： {{displayTableTitle}}</h1>
        </div>
        <el-table :data="dataTable" v-if="currentOperationID === 5">
          <el-table-column align="center" row-key="id"
            v-for="(columnDef, index) in dataTableSchema"
              :key="index"
              :label="columnDef.columnName"
              :prop="columnDef.propName">
          </el-table-column>
        </el-table>
        <el-table :data="dataTableSchema" v-if="currentOperationID === 1">
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
  name: 'IsolateRelationPage',
  data () {
    return {
      instanceID: 1, // 实例ID，默认为1
      instanceList: [{
        value: 1,
        label: '实例一'
      }, {
        value: 2,
        label: '实例二'
      }],
      tableName: ['', '', '', '', '', ''], // 分别对应六个操作的输入表名
      operationTable: [{
        'operationName': '创建表',
        'table': '',
        'operate': '执行'
      }, {
        'operationName': '查看表信息',
        'table': '',
        'operate': '执行'
      }, {
        'operationName': '插入数据',
        'table': '',
        'operate': '执行'
      }, {
        'operationName': '更新数据',
        'table': '',
        'operate': '执行'
      }, {
        'operationName': '删除数据',
        'table': '',
        'operate': '执行'
      }, {
        'operationName': '查看数据',
        'table': '',
        'operate': '执行'
      }],
      dataTable: [{
        id: 0,
        prop1: 'row1, col1',
        prop2: 'row1, col2'
      }, {
        id: 1,
        prop1: 'row2, col1',
        prop2: 'row2, col2'
      }],
      dataTableSchema: [{
        id: 0,
        columnName: 'column1',
        propName: 'prop1'
      }, {
        id: 1,
        columnName: 'column2',
        propName: 'prop2'
      }],
      displayTableTitle: '',
      currentOperationID: -1
    }
  },
  methods: {
    operate (operationID) {
      this.currentOperationID = operationID
      switch (operationID) {
        case 0:
          // 创建表
          console.log(this.tableName[operationID])
          this.$http.post('/relational/create-table/', {
            databaseName: '',
            tableName: this.tableName[operationID],
            username: '',
            instanceID: this.instanceID
          }).then(
            function (response) {
              if (response.status === 200 && response.body.success) {
                console.log(response.body)
              } else {
                this.$alert('创建数据表失败，请稍后再试！')
              }
            }, function (response) {
              this.$alert('创建数据表失败，请检查网络连接，稍后再试！')
            }
          )
          break
        case 1:
          // 查看表信息
          console.log(this.tableName[operationID])
          this.$http.get('/relational/view-table-schema/', {
            databaseName: '',
            tableName: this.tableName[operationID],
            username: '',
            instanceID: this.instanceID,
            encrypted: false
          }).then(
            function (response) {
              if (response.status === 200 && response.body.success) {
                console.log(response.body)
                this.dataTableSchema = response.body.result.schema
                this.displayTableTitle = response.body.result.tableName
              } else {
                this.$alert('查看表信息失败，请稍后再试！')
              }
            }, function (response) {
              this.$alert('查看表信息失败，请检查网络连接，稍后再试！')
            }
          )
          break
        case 2:
          // 插入数据
          console.log(this.tableName[operationID])
          this.$http.post('/relational/insert/', {
            databaseName: '',
            tableName: this.tableName[operationID],
            username: '',
            instanceID: this.instanceID
          }).then(
            function (response) {
              if (response.status === 200 && response.body.success) {
                console.log(response.body)
              } else {
                this.$alert('插入数据失败，请稍后再试！')
              }
            }, function (response) {
              this.$alert('插入数据失败，请检查网络连接，稍后再试！')
            }
          )
          break
        case 3:
          // 更新数据
          console.log(this.tableName[operationID])
          this.$http.post('/relational/update/', {
            databaseName: '',
            tableName: this.tableName[operationID],
            username: '',
            instanceID: this.instanceID
          }).then(
            function (response) {
              if (response.status === 200 && response.body.success) {
                console.log(response.body)
              } else {
                this.$alert('更新数据失败，请稍后再试！')
              }
            }, function (response) {
              this.$alert('更新数据失败，请检查网络连接，稍后再试！')
            }
          )
          break
        case 4:
          // 删除数据
          console.log(this.tableName[operationID])
          this.$http.post('/relational/delete/', {
            databaseName: '',
            tableName: this.tableName[operationID],
            username: '',
            instanceID: this.instanceID
          }).then(
            function (response) {
              if (response.status === 200 && response.body.success) {
                console.log(response.body)
              } else {
                this.$alert('删除数据失败，请稍后再试！')
              }
            }, function (response) {
              this.$alert('删除数据失败，请检查网络连接，稍后再试！')
            }
          )
          break
        case 5:
          // 查看数据
          console.log(this.tableName[operationID])
          this.$http.get('/relational/select/', {
            databaseName: '',
            tableName: this.tableName[operationID],
            username: '',
            instanceID: this.instanceID
          }).then(
            function (response) {
              if (response.status === 200 && response.body.success) {
                console.log(response.body)
                this.dataTable = response.body.result
                this.displayTableTitle = this.tableName[operationID]
                console.log(this.dataTable)
              } else {
                this.$alert('插入数据失败，请稍后再试！')
              }
            }, function (response) {
              this.$alert('插入数据失败，请检查网络连接，稍后再试！')
            }
          )
          break
      }
    },
    getProp (index) {
      console.log('porp' + String(index))
      return 'prop' + String(index)
    }
  },
  computed: {
    shouldDisplayTableTitle () {
      return this.currentOperationID === 1 | this.currentOperationID === 5
    }
  },
  created () {
    // this.createDatabase()
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
  .margin-top {
    margin-top: 20px;
  }
  .title-reserved {
    height: 60px;
  }
</style>
