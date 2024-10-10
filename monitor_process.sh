#!/bin/bash

# 列出所有正在運行的 python3 進程和 PID
echo "正在運行的 Python 3 進程："
ps aux | grep '[p]ython3' | awk '{print $2, $11, $12}'

# 提示用戶輸入要監控的 PID
read -p "請輸入你要監控的 Python 3 進程的 PID: " pid

# 檢查進程是否存在
if ! ps -p "$pid" > /dev/null; then
    echo "PID $pid 的進程不存在."
    exit 1
fi

# 提示用戶監控進程並將結果記錄到文件中
echo "開始監控進程 $pid，結果將記錄到 runtime.log."

# 背景運行進程監控並使用 nohup 確保即使斷開 SSH 也能繼續運行
nohup bash -c "
while ps -p $pid > /dev/null
do
    ps -p $pid -o etime >> runtime.log
    sleep 60  # 每分鐘檢查一次
done
echo \"Process $pid finished at \$(date)\" >> runtime.log
" &

echo "監控程序已在背景運行。你可以斷開 SSH 連接。"

# 使用方法：
# chmod +x monitor_process.sh
# ./monitor_process.sh
