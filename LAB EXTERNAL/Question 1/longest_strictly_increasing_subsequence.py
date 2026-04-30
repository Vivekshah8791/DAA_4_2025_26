nums=[10,9,2,5,3,7,101,18]
ans=float("-inf")
for i in range(len(nums)):
    count=1
    lst_max=nums[i]
    for j in range(i+1,len(nums)):
        if nums[j]>nums[i] and nums[j]>lst_max:
            count+=1
            lst_max=nums[j]
        ans=max(ans,count)
print(ans)