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
    @include('home.common.header') {{-- 顶部 --}}
    @yield('breadcrumb') {{-- 面包屑导航 --}}
    @yield('content') {{-- 主体内容区 --}}
    @include('home.common.footer') {{-- 底部 --}}
</div>
<script src="{{ url('js/jquery.slim.min.js') }}"></script>
<script src="{{ url('js/popper.min.js') }}"></script>
<script src="{{ url('js/bootstrap.js') }}"></script>
</body>
</html>
