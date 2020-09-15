@extends('home.common.base')

@section('title'){{ $cate['title'] }}@endsection

@section('keywords'){{ $cate['keywords'] }}@endsection

@section('description'){{ $cate['description'] }}@endsection

@section('breadcrumb')
    <nav aria-label="breadcrumb">
        <ol class="breadcrumb">
            <li class="breadcrumb-item"><a href="/">Home</a></li>
            {!! $breadcrumbs[$cate['id']] !!}
        </ol>
    </nav>
@endsection

@section('content')
    @foreach ($conts as $cont)
        <h3><a href="{{ route('home::cont::list', [$cont['id'],1]) }}">{{ $cont['title'] }}</a></h3>
        <p>{{ $cont['description'] }}</p>
    @endforeach
@endsection
