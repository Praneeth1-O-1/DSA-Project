import subprocess as sp

class Files:
    class Node:
        def __init__(self, file_name):
            self.file_name = file_name
            self.next = None

    def __init__(self):
        self.head = None

    def nano(self, file_name: str):
        # Open the file with nano editor
        sp.run(["nano", file_name])

        # Add the new file to the linked list
        new_node = self.Node(file_name)
        if not self.head:
            self.head = new_node
        else:
            cur_node = self.head
            while cur_node.next:
                cur_node = cur_node.next
            cur_node.next = new_node

    def delete_file(self, file_name):
        cur_node = self.head
        while cur_node and cur_node.next.file_name != file_name:
            cur_node = cur_node.next
        trash_file = cur_node.next
        cur_node.next = cur_node.next.next