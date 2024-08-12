#!/bin/bash

# ######################################## #
# 仓库初始化脚本，运行前确保此脚本有可执行权限 #
# ######################################## #

set -e

script_path=$(readlink -f "$0")
script_dir=$(dirname "$script_path")
project_dir=${script_dir}

# 无法访问pypi.org时使用的代理地址
mirror_url="mirrors.aliyun.com"

# 错误处理 #
error_deal() {
    echo -e "\033[0;31mAn error occurred when the script was triggered manually, the script will exit...\033[0m"
    cd ${project_dir}
    # 删除可能存在和python相关的临时目录
    find ./ -type d \( -name "dist" -o -name "*.egg-info" \) -exec rm -rfv {} +
    exit 1
}
trap "error_deal" ERR
trap "error_deal" SIGINT
# 错误处理 #

echo -e "\033[0;32m====================================================================\033[0m"
# python自定义模块安装 #
# 模块默认安装在python路径的site-packages下；
# 无安装权限可在pip后添加--user选项或以sudo方式执行脚本
cd ${project_dir}/common/self-fileModule
if [[ $(uname -s) == "Linux" ]]; then
    if command -v python3 &>/dev/null; then
        python3 ./setup.py sdist
        # 是否使用镜像代理，默认不使用
        if true; then
            pip3 install --upgrade ./dist/*.tar.gz
        else
            pip3 install --default-timeout=6666 --upgrade \
                -i http://${mirror_url}/pypi/simple/ --trusted-host ${mirror_url} ./dist/*.tar.gz
        fi
    elif command -v python &>/dev/null; then
        python ./setup.py sdist
        pip install --upgrade ./dist/fileModule*.tar.gz
    else
        echo -e "\033[0;31mThere is no python in the environment\033[0m"
    fi
else
    if [[ "" != $(python3 --version) ]]; then
        python3 ./setup.py sdist
        pip3 install --upgrade ./dist/fileModule*.tar.gz
    elif [[ "" != "$(python --version)" ]]; then
        python ./setup.py sdist
        pip install --upgrade ./dist/fileModule*.tar.gz
    else
        echo -e "\033[0;31mThere is no python in the environment\033[0m"
    fi
fi
find ./ -type d \( -name "dist" -o -name "*.egg-info" \) -exec rm -rfv {} +
cd -
