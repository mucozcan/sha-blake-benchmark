from typing import List
import typing
import hashlib

class BaseNode:
    def __init__(self, left, right, value: str, content) -> None:
        self.left: BaseNode = left
        self.right: BaseNode = right
        self.value = value
        self.content = content

    def __str__(self):
        return str(self.value)


class BlakeNode(BaseNode):
    def __init__(self, left, right, value, content):
        BaseNode.__init__(self, left, right, value, content)

    @staticmethod
    def hash(val: str) -> str:
        return hashlib.blake2b(val.encode('utf-8')).hexdigest() # 64B digest_size


class SHANode(BaseNode):
    def __init__(self, left, right, value, content):
        BaseNode.__init__(self, left, right, value, content)

    @staticmethod
    def hash(val: str) -> str:
        return hashlib.sha256(val.encode('utf-8')).hexdigest() # 32B digest_size


class BaseMerkleTree:

    def print_tree(self) -> None:
        self.__print_tree_rec(self.root)
 
    def __print_tree_rec(self, node: BaseNode)-> None:
        if node != None:
            if node.left != None:
                print("Left: "+str(node.left))
                print("Right: "+str(node.right))
            else:
                print("Input")
            print("Value: "+str(node.value))
            print("Content: "+str(node.content))
            print("")
            self.__printTreeRec(node.left)
            self.__printTreeRec(node.right)
    
    def get_root_hash(self)-> str:
        return self.root.value


class BlakeMerkleTree(BaseMerkleTree):
    def __init__(self, values: List[str])-> None: # FIXME depends on length of leaves 
        self.__build_tree(values)
 
    def __build_tree(self, values: List[str])-> None:
 
        leaves: List[BlakeNode] = [BlakeNode(None, None, BlakeNode.hash(e),e) for e in values]
        if len(leaves) % 2 == 1:
            leaves.append(leaves[-1:][0]) # duplicate last elem if odd number of elements
        self.root: BlakeNode = self.__build_tree_rec(leaves) 
    
    def __build_tree_rec(self, nodes: List[BlakeNode])-> BlakeNode:
        half: int = len(nodes) // 2
 
        if len(nodes) == 2:
            return BlakeNode(nodes[0], nodes[1], BlakeNode.hash(nodes[0].value + nodes[1].value), nodes[0].content+"+"+nodes[1].content)
        
        left: BlakeNode = self.__build_tree_rec(nodes[:half])
        right: BlakeNode = self.__build_tree_rec(nodes[half:])
        value: str = BlakeNode.hash(left.value + right.value)
        content: str = self.__build_tree_rec(nodes[:half]).content+"+"+self.__build_tree_rec(nodes[half:]).content
        return BlakeNode(left, right, value,content)

class SHAMerkleTree(BaseMerkleTree):
    def __init__(self, values: List[str])-> None:
        self.__build_tree(values)
 
    def __build_tree(self, values: List[str])-> None: # FIXME depends on length of leaves 
 
        leaves: List[SHANode] = [SHANode(None, None, SHANode.hash(e),e) for e in values]
        if len(leaves) % 2 == 1:
            leaves.append(leaves[-1:][0]) # duplicate last elem if odd number of elements
        self.root: SHANode = self.__build_tree_rec(leaves) 
    
    def __build_tree_rec(self, nodes: List[SHANode])-> SHANode:
        half: int = len(nodes) // 2
        if len(nodes) % 2 == 1:
            nodes.append(nodes[-1:][0]) # duplicate last elem if odd number of elements
        if len(nodes) == 2:
            return SHANode(nodes[0], nodes[1], SHANode.hash(nodes[0].value + nodes[1].value), nodes[0].content+"+"+nodes[1].content)
        
        left: SHANode = self.__build_tree_rec(nodes[:half])
        right: SHANode = self.__build_tree_rec(nodes[half:])
        value: str = SHANode.hash(left.value + right.value)
        content: str = self.__build_tree_rec(nodes[:half]).content+"+"+self.__build_tree_rec(nodes[half:]).content
        return SHANode(left, right, value,content)


if __name__ == "__main__":
    values = ["Merkle", "Tree", "Test", "SHA", "BLAKE2b", "Data", "Security", "Benchmark"]

    sha_tree = SHAMerkleTree(values)
    blake_tree = BlakeMerkleTree(values)

    print(f"SHA-256 Root Hash: {sha_tree.get_root_hash()}")
    print(f"Blake Root Hash: {blake_tree.get_root_hash()}")
