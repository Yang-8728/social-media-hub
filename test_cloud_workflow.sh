#!/bin/bash
# 云原生工作流示例 (Bash - 适用于 Linux 服务器/CCE Pod)

API_BASE="http://localhost:8080"

echo "=== 1. 查询当前编号 ==="
curl -s "$API_BASE/api/biliup/counter" | jq

echo -e "\n=== 2. 设置起始编号为 124 ==="
curl -s -X POST "$API_BASE/api/biliup/counter" \
  -H "Content-Type: application/json" \
  -d '{"value": 124}' | jq

echo -e "\n=== 3. 上传测试视频 ==="
for i in {1..3}; do
  echo "上传测试视频 #$i"
  curl -s -X POST "$API_BASE/api/biliup/upload" \
    -H "Content-Type: application/json" \
    -d "{\"video_path\": \"/videos/ai_vanvan/test$i.mp4\", \"auto_number\": true}" | jq
done

echo -e "\n=== 4. 上传后查询编号（应该是127） ==="
curl -s "$API_BASE/api/biliup/counter" | jq

echo -e "\n=== 5. 测试完成，回退计数器到 124 ==="
curl -s -X POST "$API_BASE/api/biliup/counter" \
  -H "Content-Type: application/json" \
  -d '{"value": 124}' | jq

echo -e "\n=== 6. 验证计数器已回退 ==="
curl -s "$API_BASE/api/biliup/counter" | jq

echo -e "\n✅ 完成！所有操作通过 HTTP API，无需 Python 脚本"
