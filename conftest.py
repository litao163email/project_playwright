"""
pytest 配置文件和 Playwright fixtures
"""
import os
import time
import pytest
from playwright.sync_api import Page, Browser, BrowserContext


# 存储测试用例和对应的视频路径
_test_videos = {}


@pytest.fixture(scope="session")
def browser():
    """
    创建浏览器实例（会话级别，所有测试共享）
    """
    from playwright.sync_api import sync_playwright
    
    with sync_playwright() as p:
        # 可以选择浏览器类型: chromium, firefox, webkit
        # headless=True 表示无头模式（后台运行，不显示浏览器窗口）
        browser = p.chromium.launch(headless=True)
        yield browser
        browser.close()


@pytest.fixture
def context(browser: Browser, request):
    """
    创建浏览器上下文（每个测试用例一个独立的上下文）
    配置了视频录制，无论测试成功与否都会保存视频到 test-results/videos/ 目录
    """
    # 创建视频保存目录
    video_dir = os.path.join(os.getcwd(), "test-results", "videos")
    os.makedirs(video_dir, exist_ok=True)
    
    # 获取测试用例名称，用于视频文件名
    test_name = request.node.name
    test_id = request.node.nodeid
    
    context = browser.new_context(
        viewport={"width": 1920, "height": 1080},
        # 可以设置用户代理
        user_agent="Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36",
        # 录制视频配置：录制所有测试的视频
        record_video_dir=video_dir,
        record_video_size={"width": 1920, "height": 1080},
    )
    
    # 保存测试信息和上下文
    context._test_name = test_name
    context._test_id = test_id
    context._video_dir = video_dir
    
    # 记录测试开始时间
    _test_videos[test_id] = {
        'name': test_name,
        'video_dir': video_dir,
        'start_time': time.time()
    }
    
    yield context
    
    # 无论测试成功与否，都保存视频
    try:
        # 关闭上下文，这会保存视频
        # Playwright 默认只在失败时保存，我们需要强制保存所有视频
        context.close()
        
        # 等待视频文件写入完成
        time.sleep(0.5)
        
        # 处理视频文件重命名
        _rename_test_video(test_id, test_name, video_dir)
    except Exception:
        # 确保即使出错也关闭上下文
        try:
            context.close()
        except Exception:
            pass


def _rename_test_video(test_id, test_name, video_dir):
    """
    重命名测试视频文件
    """
    try:
        # 获取 video_dir 中所有的 .webm 文件
        if not os.path.exists(video_dir):
            return
            
        video_files = [f for f in os.listdir(video_dir) if f.endswith('.webm')]
        
        if video_files:
            # 找到最新创建的文件（在测试开始时间之后创建的）
            test_info = _test_videos.get(test_id, {})
            start_time = test_info.get('start_time', 0)
            
            # 筛选在测试开始后创建的文件
            recent_videos = []
            for f in video_files:
                file_path = os.path.join(video_dir, f)
                try:
                    file_ctime = os.path.getctime(file_path)
                    if file_ctime >= start_time - 1:  # 允许1秒误差
                        recent_videos.append((f, file_ctime))
                except Exception:
                    continue
            
            if recent_videos:
                # 按创建时间排序，最新的应该是刚创建的
                recent_videos.sort(key=lambda x: x[1], reverse=True)
                latest_video = recent_videos[0][0]
                old_path = os.path.join(video_dir, latest_video)
                
                # 生成新的视频文件名（使用测试用例名称）
                test_file_name = test_name.replace("[", "_").replace("]", "_")
                new_video_path = os.path.join(video_dir, f"{test_file_name}.webm")
                
                # 如果目标文件已存在，添加时间戳
                if os.path.exists(new_video_path):
                    timestamp = int(time.time())
                    new_video_path = os.path.join(video_dir, f"{test_file_name}_{timestamp}.webm")
                
                # 重命名视频文件
                try:
                    if os.path.exists(old_path):
                        os.rename(old_path, new_video_path)
                except Exception:
                    pass  # 如果重命名失败，使用原始文件名
    except Exception:
        pass


@pytest.hookimpl(trylast=True)
def pytest_runtest_makereport(item, call):
    """
    pytest hook: 在测试完成后处理视频
    这个 hook 确保无论测试成功与否，视频都会被保存
    """
    # 只在测试完成后执行（teardown 阶段）
    if call.when == "teardown":
        test_id = item.nodeid
        if test_id in _test_videos:
            test_info = _test_videos[test_id]
            test_name = test_info['name']
            video_dir = test_info['video_dir']
            
            # 确保视频被重命名
            _rename_test_video(test_id, test_name, video_dir)


@pytest.fixture
def page(context: BrowserContext):
    """
    创建页面实例（每个测试用例一个新的页面）
    """
    page = context.new_page()
    yield page
    page.close()

