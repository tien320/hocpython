def topkfrequent(nums,k):
    count_map = {}
    for num in nums:
        if num in count_map:
            count_map[num] +=1
        else:
            count_map[num] =1
    n =len(nums)
    bucket = [[] for i in range(n+1)]
    for num in count_map:
        freq = count_map[num]
        bucket[freq].append(num)
    res = []
    freq =n
    while freq>0:
        for num in bucket[freq]:
            res.append(num)
        if len(res) == k: return res
        freq -=1
    return res
if __name__ == "__main__":
    nums = [1,2,1,1,2,3,4,5,3]
    k = 3
    print(topkfrequent(nums,k))