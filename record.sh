#!/bin/bash
# Playwright Codegen 录制脚本（pytest 格式）
# 使用方法: ./record.sh [网址] [输出文件]

URL=${1:-"http://localhost:18001/"}
OUTPUT=${2:-"tests/test_readbook_3.py"}

echo "开始录制 Playwright 测试代码（pytest 格式）..."
echo "目标网址: $URL"
echo "输出文件: $OUTPUT"
echo ""
echo "提示："
echo "1. 在打开的浏览器中进行操作"
echo "2. 右侧会实时显示生成的 pytest 格式代码"
echo "3. 按 Ctrl+C 停止录制"
echo "4. 代码会自动保存到 $OUTPUT"
echo "5. 生成的是 pytest 格式，可以直接运行: pytest $OUTPUT"
echo ""
echo "按回车键开始录制..."
read

playwright codegen \
  --target python-pytest \
  --browser chromium \
  --output "$OUTPUT" \
  "$URL"

# 录制完成后，自动将 test_example 替换为基于文件名的测试函数名
if [ -f "$OUTPUT" ]; then
    # 从文件路径中提取文件名（不含扩展名）
    # 例如: tests/test_readbook.py -> test_readbook
    filename=$(basename "$OUTPUT" .py)
    
    # 将 test_example 替换为文件名对应的函数名
    # 使用 sed 在 macOS 和 Linux 上都能工作
    if [[ "$OSTYPE" == "darwin"* ]]; then
        # macOS 使用 BSD sed
        sed -i '' "s/def test_example(/def ${filename}(/g" "$OUTPUT"
    else
        # Linux 使用 GNU sed
        sed -i "s/def test_example(/def ${filename}(/g" "$OUTPUT"
    fi
    
    echo ""
    echo "✓ 已自动将测试函数名从 'test_example' 改为 '${filename}'"
fi

echo ""
echo "录制完成！pytest 格式代码已保存到: $OUTPUT"
echo "运行测试: pytest $OUTPUT"

