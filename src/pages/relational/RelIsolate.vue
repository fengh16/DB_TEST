<template>
  <el-row type="flex">
    <el-col :span="10">
      <div class="left-indent margin-top">
        <h1>数据隔离测试</h1>
        <div class="from-left">
          <p class="header-title">数据服务实例</p>
          <el-select v-model="instanceID" placeholder="选择实例">
            <el-option
              v-for="item in instanceList"
              :key="item.value"
              :label="item.label"
              :value="item.value">
            </el-option>
          </el-select>
        </div>
          <el-table :data="operationTable"
                    class="margin-top"
                    stripe
                    default-expand-all
          >
            <el-table-column
              property="title"
              label="操作名称"
              align="left"
              width="100"
            ></el-table-column>
            <el-table-column
              property="table"
              label="表名"
              align="center">
              <template slot-scope="scope">
<!--                <el-input v-model="tableName[scope.$index]" type="text" placeholder="输入表名"></el-input>-->
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
                ></el-input>
              </template>
            </el-table-column>
            <el-table-column
              property="operate"
              label="操作"
              align="center"
              width="80">
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
        <div class="title-reserved" v-if="shouldDisplayTableTitle">
          <h1>表： {{currentTableName}}</h1>
        </div>
        <el-table
          v-if="currentOperationID === 5"
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
<!--        <el-table :data="dataTable" v-if="currentOperationID === 5">-->
<!--          <el-table-column align="center" row-key="id"-->
<!--            v-for="(columnDef, index) in dataTableSchema"-->
<!--              :key="index"-->
<!--              :label="columnDef.columnName"-->
<!--              :prop="columnDef.propName">-->
<!--          </el-table-column>-->
<!--        </el-table>-->
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
      instanceID: 0, // 实例ID，默认为1
      instanceList: [{
        value: 0,
        label: '实例一'
      }, {
        value: 1,
        label: '实例二'
      }],
      tableList: [],
      tableName: ['', '', '', '', '', ''], // 分别对应六个操作的输入表名
      operationTable: [{
        id: 0,
        title: '创建表',
        tableName: ''
      }, {
        id: 1,
        title: '查看表信息',
        tableName: ''
      }, {
        id: 2,
        title: '插入数据',
        tableName: ''
      }, {
        id: 3,
        title: '更新数据',
        tableName: ''
      }, {
        id: 4,
        title: '删除数据',
        tableName: ''
      }, {
        id: 5,
        title: '查看数据',
        tableName: ''
      }],
      databaseList: [],
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
      currentTableName: '',
      currentOperationID: -1,
      currentDatabaseName: '',
      schemaOperationID: 1,
      encodeMode: ''
    }
  },
  methods: {
    operate (operationID) {
      // let _this = this
      this.currentOperationID = operationID
      switch (operationID) {
        case 0:
          // 创建表
          console.log(this.tableName[operationID])
          this.GLOBAL.createTable(this)
          break
        case 1:
          // 查看表信息
          console.log(this.tableName[operationID])
          this.GLOBAL.getDisplayTableSchema(this, operationID)
          break
        case 2:
          // 插入数据
          console.log(this.tableName[operationID])
          this.GLOBAL.insert(this)
          break
        case 3:
          // 更新数据
          console.log(this.tableName[operationID])
          this.GLOBAL.update(this)
          break
        case 4:
          // 删除数据
          console.log(this.tableName[operationID])
          this.GLOBAL.deleteData(this)
          break
        case 5:
          // 查看数据
          this.GLOBAL.getDisplayTableSchema(this, operationID)
          this.GLOBAL.getDisplayTable(this)
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
  watch: {
    instanceID: function (val) {
      this.GLOBAL.getDatabaseList(this, true)
      this.operationTable.forEach((e) => {
        e.tableName = ''
      })
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
  .title-reserved {
    height: 60px;
  }
  .header-title {
    display: inline-block;
    border-left: 4px solid #409eff;
    margin-right: 20px;
    padding-left: 8px;
  }
</style>
