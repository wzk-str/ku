import json
import os
import hashlib
from datetime import datetime

_audit_events = []

def log_event(event_data):
    if not isinstance(event_data, dict):
        return False
    
    event = {
        'timestamp': datetime.now().isoformat(),
        'event_type': event_data.get('event_type', 'unknown'),
        'file_path': event_data.get('file_path', ''),
        'details': event_data.get('details', {}),
        'checksum': ''
    }
    
    event_str = json.dumps(event, sort_keys=True)
    event['checksum'] = hashlib.sha256(event_str.encode()).hexdigest()[:16]
    
    _audit_events.append(event)
    return True

def generate_report(output_path):
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    
    report = {
        'generated_at': datetime.now().isoformat(),
        'total_events': len(_audit_events),
        'events': _audit_events
    }
    
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(report, f, ensure_ascii=False, indent=2)
    
    return output_path
