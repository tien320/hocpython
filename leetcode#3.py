def longest():
    last_seen = [-1] *128
    left = 0
    max_len =0
    for right in range(len(s)):
        cod = ord(s[right])
        if last_seen[cod] >= left:
           left = last_seen[cod]+1
           last_seen[cod] = right
           current_len = right - left +1
        if current_len >max_len:
                max_len = current_len      
    return max_len