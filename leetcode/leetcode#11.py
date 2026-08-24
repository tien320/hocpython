def container(height):
    n = len(height)
    left = 0
    right = n-1
    max_S = 0
    while left<right:
        curr_width = right - left
        curr_height = min(height[left],height[right])
        curr_S = curr_width * curr_height
        if curr_S > max_S : max_S = curr_S
        if height[left] < height[right]: left +=1
        else: right -=1
    return max_S
if __name__ == "__main__":
    height = [1,8,6,2,5,4,8,3,7]
    print(container(height))
