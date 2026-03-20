import re

def process_content(text, rules):
    if not text or not rules:
        return text, []
    
    processed_text = text
    matches_found = []
    
    for rule in rules:
        pattern = rule.get('pattern', '')
        name = rule.get('name', 'unknown')
        replacement = rule.get('replacement', '[REDACTED]')
        
        if not pattern:
            continue
        
        try:
            regex = re.compile(pattern)
            found_matches = regex.findall(processed_text)
            
            if found_matches:
                for match in found_matches:
                    matches_found.append({
                        'rule_name': name,
                        'matched_value': str(match)[:50]
                    })
                
                processed_text = regex.sub(replacement, processed_text)
        except re.error:
            continue
    
    return processed_text, matches_found
