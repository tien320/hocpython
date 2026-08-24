class Treenode:
    def __init__(self,val = 0,left = None, right = None):
        self.val = val
        self.left = left
        self.right = right
#DFS
def max_depth(root : Treenode):
    if root is None : return 0
    left_depth = max_depth(root.left)
    right_depth = max_depth(root.right)
    if left_depth > right_depth:
        return 1 + left_depth
    else:
        return 1 + right_depth
#BFS
def maxdepth(root: Treenode):
    if root is None : return 0
    current_level = [root]
    depth = 0
    while len(current_level) > 0:
        next_level = []
        for node in current_level:
            if node.left is not None:
                next_level.append(node.left)
            if node.right is not None:
                next_level.append(node.right)
        current_level = next_level
        depth +=1
    return depth   