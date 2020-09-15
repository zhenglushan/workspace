# 查询语句

指定字段存在的记录总数：

db.getCollection('集合名').find({"bd_body":{'$exists':true}}).count()

