<!doctype html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport"
          content="width=device-width, user-scalable=no, initial-scale=1.0, maximum-scale=1.0, minimum-scale=1.0">
    <meta http-equiv="X-UA-Compatible" content="ie=edge">
    <title>后台首页</title>
    <link rel="stylesheet" href="{{ url('/css/bootstrap.css') }}">
</head>
<body>
<div class="container">
    @if(Session::has('user'))
        <ul class="nav justify-content-end">
            <li class="nav-item">
                <a class="nav-link active" href="#">Active</a>
            </li>
            <li class="nav-item">
                <span class="nav-link">你好，{{ Session::get('user')['email'] }}</span>
            </li>
            <li class="nav-item">
                <a class="nav-link" href="{{ route('admin::logout') }}">退出登录</a>
            </li>
        </ul>
    @else
        <div class="row">
            <div class="col"></div>
            <div class="col"></div>
            <div class="col">你还未登陆。</div>
            <div class="col"><a href="{{ route('admin::loging') }}">点击进行登录</a></div>
        </div>
    @endif


</div>
<script src="{{ url('js/jquery.slim.min.js') }}"></script>
<script src="{{ url('js/popper.min.js') }}"></script>
<script src="{{ url('js/bootstrap.js') }}"></script>
</body>
</html>
