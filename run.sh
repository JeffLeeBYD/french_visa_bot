#! /bin/bash
cd /root/code/visa_bot
rm -rf log.txt
touch log.txt
nohup xvfb-run /root/web_scp/bin/python3 dummy.py > test.log 2>&1 &