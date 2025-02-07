from typing import List, Any, Dict, Set, Generator


class StaticArray:
    def __init__(self, capacity: int):
        self.ar = [0] * capacity


    def set(self, index: int, value: int) -> None:
        self.ar[index] = value


    def get(self, index: int) -> int:
        return self.ar[index]


class DynamicArray:
    def __init__(self):
        self.ar = []


    def append(self, value: int) -> None:
        self.ar.append(value)


    def insert(self, index: int, value: int) -> None:
        self.ar.insert(index, value)


    def delete(self, index: int) -> None:
        del self.ar[index]


    def get(self, index: int) -> int:
        return self.ar[index]


class Node:
    def __init__(self, value: int):
        self.value = value
        self.next = None

class SinglyLinkedList:
    def __init__(self):
        self.head = self.tail = Node(0)
        self.sizeof = 0


    def append(self, value: int) -> None:
        self.tail.next = Node(value)
        self.tail = self.tail.next
        self.sizeof += 1


    def insert(self, position: int, value: int) -> None:
        current = self.head
        while position > 0:
            current = current.next
            position -= 1
        tmp = current.next
        current.next = Node(value)
        current.next.next = tmp
        self.sizeof += 1
        if not tmp:
            self.tail = current.next
        

    def delete(self, value: int) -> None:
        current = self.head.next
        prev = self.head
        while current:
            if current.value == value:
                prev.next = current.next
                self.sizeof -= 1
                if current.next == None:
                    self.tail = prev
                break
            prev = current
            current = current.next


    def find(self, value: int) -> Node:
        current = self.head.next
        while current:
            if current.value == value:
                return current
            current = current.next
        return None


    def size(self) -> int:
        return self.sizeof

    def is_empty(self) -> bool:
        return self.sizeof == 0


    def print_list(self) -> None:
        current = self.head.next
        while current:
            print(current.value, end=' ')
            current = current.next
        print()

    
    def reverse(self) -> None:
        prev = None
        self.tail = self.head.next
        if not self.tail:
            self.tail = self.head
        current = self.head.next
        while current:
            print(current.value)
            tmp = current.next
            current.next = prev
            prev = current
            current = tmp
        self.head.next = prev
        
    
    def get_head(self) -> Node:
        return self.head.next

    
    def get_tail(self) -> Node:
        return self.tail


class DoubleNode:
    def __init__(self, value: int, next_node = None, prev_node = None):
        self.value = value
        self.next_node = next_node
        self.prev_node = prev_node


class DoublyLinkedList:
    def __init__(self):
        self.head = DoubleNode(0)
        self.tail = DoubleNode(0)
        self.head.next_node = self.tail
        self.tail.prev_node = self.head
        self.sizeof = 0


    def append(self, value: int) -> None:
        self.tail.prev_node.next_node = DoubleNode(value, self.tail, self.tail.prev_node)
        self.tail.prev_node = self.tail.prev_node.next_node
        self.sizeof += 1


    def peek(self, position: int) -> int:
        if position > self.sizeof:
            return None
        current = self.head.next_node
        while position > 0:
            current = current.next_node
            position -= 1
        return current.value


    def insert(self, position: int, value: int) -> None:
        if position > self.sizeof:
            return
        current = self.head
        while position > 0:
            current = current.next_node
            position -= 1
        tmp = current.next_node
        current.next_node = DoubleNode(value, tmp, current)
        tmp.prev_node = current.next_node
        self.sizeof += 1
    
    
    def remove(self, position: int) -> int:
        if position > self.sizeof:
            return None
        current = self.head.next_node
        prev = self.head
        while position > 0:
            prev = current
            current = current.next_node
            position -= 1
        prev.next_node = current.next_node
        current.next_node.prev_node = prev
        self.sizeof -= 1
        return current.value


    def delete(self, value: int) -> None:
        current = self.head.next_node
        prev = self.head
        while current != self.tail:
            if current.value == value:
                prev.next_node = current.next_node
                current.next_node.prev_node = prev
                self.sizeof -= 1
                break
            prev = current
            current = current.next_node


    def find(self, value: int) -> DoubleNode:
        current = self.head.next_node
        while current != self.tail:
            if current.value == value:
                return current
            current = current.next_node
        return None


    def size(self) -> int:
        return self.sizeof
    

    def is_empty(self) -> bool:
        return self.sizeof == 0
    

    def print_list(self) -> None:
        current = self.head.next_node
        while current != self.tail:
            print(current.value, end=' ')
            current = current.next_node
        print()

    
    def reverse(self) -> None:
        current = self.head
        prev = None
        next = current.next_node
        while current != None:
            current.prev_node = next
            current.next_node = prev
            prev = current
            current = next
            if next:
                next = next.next_node
        self.head, self.tail = self.tail, self.head

    
    def get_head(self) -> DoubleNode:
        if self.is_empty():
            return None
        return self.head.next_node
    

    def get_tail(self) -> DoubleNode:
        if self.is_empty():
            return None
        return self.tail.prev_node


class Queue:
    def __init__(self):
        self.queue = DoublyLinkedList()
        

    def enqueue(self, value: int) -> None:
        self.queue.append(value)


    def dequeue(self) -> int:
        return self.queue.remove(0)
    

    def peek(self) -> int:
        return self.queue.peek(0)


    def is_empty(self) -> bool:
        return self.queue.is_empty()
    

class TreeNode:
    def __init__(self, value: int):
        self.value = value
        self.left = None
        self.right = None


