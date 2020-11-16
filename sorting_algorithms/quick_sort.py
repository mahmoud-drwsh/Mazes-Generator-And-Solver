import random


def quick_sort(nums, r, l=0):
    # proceed only if we have a list of at least an element
    if not l > r:

        # set the pivot index initially to "l"
        pivot = l

        # copy all of the elements that are less than the last element to the left
        for i in range(l, r + 1):
            # at the end swap the last element with "pivot"
            if nums[i] < nums[r] or i == r:
                nums[i], nums[pivot] = nums[pivot], nums[i]
                pivot += 1

        # quick sort the left half
        # the reason for subtracting 2 is that "pivot" after performing the above operations
        # would be at +1 the actual index!
        quick_sort(nums, l=l, r=pivot - 2)
        # quick sort the right half
        quick_sort(nums, l=pivot, r=r)


def quick_sort_2(nums):
    if len(nums) <= 1:
        return nums
    pivot = nums[-1]
    left = [x for x in nums if x < pivot]
    right = [x for x in nums if x > pivot]
    return quick_sort_2(left) + [pivot] + quick_sort_2(right)
