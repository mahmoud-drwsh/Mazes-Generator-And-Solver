def mergeSort(nums: list):
    # return if the list size is < 2
    if len(nums) == 1:
        return

    # calc the middle index
    len_nums = len(nums) // 2

    # split the list in 2
    left = nums[:len_nums]  # left half
    # split the list in 2
    right = nums[len_nums:]  # right half

    # perform merge_sort on left half
    mergeSort(left)
    # perform merge_sort on right half
    mergeSort(right)

    # start merging the left and right halves
    i, j, k = 0, 0, 0

    # keep merging until one of the halves has been completely merged
    while i < len(left) and j < len(right):
        if left[i] < right[j]:
            nums[k] = left[i]
            i += 1
        else:
            nums[k] = right[j]
            j += 1
        k += 1

    # merge the remaining of the left half
    while i < len(left):
        nums[k] = left[i]
        i += 1
        k += 1

    # merge the remaining of the right half
    while j < len(right):
        nums[k] = left[j]
        j += 1
        k += 1
