def selection_sort(nums: list):
    for j in range(0, len(nums)):
        max_index: int = j
        for i in range(j + 1, len(nums)):
            if nums[i] > nums[max_index]:
                max_index = i
        if max_index != j:
            nums[j], nums[max_index] = nums[max_index], nums[j]
