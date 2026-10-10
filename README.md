# 多应用管理后台原型

中文交互演示，使用 GitHub Pages 发布。

## 自动发布

仓库 Settings → Pages → Source 选择 GitHub Actions。更新 `index.html` 或图标资源并推送至 `main`，会自动更新同一个站点地址。

## 本地验证

运行 `python3 scripts/prepare-pages.py`，发布文件输出至 `.pages-site`。

## 演示登录

账号 `admin`，密码 `Admin123!`。仅用于界面演示，没有服务端认证；账号数据保存在当前浏览器中，请勿输入真实敏感信息。

## 图标许可

MingCute 图标使用 Apache-2.0 许可证，来源与许可见 `assets/icons/`。
