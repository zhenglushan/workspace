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
            <li class="nav-item mr-2">
                <a href="{{ route('admin::loging') }}" class="btn btn-outline-primary" rel="external nofollow">登陆</a>
            </li>
            <li class="nav-item">
                <a href="#" class="btn btn-outline-success" rel="external nofollow">注册</a>
            </li>
        </ul>
    </div>
</nav>
