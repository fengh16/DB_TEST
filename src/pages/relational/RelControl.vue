<template>
  <el-row type="flex">
    <el-col :span="10">
      <h1>安全控制测试</h1>
      <div class="left-indent from-left margin-top">
        <el-select v-model="encodeID" placeholder="选择加密方式">
          <el-option
            v-for="item in encodeList"
              :key="item.value"
              :label="item.label"
              :value="item.value">
          </el-option>
        </el-select>
        <el-button type="primary" plain @click="onClickDecode">解密</el-button>
      </div>
        <div class="from-left left-indent margin-top">
          <el-table :data="operationTable" class="margin-top" stripe default-expand-all>
            <el-table-column property="operationName" label="操作名称" align="left"></el-table-column>
            <el-table-column property="table" label="表名" align="center">
              <template slot-scope="scope">
                <el-input v-model="tableName[scope.$index]" type="text"  placeholder="输入表名"></el-input>
              </template>
            </el-table-column>
            <el-table-column property="operate" label="操作" align="center">
              <template slot-scope="scope">
                <el-button @click="operate(scope.$index)" type="primary" size="mini" plain>执行</el-button>
              </template>
            </el-table-column>
          </el-table>
        </div>
    </el-col>
    <el-col :span="8">
      <h1>查看测试结果</h1>
        <div class="from-left left-indent margin-top">
          <el-table :data="dataTable" class="margin-top" v-if="currentOperationID === 1">
            <el-table-column :label="displayTableTitle" align="center">
              <el-table-column align="left" row-key="id"
                v-for="(columnDef, index) in dataTableSchema"
                  :key="index"
                  :label="columnDef.columnName"
                  :prop="columnDef.propName">
              </el-table-column>
            </el-table-column>
          </el-table>
          <el-table :data="dataTableSchema" class="margin-top" v-if="currentOperationID === 0">
            <el-table-column :label="displayTableTitle" align="center">
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
            </el-table-column>
          </el-table>
        </div>
    </el-col>
  </el-row>
</template>

<script>
export default {
  name: 'ControlRelationPage',
  data () {
    return {
      encodeID: 1,
      encodeMode: 'SHA1',
      encodeList: [{
        value: 0,
        label: 'SHA1'
      }, {
        value: 1,
        label: 'SHA256'
      }, {
        value: 2,
        label: 'MD2'
      }, {
        value: 3,
        label: 'MD5'
      }],
      tableName: ['', ''],
      operationTable: [{
        'operationName': '查看表信息',
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
      displayTableTitle: 'table_instance',
      currentOperationID: -1
    }
  },
  methods: {
    operate (operationID) {
      this.currentOperationID = operationID
      switch (operationID) {
        case 0:
          // 查看表信息
          console.log(this.tableName[operationID])
          this.$http.get('/relational/view-table-schema/', {
            databaseName: '',
            tableName: this.tableName[operationID],
            username: '',
            instanceID: 0,
            encrypted: this.encodeMode
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
        case 1:
          // 查看数据
          console.log(this.tableName[operationID])
          this.$http.get('/relational/select/', {
            databaseName: '',
            tableName: this.tableName[operationID],
            username: '',
            instanceID: 0,
            encrypted: this.encodeMode
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
      }
    },
    getProp (index) {
      console.log('porp' + String(index))
      return 'prop' + String(index)
    },
    onClickDecode () {
      this.encodeMode = this.encodeList[this.encodeID].label
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
</style>
