一、它能做什么？
递归扫描任意文件夹（常见 小程序/APP 反编译输出）
按用户自定义字典（默认 key 文件）秒级命中敏感字段
自动提取 “关键词 + 其后 50 字符”（足够覆盖多数密钥/赋值）
图形界面 “选文件夹→选字典→点开始”，零门槛
结果支持 表格浏览 / 一键导出 CSV，方便审计&报告
# Select - 小程序反编译敏感词扫描器

二、 使用说明

1. 克隆或下载本仓库
2. 确保 `select.py` 与字典文件 `key` 在同一目录
3. 命令行运行 `python select.py`（需 Python 3.7 及以上）
4. 选择文件夹 → 选择字典 → 开始扫描 → 导出 CSV

## 打包成 exe（可选）

```bash
pip install pyinstaller
pyinstaller -F -w select.py -n MiniSec-Hunter
