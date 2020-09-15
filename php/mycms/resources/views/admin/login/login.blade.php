<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta http-equiv="X-UA-Compatible" content="ie=edge">
    <title>后台登陆页面</title>
    <link rel="stylesheet" href="{{ url('/css/bootstrap.css') }}">
</head>
<body>
<div class="container p-5 w-100">
    <form action="{{ route('admin::loginp') }}" method="post">
        @csrf
        <div class="form-group">
            <label for="email">邮箱：</label>
            <input type="email" class="form-control col-4" id="email" name="email"
                   oninvalid="setCustomValidity('您还没有输入您的邮箱地址呢！');" oninput="setCustomValidity('');"
                   aria-describedby="emailHelp" required placeholder="请输入您的邮箱地址">
            <small id="emailHelp" class="form-text text-muted">我们永远不会与其他人共享您的电子邮件。We'll never share your email with
                anyone else.</small>
        </div>
        <div class="form-group">
            <label for="pwd">密码：</label>
            <input type="password" class="form-control col-4" id="pwd" oninvalid="setCustomValidity('您还没有输入您的登陆密码呢！');"
                   oninput="setCustomValidity('');" name="pwd" required placeholder="请输入您的登陆密码">
        </div>
        <div class="form-group">
            <label for="verify">验证码：</label>
            <input type="text" class="form-control col-4" id="verify" oninvalid="setCustomValidity('您还没有输入验证码呢！');"
                   oninput="setCustomValidity('');" name="verify" required placeholder="请输入您的验证码">
            <img class="col-2" src="{{ route('admin::verify') }}" alt=""
                 onclick="javascript: this.src='{{ route("admin::verify") }}?' + Math.random();">
        </div>
        <div class="form-group form-check">
            <input type="checkbox" class="form-check-input" id="exampleCheck1">
            <label class="form-check-label" for="exampleCheck1">Check me out</label>
        </div>
        <button type="submit" class="btn btn-primary">登录</button>
    </form>
</div>
<script src="{{ url('js/jquery.slim.min.js') }}"></script>
<script src="{{ url('js/popper.min.js') }}"></script>
<script src="{{ url('js/bootstrap.js') }}"></script>
</body>
</html>
