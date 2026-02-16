class Solution:
    def ispos(self,stalls,maximum,k):
        stalls.sort()
        count=1
        pos=stalls[0]
        for i in range(len(stalls)):
            if stalls[i]-pos>=maximum:
                count+=1
                pos=stalls[i]
            if count==k:
                return True
        return False
        
    def aggressiveCows(self, stalls, k):
        left=1
        right=max(stalls)-min(stalls)
        ans=-1
        while left<=right:
            mid=left+(right-left)//2
            if self.ispos(stalls,mid,k):
                ans=mid
                left=mid+1
            else:
                right=mid-1
        return ans
        