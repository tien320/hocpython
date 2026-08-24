from collections import deque
def numisland(grid):
    if not grid:
        return
    rows = len(grid)
    cols = len(grid[0])
    num_island = 0
    direction = [(0,1),(0,-1),(1,0),(-1,0)]
    def dfs(r,c):
        if r < 0 or r >= rows or c < 0 or c >= cols:
            return
        grid[r][c] = '0'
        dfs(r+1,c)
        dfs(r-1,c)
        dfs(r,c+1)
        dfs(r,c-1)
    def bfs(r,c):
        queue = deque([(r,c)])
        grid[r][c] = '0'
        while queue :
            r,c = queue.popleft()
            for dr,dc in direction:
                nr,nc = r + dr, c + dc
                if 0 <= nr < rows and 0 <= nc < cols and grid[nr][nc] == '1':
                    grid[nr][nc] ='0'
                    queue.append((nr,nc))
    for r in range(rows):
        for c in range(cols):
            if grid[r][c] == '1':
                num_island += 1
                dfs(r,c)
                bfs(r,c)
    return num_island