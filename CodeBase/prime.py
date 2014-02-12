import math
def  getNumberOfPrimes( n):
    if n <= 2:
	    return 0
    elif n == 3:
		return 1
    else:
        prime_list=[2]
        for i in range(3,n,2):
            is_Prime = True
            for j in prime_list:
                if (j > math.sqrt(i)):
                    break
                if (i%j == 0):
                    is_Prime = False
                    break
            if is_Prime is True:
                prime_list.append(i)                
        return len(prime_list)