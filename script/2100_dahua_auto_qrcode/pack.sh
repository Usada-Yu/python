#!/bin/bash
# 出错后退出
set -e

artifact_name="auto_qrcode"
source_file="auto_qrcode.py"
pyzbar_dir="D:\\0700_code\\0110_python3\\Lib\\site-packages\\pyzbar"

rm -rf build ${artifact_name} ${artifact_name}.spec

# 通过 pyinstaller 命令开始打包，需要手动添加字体文件和依赖的动态库
# 此处使用 `--noupx` 禁用 upx 压缩，因为压缩后会让文件的启动速度大大降低
pyinstaller --clean --name=${artifact_name} --noupx --distpath="./" \
--add-binary="${pyzbar_dir}\\libiconv.dll;." \
--add-binary="${pyzbar_dir}\\libzbar-64.dll;." \
--add-data="./typeface/arial.ttf;./typeface/" \
--add-data="./config/auto_qr_user.ini;./config/" \
--noconsole \
${source_file}

rm -rf build ${artifact_name}.spec
