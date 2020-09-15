<?php

namespace App\Http\Controllers\Home;

use App\Http\Controllers\Controller;
use App\Util\Tools;
use Illuminate\Http\Request;
use DB;
use Cache;

class TagController extends Controller
{
    /**
     * @param $tid
     * @param int $pid
     * @return \Illuminate\Contracts\View\Factory|\Illuminate\View\View
     * 不论是 Category 还是 Tag 还是 Search 我们最多只显示最新的 200 条记录，当前测试最多 80 条，每页显示 10 条，所以最多只有 8 页
     * 1、处理起来更加方便
     * 2、可以有效禁止被第三方无限抓取
     * 3、尽管列表页不能提供入口，但是网站地图可以
     * 4、用户也不可能一页一页点下去，可以通过搜索来找需要的内容
     * 5、网站地图可以不放在 robots 文件中，然后通过本地脚本来提交
     */
    public function list($tid, $pid = 1)
    {
        // 查询标签
        $tag = DB::select('select * from tag where id = ?', [$tid])[0];
        $tag = Tools::object_to_array($tag);

        // 查询文章 IDs
        $tag_ids = DB::select('select * from article_tag_category where tag_id = ' . $tid . ' order by article_id desc limit 0,85');
        $tag_ids = Tools::object_to_array($tag_ids);
        $article_id_s = [];
        foreach ($tag_ids as $tag_id) {
            $article_id_s[] = $tag_id['article_id'];
        }

        // 先对文章 ID 进行分页，获取当前页文章的 ID 数组，然后拼凑成字符串
        $psize = 10;
        $start = ($pid - 1) * $psize;
        $new_article_id_s = array_slice($article_id_s, $start, $psize);
        $new_article_id_s = implode(',', $new_article_id_s); // in () 中的字符串

        // 查询文章列表
        $conts = DB::select("select id,cate_id,title,description from article where id in ($new_article_id_s) order by id desc");
        $conts = Tools::object_array_to_array($conts);

        // 创建分页列表
        $total_page = ceil(count($article_id_s) / $psize);
        $links = '';
        $link_front = "<li class=\"page-item\">";
        $link_back = "</li>";
        for ($i = 1; $i <= $total_page; $i++) {
            if ($i == $pid) {
                $link = '<a class="page-link" style="background-color:#dee2e6;" href="' . route('home::tag::list', [$tid, $pid]) . '">' . $pid . '</a>';
            } else {
                $link = '<a class="page-link" href="' . route('home::tag::list', [$tid, $i]) . '">' . $i . '</a>';
            }
            $links = $links . $link_front . $link . $link_back;
        }

        /**
         * 缓存测试代码
         * $key = "tag::list::".md5(route('home::tag::list', [$tid, $pid]));
         * Cache::store('file')->add($key,$links,1000000);
         */

        return view('home.tag.list', compact('conts', 'tag', 'links'));
    }
}
