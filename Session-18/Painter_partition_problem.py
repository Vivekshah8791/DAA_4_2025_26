class Solution:
    
    def ispos(self, limit, arr, k):
        count = 1
        curr_sum = 0
        
        for i in range(len(arr)):
            
            if arr[i] > limit:
                return False
            
            if curr_sum + arr[i] <= limit:
                curr_sum += arr[i]
            else:
                count += 1
                curr_sum = arr[i]
                
        return count <= k
            

    def minTime(self, arr, k):
        
        left = max(arr)
        right = sum(arr)
        res = -1
        
        while left <= right:
            
            mid = left + (right - left) // 2
            
            if self.ispos(mid, arr, k):
                res = mid
                right = mid - 1
            else:
                left = mid + 1
                
        return res
