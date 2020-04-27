# -*- coding: utf-8 -*-
"""
Created on Mon Mar  9 22:43:32 2020

@author: mohammed Ibrahim Gaballah, Mahmoud Amr Nabil
"""
from heapq import * 

class fileHandler():
    def read(fName):
        f = open(fName, 'r')
        return f.read()
        f.close()
    def write(fName, word):
        x = open(fName, 'wb')
        x.write(word)
        x.close()
    def writeTxt(fName, word):
        x = open(fName, 'w')
        x.write(word)
        x.close()
class Tree():
    def __init__(self):
        self.root = None
        

class Node():
    def __init__(self, letter, probability, left= None, right = None):
        self.letter = letter
        self.probability = probability
        self.left = None
        self.right = None
    def __str__(self):
        return "letter:" + self.letter + " ,probability: " + str(self.probability)
    def __lt__(self, n):
        return self.probability < n.probability
        
class compressor():
    
    def __init__(self):
        self.orignalText = ''
        self.tree = Tree()
        self.root = None
        
    def compress(self, fIn, fOut):
        self.orignalText = fileHandler.read(fIn)                
        self.dicFreq  = {}        
        for i in range(len(self.orignalText)):
            letter = self.orignalText[i]
            if letter in self.dicFreq.keys():
                self.dicFreq[letter] += 1
            else:
                self.dicFreq[letter] = 1
        self.normalize()
#        generate the tree 
        self.heap = []
        
        for i in self.dicFreq:            
            heappush(self.heap, Node(i, self.dicFreq[i]))
            
        while(len(self.heap) > 1):
            h1 = heappop(self.heap)
            h2 = heappop(self.heap)
            parent:Node = Node('', h1.probability + h2.probability)
            heappush(self.heap,parent)
            if(h1 < h2):
                parent.left = h1
                parent.right = h2
            else:
                parent.left = h2
                parent.right = h1
            if(len(self.heap) == 1):
                break
            
            
#        now that we built the node of the heap
#           we have to interpret the code of each of the characters
#           we will do depth first traversal
#       
        self.dicCode = {} # dictionary of the codes of the characters

        self.depth(self.heap[0])
        self.codedText = self.orignalText
        for i in self.dicCode:
            self.codedText = self.codedText.replace(i, self.dicCode[i])
        
        self.codedText = self.paddText(self.codedText)
        fCode = self.turnToByteArray(self.codedText)        
        fileHandler.write(fOut, fCode)
        self.fCode = fCode #debug
    def paddText(self, codedText):
        # it is essential for the length of our code
        # to be multiple of 8 for easier decoding after wards
        padCount = 8 - len(codedText) % 8
        for i in range(padCount):
            codedText+="0"
        # added the number of padds to the beginnig of the codedText
        padStr = "{0:08b}".format(padCount)
        codedText = padStr + codedText
        return codedText
        
    def turnToByteArray(self, codedText):
        if len(codedText)%8 != 0:
            raise Exception("error coded text not correctly padded")
        b = bytearray()
        for i in range(0, len(codedText), 8):
			#code = codedText[i:i+8]
            code = codedText[i:i+8]
            b.append(int(code, 2))
        return b
        
    def decompress(self, fin, fout):
        f = open(fin, 'rb')
        bit_string = ""
        char = f.read(1)
        while(char != "" and len(char)!=0):
            try:
                char = ord(char)
                bits = bin(char)[2:].rjust(8, '0')
                bit_string += bits
                char = f.read(1)
            except Exception as identifier:
                print(identifier)
            
        # now that bits_string conatains the code,
        # algorithm
        # 1. read the 1st byte
        # 2. truncate a 1st byte number of bits from the tail of bits_string
        # 3. decode the rest of the bits        
        #given that:
        bit_string = self.dePadding(bit_string)
        end = len(bit_string)
        i = 0
        j = 0
        self.decodedString = '' # this will hold the decoded string
        while i < end:
            j=0
            while i + j < end:                
                j+=1
                charCode = bit_string[i: i + j]
                if ( charCode in self.dicCode.values()):
                    # decode get the realCharacter
                    realChar = ''
                    for m in self.dicCode:
                        if (charCode == self.dicCode[m]):
                            self.decodedString+= m
                    
                    i += j
                    break

        print(self.decodedString)
        fileHandler.writeTxt(fout, self.decodedString)
        
        return self.decodedString
    
    def dePadding(self, text):
        nOfPadds = int(text[0:8], 2)
        # truncate        
        text = text[8: len(text) - nOfPadds]
        return text
        

    def depth(self, root:Node, x=''):
        if root is None:
            return
        elif (root.left is None) and (root.right is None):
            self.dicCode[root.letter] = x
        else:
            self.depth(root.left, x + '0')
            self.depth(root.right, x + '1')
   
    def normalize(self):
        for i in self.dicFreq:
            self.dicFreq[i] /= len(self.orignalText)
        
        
comp = compressor()
comp.compress("test.txt", "test.bin")
comp.decompress("test.bin", "test-decomb.txt")

  
#        compression algorithms steps
#       1. load the file 
#       2. compute the probabilities
#       3. generate the tree
#       4. generate the code dictionary
#       5. replace each symbol with its code
#       6. make sure that the length of the resulted string is devisible by 8 if not padd it
# 7. take each 8 consecutive letters and convert to binary number
# 8. write the resulting binary array to a fileHandler

# vice versa in compresssion
# Note: we have read about huffman compression on the internet untill we have written our optimized  version of the code
