#!/usr/bin/env python3
"""
敏感数据脱敏与审计系统 - 审计模块

此模块仅暴露 log_event(event_data) 和 generate_report(output_path) 函数。
负责记录所有脱敏操作事件并生成不可篡改的审计报告。
"""

import json
import hashlib
import time
from datetime import datetime
from typing import Dict, Any, List


# 存储审计事件的列表
_audit_events: List[Dict[str, Any]] = []


def _generate_event_hash(event: Dict[str, Any], previous_hash: str = '') -> str:
    """
    生成事件的哈希值，用于确保审计记录的不可篡改性
    
    Args:
        event: 事件数据字典
        previous_hash: 前一个事件的哈希值（用于链式哈希）
    
    Returns:
        SHA-256 哈希字符串
    """
    # 创建事件数据的字符串表示
    event_str = json.dumps(event, sort_keys=True, ensure_ascii=False)
    # 添加前一个哈希值，形成链式结构
    data_to_hash = f"{previous_hash}:{event_str}"
    # 计算 SHA-256 哈希
    return hashlib.sha256(data_to_hash.encode('utf-8')).hexdigest()


def log_event(event_data: Dict[str, Any]):
    """
    记录一个审计事件
    
    Args:
        event_data: 事件数据字典，应包含 event_type 等字段
    """
    global _audit_events
    
    # 添加时间戳
    event = event_data.copy()
    event['timestamp'] = datetime.now().isoformat()
    event['sequence'] = len(_audit_events) + 1
    
    # 计算前一个哈希值
    previous_hash = ''
    if _audit_events:
        previous_hash = _audit_events[-1].get('hash', '')
    
    # 计算当前事件的哈希值
    event['hash'] = _generate_event_hash(event, previous_hash)
    
    # 存储事件
    _audit_events.append(event)


def generate_report(output_path: str):
    """
    生成 JSON 格式的审计报告
    
    Args:
        output_path: 审计报告输出路径（必须是 .json 文件）
    """
    global _audit_events
    
    # 构建报告结构
    report = {
        'report_metadata': {
            'generated_at': datetime.now().isoformat(),
            'version': '1.0',
            'total_events': len(_audit_events)
        },
        'events': _audit_events,
        'integrity': _calculate_integrity_hash()
    }
    
    # 写入 JSON 文件
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(report, f, indent=2, ensure_ascii=False)


def _calculate_integrity_hash() -> str:
    """
    计算整个审计日志的完整性哈希
    
    Returns:
        SHA-256 哈希字符串
    """
    global _audit_events
    
    if not _audit_events:
        return ''
    
    # 将所有事件的哈希值连接起来进行最终哈希
    all_hashes = ''.join(event.get('hash', '') for event in _audit_events)
    return hashlib.sha256(all_hashes.encode('utf-8')).hexdigest()


def get_events() -> List[Dict[str, Any]]:
    """
    获取所有审计事件的副本（用于测试和调试）
    
    Returns:
        审计事件列表的副本
    """
    global _audit_events
    return _audit_events.copy()


def clear_events():
    """
    清除所有审计事件（用于测试）
    """
    global _audit_events
    _audit_events = []
