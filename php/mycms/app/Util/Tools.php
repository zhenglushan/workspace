<?php

namespace App\Util;

class Tools
{
    /**
     * 把数组中的对象转换成数组
     * 也就是对象数组转换成数组的数组
     *
     * @param [type] $obj_arr
     * @return array
     */
    public static function object_array_to_array($obj_arr)
    {
        $_array = is_object($obj_arr) ? get_object_vars($obj_arr) : $obj_arr;
        foreach ($_array as $key => $value) {
            $value = (is_array($value) || is_object($value)) ? Tools::object_array_to_array($value) : $value;
            $array[$key] = $value;
        }
        return $array;
    }

    /**
     * 把对象转换为数组
     */
    public static function object_to_array($obj)
    {
        return json_decode(json_encode($obj), true);
    }

    /**
     * @param int $len
     * @return string
     * 生成不重复的字符串
     */
    public static function no_repeat_string($len = 10)
    {
        $nums = '0123456789';
        $lower = 'abcdefghijklmnopqrstuvwxyz';
        $upper = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ';
        $chars = $nums . $lower . $upper;
        $string = time();
        for (; $len >= 0; $len--) {
            $position = rand() % strlen($chars);
            $position2 = rand() % strlen($string);
            $string = substr_replace($string, substr($chars, $position, 1), $position2, 1);
        }
        return $string;
    }
}
