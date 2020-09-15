# Jupyter 相关命令

## 帮助命令

```shell
C:\Users\Administrator\Desktop
λ jupyter notebook --help
```

信息如下：

```shell
The Jupyter HTML Notebook.

这将启动一个基于tornado的HTML笔记本服务器，它提供一个html5/javascript笔记本客户端。

Subcommands
-----------

Subcommands are launched as `jupyter-notebook cmd [args]`. For information on
using subcommand 'cmd', do: `jupyter-notebook cmd -h`.

list
    列出当前运行的Notebook服务.
stop
    Stop currently running notebook server for a given port
password
    Set a password for the notebook server.

Options
-------

Arguments that take values are actually convenience aliases to full
Configurables, whose aliases are listed on the help line. For more information
on full configurables, see '--help-all'.

--debug
    set log level to logging.DEBUG (maximize logging output)
--generate-config
    generate default config file
-y
    Answer yes to any questions instead of prompting.
--no-browser
    在启动服务以后不在浏览器中打开一个窗口.
--pylab
    DISABLED: use %pylab or %matplotlib in the notebook to enable matplotlib.
--no-mathjax
    Disable MathJax

    MathJax is the javascript library Jupyter uses to render math/LaTeX. It is
    very large, so you may want to disable it if you have a slow internet
    connection, or for offline use of the notebook.

    When disabled, equations etc. will appear as their untransformed TeX source.
--allow-root
    允许notebook在root用户下运行.
--script
    DEPRECATED, IGNORED
--no-script
    DEPRECATED, IGNORED
--log-level=<Enum> (Application.log_level)
    Default: 30
    Choices: (0, 10, 20, 30, 40, 50, 'DEBUG', 'INFO', 'WARN', 'ERROR', 'CRITICAL')
    Set the log level by value or name.
--config=<Unicode> (JupyterApp.config_file)
    Default: ''
    Full path of a config file.
--ip=<Unicode> (NotebookApp.ip)
    Default: 'localhost'
    notebook服务会监听的IP地址.
--port=<Int> (NotebookApp.port)
    Default: 8888
    notebook服务会监听的IP端口.
--port-retries=<Int> (NotebookApp.port_retries)
    Default: 50
    如果指定的端口不可用，则要尝试其他端口的数量.
--transport=<CaselessStrEnum> (KernelManager.transport)
    Default: 'tcp'
    Choices: ['tcp', 'ipc']
--keyfile=<Unicode> (NotebookApp.keyfile)
    Default: ''
    SSL/TLS 私钥文件所在全路径.
--certfile=<Unicode> (NotebookApp.certfile)
    Default: ''
    SSL/TLS 认证文件所在全路径.
--client-ca=<Unicode> (NotebookApp.client_ca)
    Default: ''
    用于ssl/tls客户端身份验证的证书颁发证书的完整路径.
--notebook-dir=<Unicode> (NotebookApp.notebook_dir)
    Default: ''
    用于笔记本和内核的目录。
--browser=<Unicode> (NotebookApp.browser)
    Default: ''
    Specify what command to use to invoke a web browser when opening the
    notebook. If not specified, the default browser will be determined by the
    `webbrowser` standard library module, which allows setting of the BROWSER
    environment variable to override it.
--pylab=<Unicode> (NotebookApp.pylab)
    Default: 'disabled'
    DISABLED: use %pylab or %matplotlib in the notebook to enable matplotlib.
--gateway-url=<Unicode> (GatewayClient.url)
    Default: None
    The url of the Kernel or Enterprise Gateway server where kernel
    specifications are defined and kernel management takes place. If defined,
    this Notebook server acts as a proxy for all kernel management and kernel
    specification retrieval.  (JUPYTER_GATEWAY_URL env var)

To see all available configurables, use `--help-all`

Examples
--------

    jupyter notebook                       # start the notebook
    jupyter notebook --certfile=mycert.pem # use SSL/TLS certificate
    jupyter notebook password              # enter a password to protect the server


C:\Users\Administrator\Desktop
λ
```

## 启动 Jupyter

### 默认端口启动

```shell
C:\Users\Administrator\Desktop
λ jupyter notebook
```

### 指定端口启动

```shell
C:\Users\Administrator\Desktop
λ jupyter notebook --port 7788
```

### 启动不开浏览器

只启动 Jupyter 服务，但是不打开浏览器。

```shell
C:\Users\Administrator\Desktop
λ jupyter notebook --no-browser
```

**总结**：Jupyter 可以通过不同端口进行启动和访问，因此可以同时启动多个 Jupyter Notebook 服务。

