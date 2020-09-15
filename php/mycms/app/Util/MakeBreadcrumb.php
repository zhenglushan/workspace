<?php


namespace App\Util;

/**
 * Class MakeBreadcrumb
 * @package App\Util
 * 获取分类的所有面包屑导航
 * 该类不需要常驻内存，所以使用的时候，直接 new 创建
 */
class MakeBreadcrumb
{
    private $id = 'id'; // 当前分类的 ID 字段
    private $reid = 'reid'; // 当前分类的父 ID 字段
    private $name = 'name'; // 当前分类的名称字段

    public function __construct($id, $reid, $name)
    {
        $this->id = $id;
        $this->reid = $reid;
        $this->name = $name;
    }

    /**
     * @param $cates
     * @return array
     * 返回所有分类各自对应的祖先分类数组的数组
     */
    public function breadcrumb($cates)
    {
        // $cate_arr = static::getChildren($cates);
        // static::printCategoriesTree($cate_arr); // 调用打印树形结构代码
        // 循环获取每个分类对应的所有祖先分类
        $breadcrumbs_arr = array();
        foreach ($cates as $cate) {
            $breadcrumbs_arr[] = $this->getBreadcrumbLink($cates, $cate[$this->id]);
        }
        return $breadcrumbs_arr;
    }

    /**
     * @param $cate_arr
     * @param int $id
     * @return array
     * 根据分类 ID 获得该 ID 的所有祖先分类
     */
    public function getBreadcrumbLink($cates, $id)
    {
        $breadcrumb = array();
        foreach ($cates as $key => $value) {
            if ($value[$this->id] == $id) {
                $value['parent'] = $this->getBreadcrumbLink($cates, $value[$this->reid]);
                unset($value['children']);
                unset($value['level']);
                $breadcrumb[] = $value;
                unset($cates[$key]); // 已经排好等级的,从数组中移除，提高性能
            }
        }
        return $breadcrumb;
    }

    /**
     * @param $cates
     * @param int $reid
     * @param int $level
     * @return array
     * 返回分类的树形结构的所有层级关系
     */
    public function getChildren($cates, $reid = 0, $level = 0)
    {
        $arr = array();
        foreach ($cates as $key => $value) {
            if ($value[$this->reid] == $reid) {
                $value['level'] = $level;
                $value['children'] = $this->getChildren($cates, $value[$this->id], $level + 1);
                $arr[] = $value;
                unset($cates[$key]); // 已经排好等级的,从数组中移除，提高性能
            }
        }
        return $arr;
    }

    /**
     * @param $breadcrumbs
     * @return array
     * 拼凑成面包屑导航
     */
    public function makeBreadcrumb($breadcrumbs_arr)
    {
        $new_breadcrumbs_arr = [];
        foreach ($breadcrumbs_arr as $breadcrumbs) {
            $key_id = $breadcrumbs[0][$this->id]; // 保存当前分类的 ID 做为键
            $result = array();
            do {
                $current = $breadcrumbs[0];

                $temp = array();
                $temp['id'] = $current['id'];
                $temp['reid'] = $current['reid'];
                $temp['name'] = $current['name'];
                $temp['pinyin'] = $current['pinyin'];

                $result[] = $temp;
                if ($current['parent']) {
                    $breadcrumbs = $current['parent'];
                }
            } while ($current['parent']);
            /** 以当前分类的 ID 为键，以当前分类的面包屑导航为值，组成的数组 */
            $new_breadcrumbs_arr["$key_id"] = $result;
        }
        return $new_breadcrumbs_arr;
    }

    /**
     * @param $cate_arr
     * 打印分类的树形结构
     */
    public function printCategoriesTree($cate_arr)
    {
        foreach ($cate_arr as $key => $value) {
            $fortime = $value['level'] * 5;
            for ($i = 0; $i < $fortime; $i++) {
                echo '-';
            }
            echo ' ' . $value[$this->id] . '<br />';
        }
    }
}
