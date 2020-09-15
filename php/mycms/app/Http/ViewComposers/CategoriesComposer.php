<?php

namespace App\Http\ViewComposers;

use App\Util\Tools;
use Illuminate\View\View;
use DB;
use Cache;

/**
 * Class CategoriesComposer
 * @package App\Http\ViewComposers
 * 获取所有分类
 */
class CategoriesComposer
{
    public function compose(View $view)
    {
        $key = "cate::all";
        if (Cache::has($key)) {
            $cates = Cache::get($key);
        } else {
            $cates = DB::select('select * from category');
            $cates = Tools::object_array_to_array($cates);
            Cache::put($key, $cates, 10);
        }
        $view->with('cates', $cates);

        /**
         * 在使用Cache::set或Cache::get时使用的是默认的缓存类型，如果想使用非默认的缓存类型，需要修改调用。
         * 比如使用 Memcached 为缓存类型，那么使用 Cache::store('memcached')->set()设置缓存，使用Cache::store('memcached')->get()获取缓存。
         * 参考页面: https://baijiahao.baidu.com/s?id=1627724408703314672
         * 测试代码位置: app/Http/Controllers/Home/TagController.php
         *
         */
    }
}
