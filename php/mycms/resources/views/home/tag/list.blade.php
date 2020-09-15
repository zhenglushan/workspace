@extends('home.common.base')

@section('title'){{ $tag['name'] }} - {{ $tag['pinyin'] }} - {{ $tag['title'] }}@endsection

@section('keywords'){{ $tag['keywords'] }}@endsection

@section('description'){{ $tag['description'] }}@endsection

@section('breadcrumb')
    <nav aria-label="breadcrumb">
        <ol class="breadcrumb">
            <li class="breadcrumb-item"><a href="/">Home</a></li>
            <li class="breadcrumb-item"><a href="{{ route('home::tag::list',[$tag['id'],1]) }}">{{ $tag['name'] }}</a>
            </li>
        </ol>
    </nav>
@endsection

@section('content')
    @foreach ($conts as $cont)
        <h3><a href="{{ route('home::cont::list', [$cont['id'],1]) }}">{{ $cont['title'] }}</a></h3>
        <p>{{ $cont['description'] }}</p>
    @endforeach
    <nav aria-label="Page navigation example">
        <ul class="pagination">
            {!! $links !!}
        </ul>
    </nav>
@endsection
