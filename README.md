一、它能做什么？
递归扫描任意文件夹（常见 小程序/APP 反编译输出）
按用户自定义字典（默认 key 文件）秒级命中敏感字段
自动提取 “关键词 + 其后 50 字符”（足够覆盖多数密钥/赋值）
图形界面 “选文件夹→选字典→点开始”，零门槛
结果支持 表格浏览 / 一键导出 CSV，方便审计&报告
二、核心特点
表格
复制
特性	说明
🔍 精准匹配	正则忽略大小写，支持 # 注释、空行
🧵 异步扫描	后台线程，界面不卡
📦 零依赖	纯 Python 标准库，无需 pip
🎨 跨平台	Windows / Linux / macOS 均可运行
🔧 可打包	提供一键 PyInstaller 命令，可自行生成 exe
三、快速上手
① 运行源码（推荐）
bash
复制
git clone https://github.com/YOUR_NAME/Select.git
cd Select
python select.py
② 打包成 exe（可选）
bash
复制
python -m pip install pyinstaller
pyinstaller -F -w select.py -n MiniSec-Hunter
输出在 dist/MiniSec-Hunter.exe
四、使用步骤
克隆或下载源码，确保 select.py 与字典 key 在同一目录
双击或命令行运行 python select.py
选文件夹 → 选字典 → 开始扫描 → 导出结果
五、字典格式
文本文件 key，一行一词，支持 # 注释：
复制
# 云密钥
accessKeyId
accessKeySecret

# 支付
mchId
apiKey
已内置 key 含 200+ 高频关键词，可直接用；改行增删即时生效
六、运行效果
复制
accessKeyId  ->  ./config.js:5  ->  accessKeyId:"AKIDabcdef0123456789...
appsecret    ->  ./const.js:12  ->  appsecret : 'wx1234567890abcdef // ...
共 37 条结果，详情见 kv_report_20251117_163000.md
七、目录结构
复制
Select/
├─ select.py          # 主源码（图形界面）
├─ key                # 默认字典
├─ requirements.txt   # 空依赖（运行无需 pip）
├─ README.md          # 本文件
├─ LICENSE            # MIT
不提供预编译 exe，需要请自行动手打包。
八、常见问答
Q1: 双击没反应？
A: 用命令行运行 python select.py 可看实时日志与报错。
Q2: 想改 50 字符长度？
A: 源码 line[start:start+50] 改 50 即可，重新打包。
Q3: 360 / 火绒报毒？
A: 自行打包的 exe 如被误报，加白名单或用源码运行。
九、贡献 & 反馈
欢迎提 Issue 或 PR，一起完善字典、增加规则！
十、License
本项目基于 MIT 协议开源，可自由修改、商业使用，但请保留原作者信息。
