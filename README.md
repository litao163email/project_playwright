# Playwright + Pytest 测试项目

这是一个使用 Playwright 和 pytest 编写的自动化测试项目，包含多个真实网站的测试用例。

## 项目结构

```
test_playwright/
├── tests/                    # 测试用例目录
│   ├── __init__.py
│   ├── test_baidu.py        # 百度搜索测试
│   ├── test_github.py       # GitHub 网站测试
│   └── test_google.py        # Google 搜索测试（可选）
├── conftest.py              # pytest fixtures 和配置
├── pytest.ini               # pytest 配置文件
├── requirements.txt         # Python 依赖
└── README.md               # 项目说明

```

## 安装步骤

### 1. 安装 Python 依赖

```bash
pip install -r requirements.txt
```

### 2. 安装 Playwright 浏览器

```bash
playwright install chromium
```

或者安装所有浏览器：

```bash
playwright install
```

## 运行测试

### 运行所有测试

```bash
pytest
```

### 运行特定测试文件

```bash
pytest tests/test_baidu.py
```

### 运行特定测试用例

```bash
pytest tests/test_baidu.py::test_baidu_search
```

### 在 Cursor/VS Code 中直接运行测试

**方法 1：使用测试资源管理器（推荐）**

1. 确保已安装 **Python 扩展** 和 **Pytest 扩展**（如果可用）
2. 打开测试文件（如 `tests/test_baidu_recorded_2.py`）
3. 在函数名上方或行号旁边，会显示 **▶ Run Test** 或 **▶ Debug Test** 按钮
4. 点击按钮即可运行单个测试用例

**方法 2：使用命令面板**

1. 按 `Cmd+Shift+P` (Mac) 或 `Ctrl+Shift+P` (Windows/Linux)
2. 输入 `Python: Run Tests` 或 `Test: Run All Tests`
3. 选择要运行的测试

**方法 3：使用调试配置**

1. 按 `F5` 或点击左侧的 "运行和调试"
2. 选择 "Python: Current File (pytest)" 配置
3. 直接运行当前文件中的所有测试

**方法 4：在终端中运行**

在 Cursor 的集成终端中：
```bash
# 运行当前文件的测试
pytest tests/test_baidu_recorded_2.py

# 运行特定测试函数
pytest tests/test_baidu_recorded_2.py::test_example
```

### 运行标记的测试

运行冒烟测试：

```bash
pytest -m smoke
```

运行慢速测试：

```bash
pytest -m slow
```

### 无头模式（后台运行，不显示浏览器）

项目默认配置为**无头模式**（`headless=True`），测试在后台运行，不会弹出浏览器窗口。

如果需要看到浏览器操作过程，可以修改 `conftest.py` 中的 `headless=True` 为 `headless=False`。

### 测试视频录制

测试过程中会自动录制视频，视频保存在以下位置：

```
test-results/videos/
```

每个测试用例都会生成一个视频文件，文件名格式为：`<测试用例名>.webm`

**查看视频：**
```bash
# macOS
open test-results/videos/

# Windows
explorer test-results\videos\

# Linux
xdg-open test-results/videos/
```

**注意：** 视频会在测试用例执行完成后自动保存，无论测试是否通过。

### 查看测试报告

运行测试后会自动生成 `report.html` 文件，在浏览器中打开查看详细的测试报告。

```bash
open report.html  # macOS
# 或
start report.html  # Windows
```

## 测试用例说明

### test_baidu.py
- 测试百度搜索功能
- 测试百度首页元素
- 测试百度新闻链接

### test_github.py
- 测试 GitHub 首页
- 测试 GitHub 搜索功能
- 测试 GitHub Trending 页面
- 测试访问 GitHub 仓库

### test_google.py
- 测试 Google 搜索（如果可访问）

## 配置说明

### conftest.py
- 配置了浏览器实例、上下文和页面的 fixtures
- 默认使用 Chromium 浏览器
- 默认 `headless=True`（无头模式，后台运行，不显示浏览器）
- 自动录制测试视频，保存在 `test-results/videos/` 目录

### pytest.ini
- 配置了测试路径和标记
- 自动生成 HTML 测试报告
- 配置了测试标记：`smoke`（冒烟测试）、`slow`（慢速测试）

## 注意事项

1. 网络连接：确保可以访问测试的网站
2. 浏览器安装：首次运行前需要安装 Playwright 浏览器
3. 测试稳定性：真实网页测试可能因为网络或页面变更而不稳定
4. 等待策略：测试中使用了 `wait_for_load_state` 来等待页面加载完成

## 扩展测试

可以按照现有模式添加更多测试用例：

1. 在 `tests/` 目录下创建新的测试文件
2. 导入必要的模块
3. 使用 `page` fixture 进行页面操作
4. 使用 `expect` 进行断言验证

## 常见问题

### Q: 测试失败怎么办？
A: 检查网络连接，确保可以访问目标网站。某些网站可能会根据地区限制访问。

### Q: 如何调试测试？
A: 设置 `headless=False` 可以观看浏览器操作。也可以使用 `page.pause()` 暂停执行。所有测试的视频都会自动保存在 `test-results/videos/` 目录，可以回放查看。

