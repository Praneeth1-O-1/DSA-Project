from datetime import datetime, timedelta


class Trash:
    class Node:
        def __init__(self, data):
            self.data = data
            self.next = None
            self.date = datetime.now()

    def __init__(self):
        self.head = None
        self.size = 0

    ''' the added file must be removed from the FileExplorer too '''

    def add_to_trash(self, node):
        #Simple adding a node to a linked list
        ins_node = self.Node(node)

        if not self.head:
            self.head = ins_node
        else:
            cur_node = self.head
            while cur_node.next:
                cur_node = cur_node.next
            cur_node.next = ins_node
        print(f"{node.name} added to trash.")

    def restore(self, file_name):
        #identifying the node
        cur_node = self.head
        while cur_node.data.name != file_name:
            cur_node = cur_node.next

        if not cur_node:
            print("\033[31m" + "File not found!")
            return

        #node added to the parent's child directories
        parent = cur_node.data.parent
        parent.child_directories.append(cur_node.data)

        #remove from trash
        if cur_node == self.head:
            self.head = self.head.next
        else:
            cur_node = self.head
            while cur_node.next.data.name != file_name:
                cur_node = cur_node.next
            cur_node.next = cur_node.next.next


    def permanent_delete(self, node_name):
        if self.head is None:
            print("The trash is empty")

    # Special case for the head node
        if self.head.data == node_name:
            temp = self.head
            self.head = self.head.next  # Move head to the next node
            del temp

    # General case for other nodes
        node = self.head
        while node.next is not None:
            if node.next.data == node_name:
                temp = node.next
                node.next = temp.next  # Bypass the node to delete it
                del temp
            node = node.next

    # If we reach here, the node was not found
        print(f"Node with name '{node_name}' not found.")

    def display(self):
        if not self.head:
            print("Trash empty!")
            return
        cur_node = self.head
        while cur_node:
            print(cur_node.data.name)
            cur_node = cur_node.next

    def garbage_collection(self, minutes_limit=2):
        current_time = datetime.now()
        threshold_time = timedelta(minutes=minutes_limit)

        items_to_del = []
        node = self.head
        while node:
            if (current_time - node.date) > threshold_time:
                items_to_del.append(node)
            node = node.next

        for items in items_to_del:
            self.permanent_delete(items)
            print(f"{node.data} has been in the trash for more than {minutes_limit} minutes and has been permanently deleted.")