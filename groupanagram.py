def groupAnagrams(strs: list[str]) -> list[list[str]]:
    groups = {}
    for s in strs:
        key = "".join(sorted(s))
        # Kiểm tra key đã có trong dict chưa
        if key not in groups:
            groups[key] = []
        groups[key].append(s)
        
    # Gom tất cả các danh sách kết quả lại
    result = []
    for key in groups:
        result.append(groups[key])   
    print(result)
if __name__ == "__main__":
    strs = str(input())
    ket_qua = groupAnagrams(strs)