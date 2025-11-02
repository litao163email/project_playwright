#!/bin/bash
# 运行测试并生成 Allure 报告
# 使用方法: ./run_with_allure.sh [测试文件或路径]

TEST_PATH=${1:-"tests/"}

echo "=========================================="
echo "运行测试并生成 Allure 报告"
echo "=========================================="
echo ""

# 检查 allure 是否安装
if ! command -v allure &> /dev/null; then
    echo "❌ Allure 未安装，请先安装 Allure"
    echo "安装方法："
    echo "  macOS: brew install allure"
    echo "  Linux: 参考 https://docs.qameta.io/allure/"
    exit 1
fi

echo "✓ Allure 已安装: $(allure --version)"
echo ""

# 检查 allure-pytest 是否安装
if ! python3 -m pip show allure-pytest &> /dev/null; then
    echo "安装 allure-pytest..."
    python3 -m pip install allure-pytest
fi

echo "✓ allure-pytest 已安装"
echo ""

# 创建报告目录
mkdir -p test_report

# 运行测试
echo "运行测试: $TEST_PATH"
echo "------------------------------------------"
pytest "$TEST_PATH" -v --alluredir=test_report

TEST_EXIT_CODE=$?

echo ""
echo "------------------------------------------"

if [ $TEST_EXIT_CODE -eq 0 ]; then
    echo "✓ 测试执行完成"
else
    echo "⚠ 测试执行完成（有失败的用例）"
fi

# 生成 Allure HTML 报告
echo ""
echo "生成 Allure HTML 报告..."
allure generate test_report -o test_report/html --clean

if [ $? -eq 0 ]; then
    echo ""
    echo "=========================================="
    echo "✓ Allure 报告已生成"
    echo "=========================================="
    echo ""
    echo "报告位置: test_report/html/index.html"
    echo ""
    echo "查看报告:"
    echo "  macOS:   open test_report/html/index.html"
    echo "  Windows: start test_report/html/index.html"
    echo "  Linux:   xdg-open test_report/html/index.html"
    echo ""
    echo "或使用 Allure 服务查看（自动刷新）:"
    echo "  allure serve test_report"
    echo ""
else
    echo "❌ 报告生成失败"
    exit 1
fi

