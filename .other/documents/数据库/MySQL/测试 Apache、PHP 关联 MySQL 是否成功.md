测试 Apache、PHP 关联 MySQL 是否成功：

```shell
[root@localhost ~]# gedit /zls/server/apache/htdocs/mysqlzls.php
```

在文件中增加如下代码：

```php
<?php
    $mysqli = new mysqli("127.0.0.1", "root", "root");
    if (!$mysqli) {
        echo "database connection error";
    } else {
        echo "php connection mysql successful";
    }
    $mysqli->close();
?>
```
然后在浏览器输入 http://127.0.0.1/mysqlzls.php 如果浏览器输出 “php connection mysql successful” 说明关联成功。

