import heapq

class Node:
    """
    A class to represent a node in a linked list.
    """
    def __init__(self, x, y):
        """
        Constructor for the Node class.
        :param x: x-coordinate of the node
        :param y: y-coordinate of the node
        """
        self.x = x
        self.y = y
        self.next = None


class LinkedList:
    """
    A class to represent a linked list data structure.
    """
    def __init__(self):
        """
        Constructor for the LinkedList class.
        """
        self.head = None
        self.size = 0
        self.tail = None

    def append(self, x, y):
        """
        Append a new node to the linked list.
        :param x: x coordinate of the node to append
        :param y: y coordinate of the node to append
        """
        new_node = Node(x, y)
        if not self.head:
            self.head = new_node
        else:
            current = self.head
            while current.next:
                current = current.next
            current.next = new_node
        self.tail = new_node
        self.size += 1

    def get_last_node(self):
        """
        Get the last node in the linked list.
        :return: the last node in the linked list
        """
        return self.tail


class Pair:
    """
    A class to represent a pair of state and actions.
    """
    def __init__(self, state, actions):
        """
        Constructor for the Pair class.
        :param state:
        :param actions:
        """
        self.state = state
        self.actions = actions

    def unpack(self):
        """
        Unpack the pair.
        :return: state, actions
        """
        return self.state, self.actions


class Stack:
    """
    Class to represent a stack data structure.
    """

    def __init__(self):
        """
        Constructor for the Stack class.
        """
        self.list = []

    def push(self, item):
        """
        Push the 'item' onto the stack
        :param item: the item to push
        """
        self.list.append(item)

    def pop(self):
        """
        Pop the most recently pushed item from the stack
        :return: the most recently pushed item
        """
        return self.list.pop()

    def is_empty(self):
        """
        Check if the stack is empty
        :return: True if the stack is empty, False otherwise
        """
        return len(self.list) == 0


class Queue:
    """
    Class to represent a queue data structure.
    """
    def __init__(self):
        """
        Constructor for the Queue class.
        """
        self.list = []

    def push(self, item):
        """
        Push the 'item' into the queue.
        :param item: the item to push
        """
        self.list.insert(0, item)

    def pop(self):
        """
        Pop the first item from the queue.
        :return: 
        """
        return self.list.pop()

    def is_empty(self):
        """
        Check if the queue is empty.
        :return: True if the queue is empty, False otherwise
        """
        return len(self.list) == 0


class PriorityQueue:
    """
    Class to represent a priority queue data structure.
    """

    def __init__(self):
        """
        Constructor for the PriorityQueue class.
        """
        self.heap = []
        self.init = False

    def push(self, item, priority):
        """
        Push the 'item' into the priority queue with the given 'priority'.
        :param item: item to push
        :param priority: priority of the item
        """
        if not self.init:
            self.init = True
            try:
                item < item
            except:
                item.__class__.__lt__ = lambda x, y: (True)
        pair = (priority, item)
        heapq.heappush(self.heap, pair)

    def pop(self):
        """
        Pop the item with the highest priority from the priority queue.
        :return: the item with the highest priority
        """
        (priority, item) = heapq.heappop(self.heap)
        return item

    def is_empty(self):
        """
        Check if the priority queue is empty.
        :return: True if the priority queue is empty, False otherwise
        """
        return len(self.heap) == 0


