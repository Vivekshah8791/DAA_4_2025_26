# Definition for singly-linked list.
# class ListNode:
#     def __init__(self, val=0, next=None):
#         self.val = val
#         self.next = next
class Solution:
    def reverseKGroup(self, head: Optional[ListNode], k: int) -> Optional[ListNode]:
        dummy=ListNode(0)
        curr=dummy
        arr=[]
        temp=head
        while temp:
            arr.append(temp.val)
            temp=temp.next
        left=0
        right=k-1
        while left<len(arr) and right<len(arr):
            newleft=left
            newright=right
            while newleft<=newright:
                arr[newleft],arr[newright]=arr[newright],arr[newleft]
                newleft+=1
                newright-=1
            left+=k
            right+=k
        for i in range(len(arr)):
            curr.next=ListNode(arr[i])
            curr=curr.next
        return dummy.next