#!/usr/bin/env python
'''
    @author: zekun zhang
    @date:   13th.Nov.2018s
    To deal with big files
'''

import os
import time
import uuid
import hashlib

'''
This function is to create a file that has a specified numbers uuids.
This is for test
'''
def create_file_size(file_name,num_events):
    with open(file_name, 'w') as f:
        note = 'Test File Contents: '
        pre = uuid.uuid4().hex
        for i in range(num_events):
 
            if i%2==0:
                f.write(pre+"\n")
            else:
                pre = uuid.uuid4().hex
                f.write(pre+"\n")
    print("done create")
'''
Get union of events of f1 and f2
For instance:
f1: a\n,a\n,b\n,b\n,c\n
f2: b\n,d\n,d\n,e\n
outfile will be: a\n,b\n,c\n,d\n,e\n
'''
def get_distinct(f1,f2,outfile):
    
    amap = {}
    out = open(outfile,'w')
    print("Processing...")
    start = time.time()
    c1 = 0
    r = 0
    with open(f1,'r') as f:
        for line in f:
            c1 += 1
        
            eline = line.encode()
            h = int(hashlib.md5(eline).hexdigest(),16)%100000
            if h in amap:
                if line not in amap[h]:
                    
                    amap[h].append(line)
                    out.write(line)
                    r += 1
                    
            else:
                amap[h] = [line]
                r += 1
                out.write(line)
    print('file1 line number:',c1)
    print("done first step")
    c2 = 0
    with open(f2,'r') as f:
        for line in f:
            c2 += 1
            eline = line.encode()
            h = int(hashlib.md5(eline).hexdigest(),16)%100000
            if h in amap:
                if line not in amap[h]:
                    out.write(line)
                    r += 1
                    amap[h].append(line)
            else:
                amap[h]=[line]
                r += 1
                out.write(line)
    out.close()
    end = time.time()
    print("process time:",end-start)
    print('file2 line number:', c2)
    print('result line number:',r)
    print("done")
'''
remove duplicate events from f1
The output will be f1+time_stamp+"_distinct.txt"
'''
def remove_dups(f1):
    amap = {}
    tmp = f1+str(time.time())[:10]+'_distinct.txt'
    out = open(tmp,"w")
    print("Removing duplicates from file...")
 
    with open(f1,'r') as f:
        for line in f:
 
        
            eline = line.encode()
            h = int(hashlib.md5(eline).hexdigest(),16)%100000
            if h in amap:
                if line not in amap[h]:
                    amap[h].append(line)
                    out.write(line)
 
                    
            else:
                amap[h] = [line]
                out.write(line)
     
    out.close()
    return tmp
    
'''
f1_out: f1 - (f1 intersection f2)
outfile: f1 intersection f2
'''
def remove_cor_from_file(f1,f2,f1_outfile,outfile):
    amap = {}
    out = open(outfile,'w')
    f1_out = open(f1_outfile,'w')
    print("Processing...")
    start = time.time()
    c1 = 0
    r = 0
    with open(f2,'r') as f:
        for line in f:
            c1 += 1
        
            eline = line.encode()
            h = int(hashlib.md5(eline).hexdigest(),16)%100000
            if h in amap:
                if line not in amap[h]:                   
                    amap[h].append(line)
                   
            else:
                amap[h] = [line]
    c2 = 0
    d_count = 0
    bmap ={}
    tmp = remove_dups(f1)
    with open(tmp,'r') as f:
        for line in f:
            c2 += 1
            eline = line.encode()
            h = int(hashlib.md5(eline).hexdigest(),16)%100000
            if h in amap:
                if line not in amap[h]:
                    f1_out.write(line)
                    r += 1
                else:
                
                    out.write(line)
                    d_count += 1
                    
            else:
                r += 1
                f1_out.write(line)            
            

    out.close()
    f1_out.close()

    end = time.time()
    print("done")
    print("process time:",end-start)
    print('file1 line number:', c2)
    print('file2 line number:', c1)
    print('file1 deduplict line number:',r)
    print('Duplicate line number:',d_count)
    
if __name__ == '__main__':
    cmd = input('Please input a command: ')
    if cmd == 'single_file_redupliction':
        remove_dups(input("File name: "))
    elif cmd == "remove_correlate":
        f = input('Please input f1,f2 and output file names, separeted by comma:\n')
        f1,f2,outfile = f.split(",")
        remove_cor_from_file(f1,f2,f1+str(time.time())+'output.txt',outfile)
    elif cmd == 'union_two_files':
        f = input('Please input f1,f2 and output file names, separeted by comma:\n')
        f1,f2,outfile = f.split(",")
        get_distinct(f1,f2,outfile)

    else:
        print('Please enter a correct command: single_file_redupliction,remove_correlate,union_two_files')
