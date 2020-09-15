<?php

use Illuminate\Support\Facades\Route;

/*
|--------------------------------------------------------------------------
| Web Routes
|--------------------------------------------------------------------------
|
| Here is where you can register web routes for your application. These
| routes are loaded by the RouteServiceProvider within a group which
| contains the "web" middleware group. Now create something great!
|
*/

Route::get('/', function () {
    return view('welcome');
});

/** 后台路由管理 */
Route::group(['prefix' => 'manager', 'as' => 'manager::'], function () {
    /* 登陆页面 */
    Route::view('loginui', 'houtai.loginui')->name("loginui");
    Route::post('login', 'UserController@login')->name("login");
    Route::get('index', 'UserController@index')->name("index");
    /* 用户管理 */

    /* 分类管理 */

    /* 文章管理 */
    /* 标签管理 */
    Route::group(['prefix' => 'tag', 'as' => 'tag::'], function () {
        Route::view('addui', 'houtai.tag.addui')->name("addui");
    });
});





/**
 * 前台路由管理
 */


