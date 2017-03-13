class Node:
    def __init__(self, weight):
        self.lchild = None
        self.rchild = None
        self.parent = None
        self.weight = weight

    def __lt__(self, other):
        return self.weight < other.weight

    def __str__(self):
        return self.weight.__str__()


class Leaf(Node):
    def __init__(self,value,weight):
        super(Leaf,self).__init__(weight)
        self.value = value


class NodeQueue:
    def __init__(self, nodes):
        self.nodes = nodes
        self.nodes.sort(reverse=True)

    def __str__(self):
        return self.nodes.__str__()

    def enqueue(self, n):
        if self.nodes is None:
            self.nodes = []
        flag = False
        for i in range(len(self.nodes)):
            if self.nodes[i] < n:
                self.nodes.insert(i,n)
                flag = True
                break
        if flag is False:
            self.nodes.append(n)

    def dequeue(self):
        l = len(self.nodes)
        if l >= 2:
            return Node(self.nodes.pop().weight + self.nodes.pop().weight)
        elif l == 1:
            return self.nodes.pop()
        else:
            return None

    def getNode(self):
        n = self.dequeue()
        if n is not None and len(self.nodes) >= 1:
            self.enqueue(n)
        return n


class Huffman:
    def __init__(self, leaf_dict):
        self.nq = NodeQueue([leaf_dict[key] for key in leaf_dict])
        self.leafs = self.nq.nodes
        self.root = None
        while(len(self.nq.nodes) > 1):
            l = self.nq.nodes[-2]
            r = self.nq.nodes[-1]
            p = self.nq.getNode()
            r.parent = l.parent = p
            p.lchild = l
            p.rchild = r
            if len(self.nq.nodes) == 0:
                self.root = p


if __name__ == '__main__':
    nq = NodeQueue([Node(1),Node(2),Node(3),Node(7)])
    while len(nq.nodes) > 0:
        print(nq.getNode())