### Q: 测试视频保存在哪里？
A: 测试视频保存在 `test-results/videos/` 目录下，每个测试用例对应一个 `.webm` 格式的视频文件。如果该目录不存在，运行测试时会自动创建。

### Q: 如何提高测试稳定性？
A: 使用适当的等待策略，如 `wait_for_selector`、`wait_for_load_state` 等。

## 使用 Playwright Codegen 录制生成代码

Playwright 提供了一个强大的代码生成工具（Codegen），可以通过录制浏览器操作自动生成测试代码。

### 基本用法（推荐：pytest 格式）

**推荐使用 `python-pytest` 格式**，这样生成的代码可以直接在项目中使用：

```bash
# 录制并生成 pytest 格式的测试代码（推荐）
playwright codegen \
  --target python-pytest \
  --browser chromium \
  --output tests/test_recorded.py \
  https://www.baidu.com
```

例如：

```bash
# 录制百度搜索操作（pytest 格式）
playwright codegen --target python-pytest --output tests/test_baidu.py https://www.baidu.com

# 录制 GitHub 操作（pytest 格式）
playwright codegen --target python-pytest --output tests/test_github.py https://github.com

# 使用普通 Python 格式（不推荐，需要手动修改）
playwright codegen --target python https://www.baidu.com
```

### 高级选项

```bash
# 指定输出格式为 python-pytest（推荐）
playwright codegen --target python-pytest --output tests/test_xxx.py https://www.baidu.com

# 指定浏览器（chromium, firefox, webkit）
playwright codegen --target python-pytest --browser chromium --output tests/test_xxx.py https://www.baidu.com

# 设置视口大小
playwright codegen --target python-pytest --viewport-size=1280,720 --output tests/test_xxx.py https://www.baidu.com

# 使用普通 Python 格式（需要手动转换为 pytest）
playwright codegen --target python https://www.baidu.com
```

### 完整命令示例

```bash
# 生成 pytest 格式代码并保存到文件（推荐）
playwright codegen \
  --target python-pytest \
  --browser chromium \
  --output tests/test_baidu_recorded.py \
  https://www.baidu.com
```

### 使用步骤

1. **启动 Codegen（使用 pytest 格式）**：
   ```bash
   playwright codegen \
     --target python-pytest \
     --output tests/test_recorded.py \
     https://www.baidu.com
   ```

2. **在打开的浏览器中操作**：
   - 浏览器会打开并显示操作提示
   - 你的所有操作（点击、输入、滚动等）都会被记录
   - 右侧会实时显示生成的代码

3. **停止录制**：
   - 按 `Ctrl+C` (Mac: `Cmd+C`) 停止录制
   - 代码会自动保存到 `--output` 指定的文件

4. **直接运行测试**：
   - 生成的 pytest 格式代码可以直接运行：
   ```bash
   pytest tests/test_recorded.py
   ```

### 示例：录制百度搜索

**推荐命令（pytest 格式）**：

```bash
# 录制百度搜索并保存为 pytest 格式
playwright codegen \
  --target python-pytest \
  --browser chromium \
  --output tests/test_baidu_recorded.py \
  https://www.baidu.com
```

操作步骤：

1. **启动录制**：运行上面的命令
2. **在浏览器中操作**：
   - 点击搜索框
   - 输入 "Playwright"
   - 点击搜索按钮
3. **停止录制**：按 `Ctrl+C`
4. **运行测试**：
   ```bash
   pytest tests/test_baidu_recorded.py
   ```

**生成的 pytest 格式代码示例**：

```python
from playwright.sync_api import Page, expect

def test_example(page: Page):
    page.goto("https://www.baidu.com/")
    page.locator("#kw").click()
    page.locator("#kw").fill("Playwright")
    page.locator("#su").click()
    expect(page).to_have_url("https://www.baidu.com/s?wd=Playwright")
```

### 集成到项目

使用 `--target python-pytest` 生成的代码已经符合 pytest 格式，可以直接使用。如果需要添加测试标记，可以这样修改：

```python
"""
录制的百度搜索测试用例
"""
import pytest
from playwright.sync_api import Page, expect

@pytest.mark.smoke  # 添加测试标记（可选）
def test_example(page: Page):
    """录制的百度搜索测试"""
    page.goto("https://www.baidu.com/")
    page.locator("#kw").click()
    page.locator("#kw").fill("Playwright")
    page.locator("#su").click()
    expect(page).to_have_url("https://www.baidu.com/s?wd=Playwright")
```

**注意**：使用 `--target python-pytest` 生成的代码已经包含了正确的函数签名 `def test_xxx(page: Page)`，无需手动修改！

### Codegen 快捷键

在录制过程中可以使用以下快捷键：

- `Ctrl/Cmd + C` - 停止录制
- `Ctrl/Cmd + \` - 清除生成的代码
- `Esc` - 退出 Codegen

### 注意事项

1. **代码需要优化**：生成的代码是基础版本，可能需要：
   - 添加等待策略（`wait_for_selector` 等）
   - 添加断言验证
   - 处理动态元素

2. **元素定位**：Codegen 会尝试生成最稳定的选择器，但可能需要手动调整

3. **代码风格**：生成的代码可能需要调整以符合项目的代码风格

