class Solution:
    def ispos(self,piles,mid,h):
        count=0
        for i in range(len(piles)):
            count += (piles[i] + mid - 1) // mid
        return count<=h
    def minEatingSpeed(self, piles: List[int], h: int) -> int:
        left=1
        right=max(piles)
        ans=0
        while left<=right:
            mid=left+(right-left)//2
            if self.ispos(piles,mid,h):
                ans=mid
                right=mid-1
            else:
                left=mid+1
        return ans
            