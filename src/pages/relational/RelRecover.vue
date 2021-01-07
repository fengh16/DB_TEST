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
            label="表名"
            align="center"
          >
            <template slot-scope="scope">
              <el-select v-model="scope.row.tableName" placeholder="选择表名" v-if="scope.row.needTable">
                <el-option
                  v-for="table in tableList"
                  :key="table.label"
                  :label="table.label"
                  :value="table.value"
                ></el-option>
              </el-select>
<!--              <el-input-->
<!--                placeholder="输入表名"-->
<!--                v-model="scope.row.tableName"-->
<!--                clearable>-->
<!--              </el-input>-->
            </template>
          </el-table-column>
          <el-table-column
            prop="filepath"
            label="文件名"
            align="center"
          >
            <template slot-scope="scope">
              <el-input
                v-if="scope.row.needFilepath"
                placeholder="输入文件名"
                v-model="scope.row.filepath"
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
<!--      <el-dialog title="dump命令备份数据" :visible.sync="filenameDialogShow_0">-->
<!--        <el-form>-->
<!--          <el-form-item label="文件路径">-->
<!--            <el-input v-model="filenameString" autocomplete="off" placeholder="输入文件路径"></el-input>-->
<!--          </el-form-item>-->
<!--        </el-form>-->
<!--        <div slot="footer" class="dialog-footer">-->
<!--          <el-button @click="filenameDialogShow_0=false">取 消</el-button>-->
<!--          <el-button type="primary" @click="exportDataShell">执 行</el-button>-->
<!--        </div>-->
<!--      </el-dialog>-->
<!--      <el-dialog title="import命令恢复数据" :visible.sync="filenameDialogShow_1">-->
<!--        <el-form>-->
<!--          <el-form-item label="文件路径">-->
<!--            <el-input v-model="filenameString" autocomplete="off" placeholder="输入文件路径"></el-input>-->
<!--          </el-form-item>-->
<!--        </el-form>-->
<!--        <div slot="footer" class="dialog-footer">-->
<!--          <el-button @click="filenameDialogShow_1=false">取 消</el-button>-->
<!--          <el-button type="primary" @click="importDataShell">执 行</el-button>-->
<!--        </div>-->
<!--      </el-dialog>-->
<!--      <el-dialog title="查看文件" :visible.sync="filenameDialogShow_3">-->
<!--        <el-form>-->
<!--          <el-form-item label="文件路径">-->
<!--            <el-input v-model="filenameString" autocomplete="off" placeholder="输入文件路径"></el-input>-->
<!--          </el-form-item>-->
<!--        </el-form>-->
<!--        <div slot="footer" class="dialog-footer">-->
<!--          <el-button @click="filenameDialogShow_3=false">取 消</el-button>-->
<!--          <el-button type="primary" @click="getFile">执 行</el-button>-->
<!--        </div>-->
<!--      </el-dialog>-->
    </el-col>
    <el-col :span="12" :offset="1" v-loading="loading">
      <h1>查看测试结果</h1>
      <div>
        <div class="title-reserved" v-if="shouldDisplayTableTitle">
          <h1>表： {{currentTableName}}</h1>
        </div>
        <el-table
          v-if="currentOperationID === 2"
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
      <div class="title-reserved" v-if="shouldDisplayFileData">
        <h1>文件： {{filenameString}}</h1>
      </div>
      <el-input v-if="shouldDisplayFileData"
                type="textarea"
                :rows="20"
                placeholder=""
                v-model="fileContent"
                :readonly="true"
                :autosize="false"
                resize="none">
      </el-input>
    </el-col>
  </el-row>
</template>

<script>
export default {
  name: 'RelRecover',
  data () {
    return {
      databaseList: [],
      tableList: [],
      currentDatabaseName: '',
      operationTable: [{
        id: 0,
        title: 'dump命令备份数据',
        tableName: '',
        needTable: true,
        filepath: '',
        needFilepath: true
      }, {
        id: 1,
        title: 'import命令恢复数据',
        tableName: '',
        needTable: true,
        filepath: '',
        needFilepath: true
      }, {
        id: 2,
        title: '查看表数据',
        tableName: '',
        needTable: true,
        filepath: '',
        needFilepath: false
      }, {
        id: 3,
        title: '查看文件',
        tableName: '',
        needTable: false,
        filepath: '',
        needFilepath: true
      }, {
        id: 4,
        title: '删除表数据',
        tableName: '',
        needTable: true,
        filepath: '',
        needFilepath: false
      }],
      dataTable: [],
      dataTableSchema: [],
      currentTableName: '',
      currentOperationID: 0,
      loading: false,
      filenameDialogShow_0: false, // 每个对话框的显示由单独的变量控制
      filenameDialogShow_1: false,
      filenameDialogShow_3: false,
      schemaOperationID: -1,
      filenameString: '',
      fileContent: '',
      instanceID: 0,
      encodeMode: ''
    }
  },
  computed: {
    shouldDisplayTableTitle () {
      return this.currentOperationID === 2
    },
    shouldDisplayFileData  () {
      return this.currentOperationID === 3
    }
  },
  methods: {
    onExecute (operationID) {
      console.log(operationID)
      this.currentOperationID = operationID
      switch (operationID) {
        case 0:
          // export (shell)
          // this.currentOperationID = operationID
          // this.filenameDialogShow_0 = true
          this.Relational.exportDataShell(this)
          break
        case 1:
          // import (shell)
          // this.currentOperationID = operationID
          // this.filenameDialogShow_1 = true
          this.Relational.importDataShell(this)
          break
        case 2:
          // select
          this.loading = true
          this.Relational.getDisplayTableSchema(this, operationID)
          this.Relational.getDisplayTable(this)
          break
        case 3:
          // select file
          this.GLOBAL.getFile(this)
          // this.currentOperationID = operationID
          // this.filenameDialogShow_3 = true
          break
        case 4:
          // delete table data
          this.Relational.deleteData(this)
          break
      }
    }
  },
  watch: {
    currentDatabaseName: function (val) {
      this.Relational.getTableList(this)
      this.operationTable.forEach((e) => {
        e.tableName = ''
        e.filepath = ''
      })
    }
  },
  created () {
    this.Relational.getDatabaseList(this)
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
  .file-text{
    margin-top: 20px;
  }
</style>
