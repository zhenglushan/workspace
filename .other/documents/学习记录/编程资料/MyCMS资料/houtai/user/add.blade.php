<!doctype html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport"
          content="width=device-width, user-scalable=no, initial-scale=1.0, maximum-scale=1.0, minimum-scale=1.0">
    <meta http-equiv="X-UA-Compatible" content="ie=edge">
    <title>添加用户信息</title>
</head>
<body>
<div style="margin: 0 auto;">
<form method="post" action="{{ route('user.store') }}">
    @csrf
    <br>
    <label for="username">账号</label>
    <input id="username" name="username" value="orange">
    <br>
    <label for="passwd">密码</label>
    <input id="passwd" name="passwd" type="password" value="123456">
    <br>
    <input type="submit" value="提交">
</form>
</div>
</body>
</html>
