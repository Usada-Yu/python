#!/bin/bash

set -e

artifact_name="pss"
source_file="pss.py"

rm -rf build ${artifact_name} ${artifact_name}.spec

pyinstaller --clean -F --name=${artifact_name} --noupx --distpath="./"  \
--icon ./favicon.ico                                                    \
--noconsole                                                             \
${source_file}

rm -rf build ${artifact_name}.spec
