@extends('home.common.base')
{{-- TDK 不要留有空格和换行 --}}
@section('title'){{ ($article['title']) }}@endsection

@section('keywords'){{ $article['keywords'] }}@endsection

@section('description'){{ $article['description'] }}@endsection

@section('content')
    <nav aria-label="breadcrumb">
        <ol class="breadcrumb">
            <li class="breadcrumb-item"><a href="/">Home</a></li>
            <li class="breadcrumb-item"><a
                    href="{{ route('home::cate::list', [$category['id'],1]) }}">{{ $category['name'] }}</a></li>
            <li class="breadcrumb-item active" aria-current="page"><a
                    href="{{ URL::current() }}">{{ $article['title'] }}</a></li>
        </ol>
    </nav>
    <div class="row"><h1>{{ $article['title'] }}</h1></div>
    <div class="row badge-danger ">
        <div class="col">分类：<a class="text-white"
                               href="{{ route('home::cate::list', [$category['id'],1]) }}">{{ $category['name'] }}</a>
        </div>
        @foreach($tags as $tag)
            <div class="col"><a class="text-white"
                                href="{{ route('home::tag::list', [$tag['id'], 1]) }}">{{ $tag['name'] }}</a>&nbsp;
            </div>
        @endforeach
    </div>
    <div class="row badge-danger ">
        <div class="col">来源：{{ $article['source'] }}</div>
        <div class="col">作者：{{ $article['writer'] }}</div>
        <div class="col">{{ date("Y-m-d H-m-s", $article['pubdate']) }}</div>
        <div class="col">访问量：{{ $article['click'] }}</div>
    </div>
    <figure class="figure">
        <figcaption
            class="figure-caption shadow-none p-3 mb-5 bg-light rounded">{{ Str::limit($article['content'], 200, '...') }}</figcaption>
    </figure>
    <article class="row">
        <img src="{{ $article['litpic'] }}" class="figure-img img-fluid rounded float-left" width="200"
             alt="{{ $article['title'] }}" title="{{ $article['title'] }}">
        <div class="col"> {{ $article['content'] }}</div>
    </article>
@endsection
