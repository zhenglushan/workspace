<!doctype html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>后台登陆页面</title>
    <style>
        #login {
            width: 100px;
            height: 100px;
            margin: 0 auto;
        }

        #double {
            padding: 10px 0;

        }
    </style>
</head>
<body>
<div id="login">
    <form action="{{route('manager::login')}}" method="post">
        @csrf
        <br/>
        <label for="username">登陆账号</label>
        <input type="text" id="username" name="username">
        <br/>
        <label for="password">登陆密码</label>
        <input type="password" id="password" name="password">
        <br/>
        <div id="double">
            <input type="submit" value="登陆">
            <input type="reset" value="重置">
        </div>
    </form>
</div>
</body>
</html>
