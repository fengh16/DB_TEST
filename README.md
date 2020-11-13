# DB_TEST

前端部分，使用vue构建。

使用方法：

- npm install
- npm run dev

## 整体架构

- App.vue: 整体框架，在pages中的内容会替换其中的<router-view/>
- router/index.js: 路由文件，将网址与具体的页面内容关联
- global_var.js: 一些全局变量，可以在pages/xxx.vue中用this.GLOBAL.varName访问
- src/mock: mockjs部分，用来模拟后端传递数据，可以参考data_getter.js文件
- pages：每一个页面的具体内容，在template里面写具体的内容

## 路由关系

- App.vue中，每一个el-menu-item会有index属性，两个menu会分别有一组index，比如纵向的（左侧的）菜单选择了关系数据服务，横向的菜单选择了权限管理，则路由是/relation/Auth_1
  - 代码中`<el-menu-item index="relation"><i class="el-icon-menu"></i><span slot="title">关系数据服务</span></el-menu-item>`有index为relation，横向的menu-item也有index属性
  - 具体可以看selectVertical和selectHorizontal函数
- 在router/index.js中，每一个路由路径都对应于一个component
