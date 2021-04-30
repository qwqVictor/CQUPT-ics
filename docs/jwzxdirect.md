教务在线数据源的实现是 CQUPT-ics 的里程碑，标志着 CQUPT-ics 可以摆脱任何外部依赖，直接提供课表和考试信息服务。

由于教务在线仅供内网访问，因此你需要在内网中运行程序，或手动指定请求的 APIROOT 到你自己的教务在线反代。

默认的 APIROOT 是 `jwzx.cqupt.edu.cn`。

为了方便服务器上的容器化部署，我们选择使用环境变量 `JWZX_APIROOT` 来传递自定义的 APIROOT。

我们假定你的教务在线反代为 `https://jwzx.fuck.cqupt.net`。

### 直接运行命令行版本
对于类 Unix 系统，在 POSIX shell 中运行：
```bash
JWZX_APIROOT="https://jwzx.fuck.cqupt.net" python3 cli.py --provider jwzxdirect 2020xxxxxx
```
或  
```bash
/usr/bin/env JWZX_APIROOT="https://jwzx.fuck.cqupt.net" python3 cli.py --provider jwzxdirect 2020xxxxxx
```

对于 Windows 用户，可在 PowerShell 中运行：
```powershell
$env:JWZX_APIROOT = 'https://jwzx.fuck.cqupt.net' python3 cli.py --provider jwzxdirect 2020xxxxxx
```
或者在 cmd 中运行：
```batch
set JWZX_APIROOT=https://jwzx.fuck.cqupt.net
python3 cli.py --provider jwzxdirect 2020xxxxxx
```

命令行直接运行服务器版方式类似。

### Docker 直接运行服务器版
```bash
docker build -t cqupt_ics .
docker run --name cqupt_ics -p 80:2021 -e JWZX_APIROOT="https://jwzx.fuck.cqupt.net" cqupt_ics
```

### Docker-Compose 运行服务器版
取消对 `docker-compose.yml` 中对于 environment 部分的注释并修改。

注意，教务在线官方的公网反代 `jwc.cqupt.edu.cn` 部署了网络安全防火墙，具备反爬虫能力，因此不能将其设置为 APIROOT。  
我们可能会在未来的更新中引入无头浏览器来抓取该公网反代。