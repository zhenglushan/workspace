<?php


namespace App\Http\Controllers\Admin;

use App\Http\Controllers\Controller;
use DB;
use App\Util\Tools;
use Request;
use Gregwar\Captcha\CaptchaBuilder;
use Gregwar\Captcha\PhraseBuilder;
use Session;

class LoginController extends Controller
{
    /**
     * 登录
     */
    /** @noinspection SqlResolve */
    public function login(Request $request)
    {
        if (Request::isMethod('get')) {
            return view('admin.login.login');
        } elseif (Request::isMethod('post')) {
            $email = $request::input('email');
            $pwd = $request::input('pwd');
            $pwd = md5($pwd);
            $verify_input = $request::input('verify');
            $verify_session = Session::get('verify_captcha');
            if ($verify_input == $verify_session) {
                // echo '您输入的验证码正确';
                $is_exist = DB::select("SELECT * FROM user WHERE email=? AND pwd=?", [$email, $pwd]);
                if ($is_exist) {
                    // echo "用户存在";
                    $user = Tools::object_to_array($is_exist[0]);
                    Session::put('user', $user);
                    return redirect(route('admin::index'));
                } else {
                    // echo "用户不存在";
                    return redirect(route('admin::loging'));
                }
            } else {
                // echo '您输入的验证码错误';
                return redirect(route('admin::loging'));
            }
        }
    }

    /**
     * 用户退出登录
     */
    public function logout()
    {
        if (Session::has('user')) {
            Session::pull('user', null);
        }
        return redirect(route('admin::loging'));
    }

    /**
     * 登陆成功后显示的页面
     */
    public function index()
    {
        return view("admin.login.index");
    }

    /**
     * 生成登陆的验证码
     */
    public function verify()
    {
        $phraseBuilder = new PhraseBuilder(5, '0123456789');
        $captcha = new CaptchaBuilder(null, $phraseBuilder);
        // 可以设置图片宽高及字体
        $captcha->build($widht = 200, $height = 80);
        //获取验证码的内容
        $phrase = $captcha->getPhrase();
        //把内容存入session
        Session::flash('verify_captcha', $phrase);
        //生成图片
        header("Cache-Control: no-cache, must-revalidate");
        header('Content-Type: image/jpeg');
        $captcha->output();
    }
}
