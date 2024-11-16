#!/bin/bash
npx hardhat node --port 1234 --config hardhat.config.js > /app/logs/hardhat.log 2>&1 &
hardhat_pid=$!
sleep 5
python3 submit_payloads.py > /app/logs/submit_payloads.log 2>&1
pkill -P $hardhat_pid
exit 0