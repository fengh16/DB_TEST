<template>
  <el-row type="flex">
    <el-col :span="10">
      <div class="left-indent">
        <h1>安全控制测试</h1>
        <div class="from-left margin-top">
          <p class="header-title">防篡改加密</p>
          <el-select v-model="encodeID" placeholder="选择加密方式">
            <el-option
              v-for="item in encodeList"
              :key="item.value"
              :label="item.label"
              :value="item.value">
            </el-option>
          </el-select>
<!--          <el-button type="primary" plain @click="onClickDecode">解密</el-button>-->
        </div>
        <el-table :data="operationTable" class="margin-top" stripe default-expand-all>
          <el-table-column property="title" label="操作名称" align="left" width="100"></el-table-column>
          <el-table-column property="tableName" label="表名" align="center">
            <template slot-scope="scope">
              <el-select v-model="scope.row.tableName" placeholder="选择表名">
                <el-option
                  v-for="table in tableList"
                  :key="table.label"
                  :label="table.label"
                  :value="table.value"
                ></el-option>
              </el-select>
<!--              <el-input v-model="tableName[scope.$index]" type="text"  placeholder="输入表名"></el-input>-->
            </template>
          </el-table-column>
          <el-table-column property="operate" label="操作" align="center" width="80">
            <template slot-scope="scope">
              <el-button @click="operate(scope.$index)" type="primary" size="mini" plain>执行</el-button>
            </template>
          </el-table-column>
        </el-table>
      </div>
    </el-col>
    <el-col :span="12" :offset="1">
      <h1>查看测试结果</h1>
      <div>
        <div class="title-reserved" v-if="currentOperationID === 0 || currentOperationID === 1">
          <h1>表： {{currentTableName}}</h1>
        </div>
        <el-table
          v-if="currentOperationID === 1"
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
        <el-table :data="dataTableSchema" v-if="currentOperationID === 0">
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
  name: 'ControlRelationPage',
  data () {
    return {
      encodeID: 0,
      encodeMode: '',
      encodeList: [{
        value: 0,
        label: '不加密',
        encodeMethod: ''
      }, {
        value: 1,
        label: 'SHA1',
        encodeMethod: 'SHA1'
      }, {
        value: 2,
        label: 'SHA256',
        encodeMethod: 'SHA256'
      }, {
        value: 3,
        label: 'MD2',
        encodeMethod: 'MD2'
      }, {
        value: 4,
        label: 'MD5',
        encodeMethod: 'MD5'
      }],
      tableName: ['', ''],
      operationTable: [{
        id: 0,
        title: '查看表信息',
        tableName: ''
      }, {
        id: 1,
        title: '查看数据',
        tableName: ''
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
      tableList: [],
      databaseList: [],
      currentTableName: '',
      currentOperationID: -1,
      schemaOperationID: 0
    }
  },
  methods: {
    operate (operationID) {
      this.currentOperationID = operationID
      switch (operationID) {
        case 0:
          // 查看表信息
          console.log(this.tableName[operationID])
          this.GLOBAL.getDisplayTableSchema(this, operationID)
          break
        case 1:
          // 查看数据
          console.log(this.tableName[operationID])
          this.encodeMode = ''
          this.GLOBAL.getDisplayTableSchema(this, operationID)
          this.encodeMode = this.encodeList[this.encodeID].encodeMethod
          this.GLOBAL.getDisplayTable(this)
          break
      }
    },
    getProp (index) {
      console.log('porp' + String(index))
      return 'prop' + String(index)
    }
  },
  watch: {
    encodeID: function (val) {
      this.encodeMode = this.encodeList[val].encodeMethod
    }
  },
  created () {
    this.GLOBAL.getDatabaseList(this, true)
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
  .header-title {
    display: inline-block;
    border-left: 4px solid #409eff;
    margin-right: 20px;
    padding-left: 8px;
  }
</style>
