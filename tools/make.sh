#!/bin/bash
# -*- coding: utf-8 -*-
orig_pv=$1

# ms 毎のフレームにする
ms=${2:-100}

# フレーム毎に分解
mkdir -p out
rm -f out/*
ffmpeg -i ${orig_pv} -vf fps=1000/${ms},scale=-1:30 out/%d.png 2> /dev/null

# エンコード
for f in out/*.png; do
    base64 -i $f -o ${f/.*}.b64
done

# フレーム数を取得
frames=$(ls -1 out/*.b64 | wc -l)

# テンプレートからスクリプトを作成
cwd=$(pwd)
out=${orig_pv/.*}.${ms}ms.sh
cat script.in | sed -e "s/____/${frames}/" -e "s,__CWD__,${cwd}," > ${out}
chmod +x ${out}
