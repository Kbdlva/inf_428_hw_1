class Solution:
    def findLengthOfLCIS(self, nums: List[int]) -> int:
        count = 1
        max_value = 0

        if len(nums) == 1:
            return 1

        for i in range(1, len(nums)):
            if nums[i] > nums[i - 1]:
                count += 1
            else: 
                count = 1
            if count > max_value:
                max_value = count 

        return max_value

        # Check if the next number is creater than current
        # save max count value