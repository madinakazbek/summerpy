class Solution(object):
    def subtractProductAndSum(self, n):
        """
        :type n: int
        :rtype: int
        """
        sum = 0
        product = 1
        for i in str(n):
            product *= int(i)
            sum += int(i)
        return product - sum