#!/bin/bash
source /home/ec2-user/anaconda3/bin/activate schencj_env
# 检查是否提供了要运行的文件名作为参数
if [ $# -ne 1 ]; then
  echo "请提供要运行的文件名作为参数"
  exit 1
fi

# 要运行的文件名
file_to_run="$1"

# 拉取最新的代码到本地
git stash
git pull

# 检查是否拉取成功
if [ $? -ne 0 ]; then
  echo "拉取代码失败，请检查Git配置和网络连接"
  exit 1
fi

# 检查要运行的文件是否存在
if [ ! -f "$file_to_run" ]; then
  echo "文件 '$file_to_run' 不存在"
  exit 1
fi

# 给文件执行权限（如果需要）
chmod +x "$file_to_run"

# 运行指定的文件
python ./"$file_to_run"
