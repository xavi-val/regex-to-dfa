from operator import index
from tree import SyntaxTree
from convert_to_dfa import ConvertToDfa
from graphTree import graph


file=open('input.txt','r')

inputs=file.read()
inputs=inputs.split('\n')
print(inputs)
index = 0

for input in inputs:
    regex=input
    tree=SyntaxTree(regex)
    tree.findfollowpos(tree.root)    
    index+=1
    graph(tree,regex,"tree"+str(index)+".gv")

    converttree=ConvertToDfa(tree=tree)
    dfa=converttree.convert()
    outputfile=open('output.txt','a')
    converttree.write_in_file(outputfile)
    
