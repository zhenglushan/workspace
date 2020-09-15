<?php


namespace App\Http\Controllers\Home;

use App\Http\Controllers\Controller;
use DB;
use App\Util\Tools;

class ArticleController extends Controller
{
    // 显示 article 详情页
    /** @noinspection SqlResolve */
    public function detail($aid, $pid = 1)
    {
        $article = DB::select('select * from article where id = ?', [$aid])[0];
        $article = Tools::object_to_array($article);

        $category = DB::select('select * from category where id = ?', [$article['cate_id']])[0];
        $category = Tools::object_to_array($category);

        $tag_ids = DB::select('select tag_id from article_tag_category where article_id = ?', [$aid]);
        $tag_ids = Tools::object_to_array($tag_ids);
        $tag_ids_str = implode(',', array_column($tag_ids, 'tag_id'));
        $tags = DB::select("select id,name,pinyin from tag where id in ($tag_ids_str)");
        $tags = Tools::object_to_array($tags);

        return view('home.article.detail', compact('article', 'category', 'tags'));
    }
}
