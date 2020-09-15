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

/** 添加测试数据 */
Route::prefix('test')->name('test::date::')->group(function () {
    Route::get('/category/', 'TestController@addCategory')->name('add::category');
    Route::get('/article/', 'TestController@addArticle')->name('add::article');
    Route::get('/tag/', 'TestController@addTag')->name('add::tag');
    Route::get('/actmiddle/', 'TestController@addArticleCategoryTag')->name('add::actmiddle');
    Route::get('/user/', 'TestController@addUser')->name('add::user');
    Route::get('/redis/', 'TestController@testRedis')->name('redis');
    Route::get('/breadcrumb/', 'TestController@testBreadcrumb')->name('redis');
    Route::get('/norepeatstr/', 'TestController@testNoRepeatStr')->name('norepeatstr');
});

/** 前台访问路由 */
Route::namespace('Home')->name('home::')->group(function () {
    /* 网站地图 和 robots.xt 文件 */

    /* 栏目操作 */
    Route::get('colcate-{cid}-{pid}', 'CategoryController@list')->name('cate::list'); // 栏目列表页

    /* 文章操作 */
    Route::get('colcont-{aid}-{pid}', 'ArticleController@detail')->name('cont::list'); // 文章详情页

    /* 标签操作 */
    Route::get('tag-{tid}-{pid}', 'TagController@list')->name('tag::list'); // 标签列表页
});

/** 后台访问路由 */
Route::prefix(config('app.admin_dir'))->namespace('Admin')->name('admin::')->group(function () {
    //登陆功能
    Route::get('login', 'LoginController@login')->name('loging');
    Route::post('login', 'LoginController@login')->name('loginp');
    Route::get('verify', 'LoginController@verify')->name('verify');
    Route::get('index', 'LoginController@index')->name('index');
    Route::get('logout', 'LoginController@logout')->name('logout');
});
