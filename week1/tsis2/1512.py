class Solution(object):
    def numIdenticalPairs(self, nums):
        """
        :type nums: List[int]
        :rtype: int
        """
        cnt = 0
        for i in nums:
            cnt += nums.count(i) - 1
            nums.remove(i)
        return cnt