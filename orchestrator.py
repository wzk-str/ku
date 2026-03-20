#!/usr/bin/env python3
"""
敏感数据脱敏与审计系统 - 核心调度器模块

此模块是核心调度器，协调 scanner, sanitizer, auditor 的工作流。
必须作为其他模块的唯一调用者，避免模块间直接相互调用导致循环依赖。
"""

import os
from pathlib import Path
from typing import List, Dict, Any

# 导入子模块
import scanner
import sanitizer
import auditor


# 受保护文件列表 - 严禁处理这些文件
PROTECTED_FILES = {'.gitkeep', 'README.md'}


def is_protected_file(filename: str) -> bool:
    """检查文件是否受保护"""
    return filename in PROTECTED_FILES


def run(source_dir: str, output_dir: str, audit_report_path: str, config: dict):
    """
    主调度函数 - 协调整个脱敏工作流
    
    Args:
        source_dir: 源数据目录路径
        output_dir: 脱敏后输出目录路径
        audit_report_path: 审计报告输出路径
        config: 配置字典
    """
    # 从配置中获取脱敏规则
    rules = config.get('sanitization_rules', [])
    
    # 初始化审计日志
    auditor.log_event({
        'event_type': 'process_start',
        'source_dir': source_dir,
        'output_dir': output_dir,
        'rules_count': len(rules)
    })
    
    # 1. 扫描获取文件列表
    file_list = scanner.get_file_list(source_dir)
    
    # 过滤掉受保护文件
    filtered_files = [
        f for f in file_list 
        if not is_protected_file(os.path.basename(f))
    ]
    
    auditor.log_event({
        'event_type': 'files_scanned',
        'total_files': len(file_list),
        'processed_files': len(filtered_files),
        'protected_files_skipped': len(file_list) - len(filtered_files)
    })
    
    # 2. 处理每个文件
    processed_count = 0
    skipped_count = 0
    error_count = 0
    
    for file_path in filtered_files:
        try:
            result = process_single_file(file_path, source_dir, output_dir, rules)
            if result['success']:
                processed_count += 1
            else:
                skipped_count += 1
        except Exception as e:
            error_count += 1
            auditor.log_event({
                'event_type': 'file_error',
                'file_path': file_path,
                'error_message': str(e)
            })
    
    # 3. 记录处理摘要
    auditor.log_event({
        'event_type': 'process_complete',
        'processed_count': processed_count,
        'skipped_count': skipped_count,
        'error_count': error_count
    })
    
    # 4. 生成审计报告
    auditor.generate_report(audit_report_path)
    
    print(f"处理完成: {processed_count} 个文件已脱敏, {skipped_count} 个文件跳过, {error_count} 个错误")


def process_single_file(file_path: str, source_dir: str, output_dir: str, rules: List[Dict]) -> Dict[str, Any]:
    """
    处理单个文件
    
    Args:
        file_path: 文件完整路径
        source_dir: 源目录（用于计算相对路径）
        output_dir: 输出目录
        rules: 脱敏规则列表
    
    Returns:
        处理结果字典
    """
    filename = os.path.basename(file_path)
    
    # 检查是否为受保护文件（双重检查）
    if is_protected_file(filename):
        return {'success': False, 'reason': 'protected_file'}
    
    # 检查文件扩展名
    if not filename.endswith(('.txt', '.log')):
        return {'success': False, 'reason': 'unsupported_format'}
    
    # 计算相对路径，保持目录结构
    rel_path = os.path.relpath(file_path, source_dir)
    output_path = os.path.join(output_dir, rel_path)
    
    # 确保输出目录存在
    output_dir_path = os.path.dirname(output_path)
    if output_dir_path:
        os.makedirs(output_dir_path, exist_ok=True)
    
    # 读取文件内容
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
    except UnicodeDecodeError:
        # 尝试使用其他编码
        with open(file_path, 'r', encoding='gbk', errors='ignore') as f:
            content = f.read()
    except Exception as e:
        raise Exception(f"读取文件失败: {e}")
    
    # 记录原始文件信息
    original_size = len(content)
    
    # 调用 sanitizer 进行脱敏处理
    sanitized_content = sanitizer.process_content(content, rules)
    
    # 写入脱敏后的内容
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(sanitized_content)
    
    # 记录审计日志
    auditor.log_event({
        'event_type': 'file_processed',
        'source_file': file_path,
        'output_file': output_path,
        'original_size': original_size,
        'sanitized_size': len(sanitized_content),
        'rules_applied': len(rules)
    })
    
    return {'success': True}
