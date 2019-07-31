def solution(A, B):
    # write your code in Python 3.6
    c = A*B
    bin_c = str(bin(c))
    print(bin_c)
    counter = 0
    for x in range(len(bin_c)):
        print(bin_c[x])
        if (bin_c[x] == '1'):
            print('woo')
            counter += 1
    print(counter)

print(solution(7,3))
print(solution(1,3))
print(solution(1,3))
