class Solution:
    def reverseKGroup(self, head: Optional[ListNode], k: int):

        curr = head
        prevEnd = None
        newHead = head

        while curr:

            count = 0
            temp = curr

            while temp and count < k:
                temp = temp.next
                count += 1

            if count < k:
                if prevEnd:
                    prevEnd.next = curr
                break

            start = curr
            prev = None

            for _ in range(k):
                nextNode = curr.next
                curr.next = prev
                prev = curr
                curr = nextNode

            if prevEnd is None:
                newHead = prev
            else:
                prevEnd.next = prev

            start.next = curr
            prevEnd = start

        return newHead