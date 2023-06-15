import re
arr=[]
pattern=r"/solution"
with open("./lc.txt") as f:
    for line in f:
        if(re.search(pattern,line)):
            pass
        else:
            arr.append(line)
arr=list(set(arr))
with open("lc_problems.txt",'a') as f:
    for link in arr:
        f.write(link)
        print(link)