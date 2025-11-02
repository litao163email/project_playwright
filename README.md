# Playwright + Pytest 测试项目

这是一个使用 Playwright 和 pytest 编写的自动化测试项目，用于测试本地 Web 应用。

## 项目结构

```
test_playwright/
├── tests/                    # 测试用例目录
│   ├── __init__.py
│   ├── test_readbook.py      # 读书网站测试用例
│   └── test_readbook_3.py    # 读书网站测试用例
├── conftest.py              # pytest fixtures 和配置
├── pytest.ini               # pytest 配置文件
├── requirements.txt         # Python 依赖
├── record.sh                # 录制脚本（自动生成测试用例）
├── test-results/            # 测试结果和视频
│   └── videos/              # 测试视频保存目录
└── README.md               # 项目说明

```

## 安装步骤

### 1. 安装 Python 依赖

```bash
pip install -r requirements.txt
```

或使用 Python 3：

```bash
python3 -m pip install -r requirements.txt
```

### 2. 安装 Playwright 浏览器

```bash
playwright install chromium
```

或者安装所有浏览器：

```bash
playwright install
```

## 快速开始

### 使用录制脚本生成测试用例（推荐）

项目提供了便捷的录制脚本，可以自动录制操作并生成测试代码：

```bash
# 使用默认配置（http://localhost:18001/）
./record.sh

# 指定网址和输出文件
./record.sh http://localhost:18001/ tests/test_readbook.py

# 自定义输出文件名
./record.sh http://localhost:18001/ tests/test_custom.py
```

**录制脚本特点：**
- ✅ 自动生成 pytest 格式代码
- ✅ 自动将测试函数名改为与文件名一致（例如：`test_readbook.py` → `def test_readbook()`）
- ✅ 直接可用的测试代码

## 运行测试

### 运行所有测试

```bash
pytest
```

### 运行特定测试文件

```bash
pytest tests/test_readbook.py
```

### 运行特定测试用例

```bash
pytest tests/test_readbook.py::test_readbook
```

### 在 Cursor/VS Code 中直接运行测试

**方法 1：使用任务运行（最简单）**

1. 打开测试文件
2. 按 `Cmd+Shift+B` (Mac) 或 `Ctrl+Shift+B` (Windows/Linux)
3. 自动运行当前测试文件

**方法 2：使用调试功能 (F5)**

1. 打开测试文件
2. 按 `F5` 或点击左侧的 "运行和调试"
3. 选择 "Python: Current File (pytest)"

**方法 3：使用命令面板**

1. 按 `Cmd+Shift+P` (Mac) 或 `Ctrl+Shift+P` (Windows/Linux)
2. 输入 `Tasks: Run Task`
3. 选择 `Run Current Test File`

**方法 4：在终端中运行**

```bash
# 运行当前文件的测试
pytest tests/test_readbook.py

# 运行特定测试函数
pytest tests/test_readbook.py::test_readbook -v
```

### 运行标记的测试

```bash
# 运行冒烟测试
pytest -m smoke

# 运行慢速测试
pytest -m slow
```

## 配置说明

### conftest.py
- 配置了浏览器实例、上下文和页面的 fixtures
- 默认使用 Chromium 浏览器
- 默认 `headless=True`（无头模式，后台运行，不显示浏览器）
- 自动录制测试视频，保存在 `test-results/videos/` 目录

### pytest.ini
- 配置了测试路径和标记
- 自动生成 HTML 测试报告（`report.html`）
- 配置了测试标记：`smoke`（冒烟测试）、`slow`（慢速测试）

### record.sh
- 便捷的录制脚本，自动生成 pytest 格式代码
- 自动将测试函数名改为与文件名一致
- 默认录制目标：`http://localhost:18001/`

## 测试视频录制

测试过程中会自动录制视频，视频保存在：

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

**注意：** 测试视频会在测试用例执行完成后自动保存，无论测试是否通过。

### 查看测试报告

运行测试后会自动生成 `report.html` 文件，在浏览器中打开查看详细的测试报告。

```bash
open report.html  # macOS
# 或
start report.html  # Windows
```

## 使用 Playwright Codegen 录制生成代码

### 使用录制脚本（推荐）

最简单的方式是使用项目提供的 `record.sh` 脚本：

```bash
# 使用默认配置
./record.sh

# 指定网址和输出文件
./record.sh http://localhost:18001/ tests/test_my_feature.py
```

