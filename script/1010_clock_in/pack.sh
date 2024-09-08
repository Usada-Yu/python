#!/bin/bash
# 出错后退出
set -e

artifact_name="clock_in"
source_file="clock_in.py"

rm -rf build ${artifact_name} ${artifact_name}.spec

pyinstaller --clean -F --name=${artifact_name} --noupx --distpath="./"  \
--noconsole                                                             \
${source_file}

rm -rf build ${artifact_name}.spec
