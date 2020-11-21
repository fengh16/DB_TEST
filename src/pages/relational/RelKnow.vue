<template>
  <div>
    <h1>知情权测试</h1>
    <div class="left-indent">
      <el-table :data="relation_info">
        <el-table-column
          property="item"
          label="属性"
          width="300"
          align="left">

        </el-table-column>
        <el-table-column
          property="info"
          label="值"
          align="left">

        </el-table-column>
      </el-table>
    </div>
  </div>
</template>

<script>
export default {
  name: 'KnowRelationPage',
  data () {
    return {
      relation_info: [{
        item: 'IP地址',
        info: '166.111.80.113'
      }, {
        item: 'MAC地址',
        info: '80:18:44:f4:07:6e'
      }, {
        item: '服务程序位置',
        info: '/mnt/rel-service/3307/'
      }, {
        item: '数据存储位置',
        info: '/mnt/rel-service/3307/data/'
      }, {
        item: '数据量',
        info: '4.3 GB'
      }, {
        item: '服务器总空间',
        info: '38 GB'
      }, {
        item: '服务器可用空间',
        info: '9.1 GB'
      }]
    }
  },
  methods: {
    getRelationalInfo () {
      this.relation_info = []
      this.$http.get('/relational/description').then(
        function (response) {
          if (response.status === 200 && response.body.success) {
            console.log(response.body)
            for (let t in response.body.result) {
              this.relation_info.push({
                'item': t,
                'info': response.body.result[t]
              })
            }
          } else {
            this.$alert('获取数据服务信息失败，请稍后再试！')
          }
        }, function (response) {
          this.$alert('获取数据服务信息失败，请检查网络连接，稍后再试！')
        })
    }
  },
  created () {
    // this.getRelationalInfo()
  }
}
</script>

<style scoped>
  .left-indent {
    margin-left: 40px;
  }
</style>
