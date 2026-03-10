class Node:
    def __init__(self, data):
        self.data = data
        self.next = None


class LinkedList:
    def __init__(self):
        self.head = None
        self._size = 0

    def __len__(self):
        return self._size

    def __iter__(self):
        current = self.head
        while current:
            yield current.data
            current = current.next

    def append(self, data):
        new_node = Node(data)
        if self.head is None:
            self.head = new_node
        else:
            current = self.head
            while current.next:
                current = current.next
            current.next = new_node
        self._size += 1

    def delete(self, key, key_attr):
        current = self.head
        prev = None
        while current:
            if getattr(current.data, key_attr, None) == key:
                if prev:
                    prev.next = current.next
                else:
                    self.head = current.next
                self._size -= 1
                return True
            prev = current
            current = current.next
        return False

    def find(self, key, key_attr):
        for item in self:
            if getattr(item, key_attr, None) == key:
                return item
        return None

    def to_list(self):
        return list(self)

    def clear(self):
        self.head = None
        self._size = 0

# ---- TEMPORARY TEST - delete after testing ----
if __name__ == "__main__":

    class Dummy:
        def __init__(self, email):
            self.email_address = email

    ll = LinkedList()
    ll.append(Dummy("sam@sjsu.edu"))
    ll.append(Dummy("alex@sjsu.edu"))
    ll.append(Dummy("pam@sjsu.edu"))

    print("Size:", len(ll))
    for item in ll:
        print(" -", item.email_address)

    found = ll.find("alex@sjsu.edu", "email_address")
    print("Found:", found.email_address)

    ll.delete("alex@sjsu.edu", "email_address")
    print("After delete, size:", len(ll))