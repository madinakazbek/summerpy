class Solution(object):
    def largestAltitude(self, gain):
        """
        :type gain: List[int]
        :rtype: int
        """
        start = max = 0
        for i in gain:
            start += i
            if max < start:
                max = start
                
        return max