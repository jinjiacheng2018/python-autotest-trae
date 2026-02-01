import pytest
import os
import sys
import shutil
import subprocess


def app():
    """
    统一执行 pytest 测试入口
    支持：
    1. pytest.ini 配置自动生效（testcases、markers、addopts）
    2. Allure 报告输出到根目录 report/allure-results
    3. 可命令行指定单个测试文件或测试目录
    """

    # 1、确保工作目录是项目根目录,切换Python当前工作目录到项目根目录（pytest.ini 所在目录）
    root_dir = os.path.dirname(os.path.abspath(__file__))
    os.chdir(root_dir)

    # 2、清空旧 Allure 报告
    allure_result_dir = os.path.join(root_dir, "report", "allure-results")
    allure_html_dir = os.path.join(root_dir, "report", "allure-html")

    if os.path.exists(allure_result_dir):
        print(f"清理旧的 Allure 报告: {allure_result_dir}")
        shutil.rmtree(allure_result_dir)

    if os.path.exists(allure_html_dir):
        print(f"清理旧的 Allure HTML 报告: {allure_html_dir}")
        shutil.rmtree(allure_html_dir)

    # 保证目录存在
    os.makedirs(allure_result_dir, exist_ok=True)
    os.makedirs(allure_html_dir, exist_ok=True)

    #  3、构建 pytest 参数列表，q 简洁输出，-s 保留 print 输出
    pytest_args = ["-q", "-s"]

    # 4、命令行参数可指定测试文件/目录，如果没有指定，则 pytest 会根据 pytest.ini testcases 收集用例
    if len(sys.argv) > 1:
        # 命令行没有传参是此逻辑不仅如此，例：python app.py testcases/test_01_get_user_info.py
        pytest_args += sys.argv[1:]
    # else:
    #     # 若需要指定某个用例文件时：将else放开
    #     pytest_args += ["testcases/api_test/test_02_register.py"]

    # 5、调用 pytest.main 执行
    exit_code = pytest.main(pytest_args)

    # 6、生成并打开 Allure 报告
    if exit_code == 0 or exit_code == 1:
        print("测试执行完成，开始生成 Allure 报告...")
        try:
            # 生成报告
            # 注意：allure 命令需要在系统环境变量中
            generate_cmd = f"allure generate \"{allure_result_dir}\" -o \"{allure_html_dir}\" --clean"
            print(f"执行命令: {generate_cmd}")
            subprocess.run(generate_cmd, shell=True, check=True)
            
            print(f"Allure 报告生成成功: {allure_html_dir}")
            
            # 打开报告
            # 注意：allure open 会启动一个服务并阻塞，直到手动停止
            print("正在打开 Allure 报告 (Ctrl+C 可停止服务)...")
            open_cmd = f"allure open \"{allure_html_dir}\""
            subprocess.run(open_cmd, shell=True)
            
        except subprocess.CalledProcessError as e:
            print(f"生成报告失败: {e}")
        except Exception as e:
            print(f"发生错误: {e}")
    else:
        print(f"测试执行异常或无用例执行 (Exit Code: {exit_code})，跳过报告生成。")

    # 7、返回退出码（可用于 CI/CD）
    sys.exit(exit_code)


if __name__ == "__main__":
    app()
