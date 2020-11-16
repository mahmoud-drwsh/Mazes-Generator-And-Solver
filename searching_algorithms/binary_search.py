def binary_search(nums, e, l, r):
    if l > r:
        return -1

    mid = l + ((r - l) // 2)

    if nums[mid] == e:
        return mid
    elif nums[mid] > e:
        return binary_search(nums, e, mid + 1, r)
    else:
        return binary_search(nums, e, l, mid - 1)
