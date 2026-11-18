```python
def parse_duration(s: str) -> int:
    s = s.strip()
    if not s:
        raise ValueError("빈 문자열 또는 공백만 포함")
    
    total = 0
    i, n = 0, len(s)
    last_ord = -1
    units = {'d': 86400, 'h': 3600, 'm': 60, 's': 1}
    order = {'d': 0, 'h': 1, 'm': 2, 's': 3}

    while i < n:
        if not s[i].isdigit():
            raise ValueError("잘못된 형식")
        
        num_start = i
        while i < n and s[i].isdigit():
            i += 1
        num = int(s[num_start:i])
        
        if i >= n or s[i] not in units:
            raise ValueError("단위 누락 또는 알 수 없는 단위")
            
        unit = s[i]
        i += 1
        
        curr_ord = order[unit]
        if curr_ord <= last_ord:
            raise ValueError("순서 위반 또는 중복 단위")
        last_ord = curr_ord
        
        total += num * units[unit]
        
    return total
```