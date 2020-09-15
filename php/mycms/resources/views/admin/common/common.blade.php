<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no">
    <title>@yield('title')</title>
    <meta name="keywords" content="@yield('keywords')">
    <meta name="description" content="@yield('description')">
    <link rel="stylesheet" href="{{ url('/css/bootstrap.css') }}">
</head>
<body>
<div class="container">
    <nav class="navbar navbar-light bg-light">
        <div class="container">
            <ul class="nav navbar">
                <li class="nav-item active">
                    <a href="/" class="nav-link " rel="external nofollow">首页</a>
                </li>
                @foreach($cates as $cate)
                    @if($loop->index <= 7)
                        <li class="nav-item">
                            <a href="{{ route('home::cate::list', [$cate['id'],1]) }}" class="nav-link"
                               target="_blank">{{ $cate['name'] }}</a>
                        </li>
                    @endif
                @endforeach
            </ul>
            <ul class="nav navbar">
                @if(Session::has('user'))
                    <div class="row">
                        <div class="col"></div>
                        <div class="col"></div>
                        <div class="col">你好，{{ Session::get('user')['email'] }}</div>
                        <div class="col"><a href="{{ route('admin::logout') }}">退出登录</a></div>
                    </div>
                    <div class="row" style="height: 100%">
                        <div class="col-2 m-lg-5">
                            <div class="row">文章管理</div>
                            <div class="row">文章列表</div>
                            <div class="row">增加文章</div>
                        </div>
                        <div class="col-10"></div>
                    </div>
                @else
                    <div class="row">
                        <div class="col"></div>
                        <div class="col"></div>
                        <div class="col">你还未登陆。</div>
                        <div class="col"><a href="{{ route('admin::loging') }}">点击进行登录</a></div>
                    </div>
                @endif
            </ul>
        </div>
    </nav>
    {{-- 左侧菜单 --}}
    @yield('content') {{-- 主体内容区 --}}
    <div class="footer" style="width: 100%;height: 300px;padding-top: 50px;">
        <div class="container">
            <h1 style="color: #FFFFFF;font-size: 1.5em;">Articles</h1>
        </div>
    </div>
</div>
<script src="{{ url('js/jquery.slim.min.js') }}"></script>
<script src="{{ url('js/popper.min.js') }}"></script>
<script src="{{ url('js/bootstrap.js') }}"></script>
</body>
</html>
