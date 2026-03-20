#!/usr/bin/env python3
"""
敏感数据脱敏与审计系统 - 文件遍历模块

此模块仅暴露 get_file_list(root_path) 函数。
负责遍历目录并返回符合条件的文件列表。
"""

import os
from pathlib import Path
from typing import List


# 受保护文件列表 - 扫描时忽略这些文件
PROTECTED_FILES = {'.gitkeep', 'README.md'}


def get_file_list(root_path: str) -> List[str]:
    """
    遍历指定目录，返回所有文件的路径列表
    
    Args:
        root_path: 要遍历的根目录路径
    
    Returns:
        文件完整路径的列表（仅包含 .txt 和 .log 文件）
    """
    file_list = []
    root = Path(root_path)
    
    if not root.exists():
        return file_list
    
    if not root.is_dir():
        return file_list
    
    # 递归遍历目录
    for item in root.rglob('*'):
        if item.is_file():
            filename = item.name
            
            # 跳过受保护文件
            if filename in PROTECTED_FILES:
                continue
            
            # 仅处理 .txt 和 .log 文件
            if filename.endswith(('.txt', '.log')):
                file_list.append(str(item.resolve()))
    
    # 按路径排序，确保处理顺序一致
    file_list.sort()
    
    return file_list
