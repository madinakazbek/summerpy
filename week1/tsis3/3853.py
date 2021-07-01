def lol(lst,k):
    k=k%len(lst)
    k=-k
    ret=[0]*len(lst)
    for i in range(len(lst)):
        if i+k<len(lst) and i+k>=0:
            ret[i]=lst[i+k]
        if i+k>=len(lst):
            ret[i]=lst[i+k-len(lst)]
        if i+k<0:
            ret[i]=lst[i+k+len(lst)]
 
    return(ret)