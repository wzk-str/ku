#!/usr/bin/env python3
"""
敏感数据脱敏与审计系统 - 主入口模块

此文件是唯一入口，仅负责初始化配置和调用 orchestrator 模块。
禁止在此文件中定义业务逻辑函数。
"""

import os
import sys
import yaml
from pathlib import Path


def load_config(config_path: str) -> dict:
    """加载 YAML 配置文件"""
    with open(config_path, 'r', encoding='utf-8') as f:
        return yaml.safe_load(f)


def resolve_paths() -> dict:
    """
    统一解析所有路径，作为参数传递给下游函数。
    所有路径解析在此完成，严禁在各子模块中硬编码路径字符串。
    """
    base_dir = Path(__file__).parent.resolve()
    
    paths = {
        'source_dir': base_dir / 'source_data',
        'output_dir': base_dir / 'cleaned_data',
        'audit_dir': base_dir / 'audit_logs',
        'config_file': base_dir / 'config.yaml',
        'audit_report': base_dir / 'audit_logs' / 'audit_report.json'
    }
    
    return paths


def main():
    """主函数 - 系统入口"""
    # 解析所有路径
    paths = resolve_paths()
    
    # 检查配置文件是否存在
    if not paths['config_file'].exists():
        print(f"错误: 配置文件不存在: {paths['config_file']}")
        sys.exit(1)
    
    # 加载配置
    try:
        config = load_config(str(paths['config_file']))
    except Exception as e:
        print(f"错误: 加载配置文件失败: {e}")
        sys.exit(1)
    
    # 检查源目录是否存在
    if not paths['source_dir'].exists():
        print(f"错误: 源数据目录不存在: {paths['source_dir']}")
        sys.exit(1)
    
    # 确保输出目录存在
    paths['output_dir'].mkdir(parents=True, exist_ok=True)
    paths['audit_dir'].mkdir(parents=True, exist_ok=True)
    
    # 导入并调用 orchestrator 模块
    try:
        import orchestrator
        orchestrator.run(
            source_dir=str(paths['source_dir']),
            output_dir=str(paths['output_dir']),
            audit_report_path=str(paths['audit_report']),
            config=config
        )
        print("脱敏处理完成。审计报告已生成。")
    except Exception as e:
        print(f"错误: 处理过程中发生异常: {e}")
        sys.exit(1)


if __name__ == '__main__':
    main()
