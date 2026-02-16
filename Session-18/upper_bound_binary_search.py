l=list(map(int,input().split()))
target=1
left=0
right=len(l)-1
ub=len(l)
while left<=right:
    mid=left+(right-left)//2
    if l[mid]>target:
        ub=mid
        right=mid-1
    else:
        left=mid+1
print(ub)