**脚本会自动：**
- 生成 pytest 格式代码
- 将测试函数名改为与文件名一致
- 保存到指定文件

### 直接使用 Codegen 命令

```bash
# 录制并生成 pytest 格式代码
playwright codegen \
  --target python-pytest \
  --browser chromium \
  --output tests/test_recorded.py \
  http://localhost:18001/
```

### 使用步骤

1. **启动录制**：
   ```bash
   ./record.sh http://localhost:18001/ tests/test_readbook.py
   ```

2. **在打开的浏览器中操作**：
   - 浏览器会打开并显示操作提示
   - 你的所有操作（点击、输入、滚动等）都会被记录
   - 右侧会实时显示生成的代码

3. **停止录制**：
   - 按 `Ctrl+C` (Mac: `Cmd+C`) 停止录制
   - 代码会自动保存，并自动将函数名改为与文件名一致

4. **直接运行测试**：
   ```bash
   pytest tests/test_readbook.py
   ```

### 生成的代码示例

录制 `tests/test_readbook.py` 后，生成的代码类似：

```python
from playwright.sync_api import Page, expect

def test_readbook(page: Page) -> None:
    page.goto("http://localhost:18001/")
    page.get_by_placeholder("书名、作者、关键字").click()
    page.get_by_placeholder("书名、作者、关键字").fill("ni")
    page.locator("#btnSearch i").click()
    # ... 更多操作
```

**注意：** 脚本会自动将 `test_example` 替换为 `test_readbook`（与文件名一致）

## 项目特性

- ✅ **自动视频录制**：所有测试都会自动录制视频
- ✅ **便捷录制脚本**：`record.sh` 一键录制并生成测试代码
- ✅ **智能函数命名**：测试函数名自动与文件名匹配
- ✅ **无头模式运行**：默认后台运行，不显示浏览器
- ✅ **HTML 测试报告**：自动生成详细的测试报告

## 注意事项

1. **本地服务**：确保 `http://localhost:18001/` 服务正在运行
2. **浏览器安装**：首次运行前需要安装 Playwright 浏览器
3. **测试稳定性**：真实网页测试可能因为页面变更而不稳定
4. **等待策略**：测试中使用了适当的等待策略来确保稳定性

## 常见问题

### Q: 测试失败怎么办？
A: 检查本地服务是否运行，确保可以访问 `http://localhost:18001/`。查看测试视频可以帮助诊断问题。

### Q: 如何调试测试？
A: 
- 设置 `headless=False` 可以观看浏览器操作
- 使用 `page.pause()` 暂停执行
- 查看 `test-results/videos/` 目录中的测试视频

### Q: 测试视频保存在哪里？
A: 测试视频保存在 `test-results/videos/` 目录下，每个测试用例对应一个 `.webm` 格式的视频文件。

### Q: 如何提高测试稳定性？
A: 使用适当的等待策略，如 `wait_for_selector`、`wait_for_load_state` 等。生成的录制代码可能需要手动优化。

### Q: 录制脚本如何使用？
A: 
```bash
# 基本用法
./record.sh

# 自定义网址和文件名
./record.sh http://localhost:18001/ tests/test_custom.py
```

录制完成后，脚本会自动：
- 将测试函数名改为与文件名一致
- 生成可直接运行的 pytest 格式代码

## 扩展测试

可以按照以下方式添加更多测试用例：

1. **使用录制脚本**：
   ```bash
   ./record.sh http://localhost:18001/ tests/test_my_feature.py
   ```

2. **手动编写测试**：
   - 在 `tests/` 目录下创建新的测试文件
   - 导入必要的模块：`from playwright.sync_api import Page, expect`
   - 使用 `page` fixture 进行页面操作
   - 使用 `expect` 进行断言验证

## 示例测试用例

当前项目包含的测试用例：

- `test_readbook.py` - 读书网站功能测试
- `test_readbook_3.py` - 读书网站功能测试（排行榜等）

## 开发建议

1. **使用录制脚本**：对于复杂流程，先录制再优化代码
2. **优化选择器**：录制生成的选择器可能需要优化，优先使用 ID 或稳定的选择器
3. **添加等待**：对于动态内容，添加适当的等待策略
4. **查看视频**：测试失败时，查看视频可以帮助快速定位问题
