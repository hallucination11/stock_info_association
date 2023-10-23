#!/bin/bash

# 提交消息
commit_message="自动提交 $(date +'%Y-%m-%d %H:%M:%S')"

# 添加所有更改并提交到当前分支
git add .
git commit -m "$commit_message"

# 推送到当前分支
git push origin HEAD

# 输出提交成功消息
echo "自动提交并推送成功: $commit_message"
