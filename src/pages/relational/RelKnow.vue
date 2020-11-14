<template>
  <div>
    <el-table :data="relation_info" border>
      <el-table-column property="item" label="项目" fixed width="100px"></el-table-column>
      <el-table-column property="info" label="信息"></el-table-column>
    </el-table>
  </div>
</template>

<script>
export default {
  name: 'KnowRelationPage',
  data () {
    return {
      relation_info: []
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
    this.getRelationalInfo()
  }
}
</script>

<style scoped>

</style>
