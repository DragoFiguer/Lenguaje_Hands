def convertToPositive(num):
    if (num < 0):
        return (num * -1)
    return num


a=str("-1")
c = convertToPositive(int(a))
print(c)
