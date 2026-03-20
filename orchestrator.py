import os
import shutil
import yaml

from scanner import get_file_list
from sanitizer import process_content
from auditor import log_event, generate_report

def load_config(config_path):
    with open(config_path, 'r', encoding='utf-8') as f:
        return yaml.safe_load(f)

def run_pipeline(source_path, output_path, audit_report_path, config_path):
    config = load_config(config_path)
    rules = config.get('sensitive_patterns', [])
    
    log_event({
        'event_type': 'pipeline_start',
        'file_path': source_path,
        'details': {'rules_count': len(rules)}
    })
    
    os.makedirs(output_path, exist_ok=True)
    
    files = get_file_list(source_path)
    
    log_event({
        'event_type': 'scan_complete',
        'file_path': source_path,
        'details': {'files_found': len(files)}
    })
    
    processed_count = 0
    error_count = 0
    
    for file_info in files:
        src_full_path = file_info['full_path']
        rel_path = file_info['relative_path']
        dst_full_path = os.path.join(output_path, rel_path)
        
        try:
            with open(src_full_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            original_size = len(content)
            
            cleaned_content, matches = process_content(content, rules)
            
            os.makedirs(os.path.dirname(dst_full_path), exist_ok=True)
            
            with open(dst_full_path, 'w', encoding='utf-8') as f:
                f.write(cleaned_content)
            
            log_event({
                'event_type': 'file_processed',
                'file_path': rel_path,
                'details': {
                    'original_size': original_size,
                    'cleaned_size': len(cleaned_content),
                    'matches_found': len(matches),
                    'match_details': matches[:10]
                }
            })
            
            processed_count += 1
            
        except Exception as e:
            log_event({
                'event_type': 'file_error',
                'file_path': rel_path,
                'details': {'error': str(e)}
            })
            error_count += 1
    
    log_event({
        'event_type': 'pipeline_complete',
        'file_path': output_path,
        'details': {
            'processed': processed_count,
            'errors': error_count
        }
    })
    
    generate_report(audit_report_path)
    
    return {
        'processed': processed_count,
        'errors': error_count,
        'report_path': audit_report_path
    }
