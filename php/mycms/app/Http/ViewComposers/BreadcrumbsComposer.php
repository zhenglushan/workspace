<?php


namespace App\Http\ViewComposers;

use App\Util\MakeBreadcrumb;
use App\Util\Tools;
use Illuminate\View\View;
use DB;
use Cache;

/**
 * Class BreadcrumbsComposer
 * @package App\Http\ViewComposers
 * 获取所有分类，然后拼接出所有分类的面包屑导航
 * 以当前分类的 ID 做为键，面包屑导航代码做为值
 */
class BreadcrumbsComposer
{
    public function compose(View $view)
    {
        $key = "breadcrumb::all";
        if (Cache::has($key)) {
            $new_breadcrumbs_arr = Cache::get($key);
        } else {
            $cates = DB::select('select id, reid, name, pinyin from category');
            $cates = Tools::object_array_to_array($cates);
            $makeBreadcrumb = new MakeBreadcrumb('id', 'reid', 'name');
            $breadcrumbs_arr = $makeBreadcrumb->breadcrumb($cates);
            $new_breadcrumbs_arr = $makeBreadcrumb->makeBreadcrumb($breadcrumbs_arr);

            foreach ($new_breadcrumbs_arr as $key => $new_breadcrumbs) {
                $result = '';
                foreach ($new_breadcrumbs as $breadcrumb) {
                    $id = $breadcrumb['id'];
                    $name = $breadcrumb['name'];
                    $pinyin = $breadcrumb['pinyin'];
                    $front = '<li class="breadcrumb-item">';
                    $link = '<a href="' . route('home::cate::list', [$id, 1]) . '">' . $name . '</a>';
                    $back = '</li>';
                    $result = $front . $link . $back . $result;
                }
                $new_breadcrumbs_arr[$key] = $result;
            }
            Cache::put($key, $new_breadcrumbs_arr, 1);
        }
        $view->with('breadcrumbs', $new_breadcrumbs_arr);
    }
}
