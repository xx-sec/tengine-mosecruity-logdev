## 文件说明

- xopt 对应的是操作xmodel的可选内容
- xcolumn 元祖对象
- xmodel 对应的是增强版本的SQL管理对象，增强table
- exutil 对应的是扩展工具
- xshow 为高级查询的思路提供，重要扩展。
  - 这里主要是为了后面服务于日志查询。

—————————————————————————————————————————————
|      xmodel                    |
|                                |
|    ————————————|————————————|  |
|    | xcolumn1  | xcolumn2   |  |   xopt
|    |—————————— |————————————|  | 
|                                | 
————— - - - - - - - - - - - -- - ————————
|    xutil  
—————————————————————————————————————————————


### 2019-4-15 
- 完成了创建表格的过程; 简单表格的基础创建; 
  - 目前只有三种类型 `str/datetime/int/text` 当然text 就跟str、datetime 一样。
 
### 2019-4-16
- 开始编写修改更新删除表格等操作。增加过滤器和中间件。 当前版本忽略触发器。

### 2019-4-19
- 预先放弃当前这个制作表格和管理表格的内容。
- 进行相关的其他设置; 重点开发show模块; 条件查询




