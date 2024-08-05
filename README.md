# magic-html-browser-plugin

使用magic-html部署后端python应用程序，同时提供chrome插件，右键支持任意html导出markdown下载
## chrome插件
1. 浏览器开发者模式，直接加载
2. 配置后端服务地址`https://ip:port/convert`

## 后端服务

### https://github.com/opendatalab/magic-html 根据magic-html使用，完成main.py，启动流程如下

1. 生成证书：`openssl req -x509 -newkey rsa:4096 -keyout key.pem -out cert.pem -days 3650`
2. 解密`openssl rsa -in key.pem -out decrypted_key.pem`
3. 浏览器导入证书
4. 启动服务：`nohup python3 main.py 2>&1 > app.log &`

## 使用

右键点击页面即可