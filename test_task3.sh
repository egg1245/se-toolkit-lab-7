#!/bin/bash
# Test Task-3: Natural language intent routing

set -e

VM_USER=root
VM_HOST=10.93.25.76
PROJECT_DIR=~/se-toolkit-lab-7

echo "=== Testing Task-3: LLM Intent Routing ==="
echo ""

echo "1. Check if Qwen proxy is running..."
ssh $VM_USER@$VM_HOST "curl -s http://localhost:42005/v1/models -H 'Authorization: Bearer default-key' | head -c 100" || echo "WARNING: Qwen proxy not reachable"
echo ""

echo "2. Check if backend is running..."
ssh $VM_USER@$VM_HOST "curl -s http://localhost:42002/items/ -H 'Authorization: Bearer my-secret-api-key' | grep -o 'id' | head -1" || echo "WARNING: Backend not reachable"
echo ""

echo "3. Test natural language query on VM..."
ssh $VM_USER@$VM_HOST "cd $PROJECT_DIR && uv run python -m bot.bot --test \"what labs are available?\" 2>&1" | tee /tmp/task3_result.log
echo ""

echo "4. Check stderr for tool calls..."
tail -20 /tmp/task3_result.log | grep -E "\[tool\]|\[summary\]|Lab" || echo "No tool calls or data found"

echo ""
echo "Test completed. Check output above for results."
