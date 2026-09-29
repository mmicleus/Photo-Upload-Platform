



def secret(nums):

    result = []

    nums.sort()

    for i,num in enumerate(nums):

        x = 0
        y = len(nums)-1

        while x < y:

            if x == i:
                x += 1
                continue
            if y == i:
                y -= 1
                continue

            if nums[x] + nums[y] + num == 0:
                result.append((nums[x], nums[y], num))
                x += 1
                y -= 1
            elif nums[x] + nums[y] + num < 0:
                x += 1
            elif nums[x] + nums[y] + num > 0:
                y -= 1


    return result


print(secret([-1,0,1,2,-1,-4]))
            
            
       
