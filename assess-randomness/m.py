from random import randint
import math


N = 10
def assess_randomness(sequence, digits):
    print(sequence[:10])
    count = len(sequence) 
    if count == 0:
        return 0
    digit = 1
    result = []

    while (1):
        k = 0
        hist = dict()
        hist.update({sequence[0]//digit: 1})
        dif = sequence[1]//digit - sequence[0]//digit
        for i in range(1, count):
            if sequence[i]//digit not in hist.keys():
                hist.update({sequence[i]//digit: 1})
            else:
                hist[sequence[i]//digit] += 1
            if i != 1 and sequence[i]//digit - sequence[i-1]//digit == dif:
                k -= 1/count
            else:
                dif = sequence[i]//digit - sequence[i-1]//digit

        print(hist)
        print("before entropy k = ", k)

        for el in hist.keys():
            p = hist[el] / count
            k -= p * math.log(p, count)
        print("after entropy k = ", k)

        result.append(k)
        print(result)

        if digit == digits:
            break
        else:
            digit = digit * 10

    return sum(result)/len(result)


one_digit = [randint(0, 9) for i in range(N)]
two_digits = [randint(10, 99) for i in range(N)]
three_digits = [randint(100, 999) for i in range(N)]

b1 =  [1,9,1,9,1,9,1,9,1,9]
b11 = [11,93,14,95,19,95,15,94,17,99]
b111 = [113,933,143,953,193,953,153,943,173,993]


b2 = [1,1,1,1,1,1,1,1,1,1]
b3 = [i for i in range(10, 0, -1)]
b4 = [i for i in range(1, 11)]

g1 = [1,9,2,8,3,7,4,6,5,0]
g2 = [1,9,5,8,3,1,4,6,5,0]


# print(assess_randomness(one_digit), "\n")
print(assess_randomness(b1, 1), "\n")
print(assess_randomness(b11, 10), "\n")
print(assess_randomness(b111, 100), "\n")


# print(assess_randomness(b2), "\n")
# print(assess_randomness(b3), "\n")
# print(assess_randomness(b4), "\n")
# print(assess_randomness(g1), "\n")
# print(assess_randomness(g2), "\n")




