sample = [1, 2, 3, 4, -100, 6]
max_sum = 0
temp_sum = 0
for element in sample:
    temp_sum += element
    if element > 0:
        max_sum = max(max_sum, temp_sum)
    elif element <= 0 and temp_sum <= 0:
        temp_sum = 0
        
print max_sum
    