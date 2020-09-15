<?php

namespace App\Http\Controllers\Home;

use App\Http\Controllers\Controller;
use App\Util\Tools;
use Illuminate\Http\Request;
use DB;
use Cache;


class CategoryController extends Controller
{
    public function list($cid, $pid = 1)
    {
        // 查询分类
        $cate = DB::select('select * from category where id = ?', [$cid])[0];
        $cate = Tools::object_to_array($cate);
        // 查询文章列表
        $psize = 10; // 每页显示 10 条数据
        $start = ($pid - 1) * $psize;
        $conts = DB::select("select id,title,description from article where cate_id = {$cid} order by id limit {$start},10");
        $conts = Tools::object_array_to_array($conts);
        return view('home.category.list', compact('conts', 'cate'));
    }
}
