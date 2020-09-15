### github push 时出现 fatal: HttpRequestException encountered. 错误

在执行 `git push -u github_workspace master` 提交操作时，提示如下错误信息：

```shell
fatal: HttpRequestException encountered.
   发送请求时出错。
Username for 'https://github.com':
Password for 'https://276517382@qq.com@github.com':
```

奇怪的是，`GitHub` 有这个问题，但是 `Gitee` 却没有。所以，我们查看下提交方式：

```shell
# 查看提交方式
git remote -v
```

结果如下所示：

```shell
gitee_workspace git@gitee.com:zhenglushan/workspace.git (fetch)
gitee_workspace git@gitee.com:zhenglushan/workspace.git (push)
github_workspace        https://github.com/zhenglushan/workspace.git (fetch)
github_workspace        https://github.com/zhenglushan/workspace.git (push)
```

我们发现 `Gitee` 采用 `SSH` 方式提交，而 `GitHub` 采用的是 `HTTPS` 方式提交，所以我们需要修改下 `GitHub` 的提交方式：

```shell
# 修改为 SSH 方式提交:
git remote set-url github_workspace git@github.com:zhenglushan/workspace.git
```

然后再次查询下提交方式：

```shell
# 查看提交方式
git remote -v
```

结果显示如下：
```shell
gitee_workspace git@gitee.com:zhenglushan/workspace.git (fetch)
gitee_workspace git@gitee.com:zhenglushan/workspace.git (push)
github_workspace        git@github.com:zhenglushan/workspace.git (fetch)
github_workspace        git@github.com:zhenglushan/workspace.git (push)
```
说明我们已经成功把 `GitHub` 的提交方式修改为 `SSH` 方式了。重新执行 `GitHub` 提交命令：

```shell
git push -u github_workspace master
```
成功提交，没有弹出输入账号和密码的对话框了。