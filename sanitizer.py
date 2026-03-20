#!/usr/bin/env python3
"""
敏感数据脱敏与审计系统 - 脱敏核心模块

此模块仅暴露 process_content(text, rules) 函数。
禁止在此模块中进行文件读写操作。
"""

import re
from typing import List, Dict, Any


def process_content(text: str, rules: List[Dict[str, Any]]) -> str:
    """
    对文本内容进行脱敏处理
    
    Args:
        text: 原始文本内容
        rules: 脱敏规则列表，每个规则是一个字典，包含:
            - pattern: 正则表达式模式
            - replacement: 替换字符串
            - description: 规则描述（可选）
    
    Returns:
        脱敏后的文本内容
    """
    if not text:
        return text
    
    if not rules:
        return text
    
    result = text
    
    for rule in rules:
        pattern = rule.get('pattern', '')
        replacement = rule.get('replacement', '[REDACTED]')
        
        if not pattern:
            continue
        
        try:
            # 使用正则表达式进行替换
            flags = 0
            if rule.get('case_insensitive', False):
                flags |= re.IGNORECASE
            
            result = re.sub(pattern, replacement, result, flags=flags)
        except re.error:
            # 如果正则表达式无效，跳过此规则
            continue
    
    return result


def mask_phone_number(text: str) -> str:
    """
    脱敏手机号 - 保留前3位和后4位，中间用*代替
    
    Args:
        text: 原始文本
    
    Returns:
        脱敏后的文本
    """
    pattern = r'(1[3-9]\d)\d{4}(\d{4})'
    replacement = r'\1****\2'
    return re.sub(pattern, replacement, text)


def mask_id_card(text: str) -> str:
    """
    脱敏身份证号 - 保留前6位和后4位，中间用*代替
    
    Args:
        text: 原始文本
    
    Returns:
        脱敏后的文本
    """
    pattern = r'(\d{6})\d{8,11}(\d{4})'
    replacement = r'\1***********\2'
    return re.sub(pattern, replacement, text)


def mask_email(text: str) -> str:
    """
    脱敏邮箱 - 保留邮箱名首字母和域名，中间用*代替
    
    Args:
        text: 原始文本
    
    Returns:
        脱敏后的文本
    """
    pattern = r'([a-zA-Z0-9])[a-zA-Z0-9._-]*(@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,})'
    replacement = r'\1****\2'
    return re.sub(pattern, replacement, text)


def mask_bank_card(text: str) -> str:
    """
    脱敏银行卡号 - 保留前4位和后4位，中间用*代替
    
    Args:
        text: 原始文本
    
    Returns:
        脱敏后的文本
    """
    pattern = r'(\d{4})\d{8,12}(\d{4})'
    replacement = r'\1 **** **** \2'
    return re.sub(pattern, replacement, text)


def mask_ip_address(text: str) -> str:
    """
    脱敏IP地址 - 隐藏最后一段
    
    Args:
        text: 原始文本
    
    Returns:
        脱敏后的文本
    """
    pattern = r'(\d{1,3}\.\d{1,3}\.\d{1,3})\.\d{1,3}'
    replacement = r'\1.***'
    return re.sub(pattern, replacement, text)
