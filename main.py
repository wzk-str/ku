import os
import sys

from orchestrator import run_pipeline

SOURCE_PATH = os.path.join('.', 'source_data')
OUTPUT_PATH = os.path.join('.', 'cleaned_data')
AUDIT_DIR = os.path.join('.', 'audit_logs')
CONFIG_PATH = os.path.join('.', 'config.yaml')
AUDIT_REPORT_PATH = os.path.join(AUDIT_DIR, 'audit_report.json')

def main():
    print("=" * 50)
    print("敏感数据脱敏与审计系统")
    print("=" * 50)
    
    print(f"\n[配置] 源数据目录: {SOURCE_PATH}")
    print(f"[配置] 输出目录: {OUTPUT_PATH}")
    print(f"[配置] 审计报告: {AUDIT_REPORT_PATH}")
    
    if not os.path.exists(CONFIG_PATH):
        print(f"\n[错误] 配置文件不存在: {CONFIG_PATH}")
        sys.exit(1)
    
    if not os.path.exists(SOURCE_PATH):
        print(f"\n[警告] 源数据目录不存在，正在创建: {SOURCE_PATH}")
        os.makedirs(SOURCE_PATH, exist_ok=True)
        print("[提示] 请将需要脱敏的 .txt 或 .log 文件放入 source_data 目录后重新运行")
        return
    
    print("\n[开始] 执行脱敏处理流水线...")
    
    result = run_pipeline(
        source_path=SOURCE_PATH,
        output_path=OUTPUT_PATH,
        audit_report_path=AUDIT_REPORT_PATH,
        config_path=CONFIG_PATH
    )
    
    print("\n" + "=" * 50)
    print("[完成] 处理结果:")
    print(f"  - 成功处理文件数: {result['processed']}")
    print(f"  - 处理错误数: {result['errors']}")
    print(f"  - 审计报告路径: {result['report_path']}")
    print("=" * 50)

if __name__ == '__main__':
    main()