class BinarySearchTree: #very poor O(n^2) performance bst :(
    def __init__(self):
        self.root = None
        self.sizeof = 0


    def insert(self, value: int) -> None:
        if self.root == None:
            self.root = TreeNode(value)
            self.sizeof += 1
            return
        parent = None
        current = self.root
        while current:
            if current.value == value:
                return
            parent = current
            if value < current.value:
                current = current.left
            else:
                current = current.right
        if value < parent.value:
            parent.left = TreeNode(value)
        else:
            parent.right = TreeNode(value)
        self.sizeof += 1


    def delete(self, value: int) -> None:
        if not self.root:
            return
        parent = None
        current = self.root
        while current and current.value != value:
            parent = current
            if value < current.value:
                current = current.left
            else:
                current = current.right
        if not current:
            return
        self.sizeof -= 1
        if not current.right:
            if not parent:
                self.root = current.left
                return
            if parent.left == current:
                parent.left = current.left
            else:
                parent.right = current.left
            return
        next = current.right
        if not next.left:
            if not parent:
                next.left = self.root.left
                self.root = next
                return
            if parent.left == current:
                parent.left = next
            else:
                parent.right = next
            next.left = current.left
            return
        prev = current
        while next.left:
            prev = next
            next = next.left
        current.value = next.value
        prev.left = None


    def search(self, value: int) -> TreeNode:
        current = self.root
        while current:
            if current.value == value:
                return current
            if value < current.value:
                current = current.left
            else:
                current = current.right
        return None


    def inorder_dfs(self, root : TreeNode) -> List[int]:
        if not root:
            return []
        return self.inorder_dfs(root.left) + [root.value] + self.inorder_dfs(root.right)
    

    def preorder_dfs(self, root : TreeNode) -> List[int]:
        if not root:
            return []
        return [root.value] + self.preorder_dfs(root.left) + self.preorder_dfs(root.right)


    def postorder_dfs(self, root : TreeNode) -> List[int]:
        if not root:
            return []
        return self.postorder_dfs(root.left) + self.postorder_dfs(root.right) + [root.value]


    def height_dfs(self, root : TreeNode) -> int:
        if not root:
            return 0
        return max(self.height_dfs(root.left), self.height_dfs(root.right)) + 1


    def inorder_traversal(self) -> List[int]:
        return self.inorder_dfs(self.root)

    
    def size(self) -> int:
        return self.sizeof


    def is_empty(self) -> bool:
        return self.sizeof == 0
    

    def height(self) -> int:
        return self.height_dfs(self.root)


    def preorder_traversal(self) -> List[int]:
        return self.preorder_dfs(self.root)
    

    def postorder_traversal(self) -> List[int]:
        return self.postorder_dfs(self.root)
    

    def level_order_traversal(self) -> List[int]:
        from collections import deque
        q = deque()
        q.append(self.root)
        order = []
        while len(q) > 0:
            current = q.popleft()
            if not current:
                continue
            order.append(current.value)
            q.append(current.left)
            q.append(current.right)
        return order


    def minimum(self) -> TreeNode:
        current = self.root
        while current.left:
            current = current.left
        return current


    def maximum(self) -> TreeNode:
        current = self.root
        while current.right:
            current = current.right
        return current
    
    
    def is_valid_bst(self) -> bool:
        order = self.inorder_traversal()
        return all(order[i] < order[i + 1] for i in range(len(order) - 1)) and len(order) == self.sizeof


def insertion_sort(lst: List[int]) -> List[int]:
    for i in range(1, len(lst)):
        id = i
        for j in range(i):
            if lst[j] > lst[i]:
                id = j
                break
        lst = lst[0:id] + [lst[i]] + lst[id:i] + lst[i+1:len(lst)]
    return lst


def selection_sort(lst: List[int]) -> List[int]:
    for i in range(len(lst) - 1):
        id = i
        for j in range(i + 1, len(lst)):
            if lst[j] < lst[id]:
                id = j
        lst[i], lst[id] = lst[id], lst[i]
    return lst


def bubble_sort(lst: List[int]) -> List[int]:
    for i in range(len(lst)):
        for j in range(len(lst) - i - 1):
            if lst[j + 1] < lst[j]:
                lst[j], lst[j + 1] = lst[j + 1], lst[j]
    return lst


def shell_sort(lst: List[int]) -> List[int]: #idk what it is
    return sorted(lst)


def merge_sort(lst: List[int]) -> List[int]:
    if len(lst) <= 1:
        return lst
    mid = len(lst) // 2
    left = merge_sort(lst[:mid])
    right = merge_sort(lst[mid:])
    result = []
    left_pointer = 0
    right_pointer = 0
    while left_pointer < len(left) or right_pointer < len(right):
        if left_pointer == len(left):
            result.append(right[right_pointer])
            right_pointer += 1
        elif right_pointer == len(right):
            result.append(left[left_pointer])
            left_pointer += 1
        elif left[left_pointer] < right[right_pointer]:
            result.append(left[left_pointer])
            left_pointer += 1
        else:
            result.append(right[right_pointer])
            right_pointer += 1
    return result


def quick_sort(lst: List[int]) -> List[int]:
    from random import randint
    if len(lst) <= 1:
        return lst
    mid = lst[randint(0, len(lst) - 1)]
    left = []
    right = []
    cnt = 0
    for i in lst:
        if i == mid:
            cnt += 1
        elif i < mid:
            left.append(i)
        else:
            right.append(i)
    return quick_sort(left) + [mid] * cnt + quick_sort(right)
    
