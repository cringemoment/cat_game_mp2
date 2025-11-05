def flatten(l):
    out = []
    for i in l:
        for j in i:
            out.append(j)

    return out

def insert_operations(number, count):
    length = len(number)
    operations_left = count
    start = 1
    expressions = [number]
    # expressions = ['1+23456789', '12+3456789', '123+456789', '1234+56789', '12345+6789', '123456+789', '1234567+89', '12345678+9']
    while operations_left > 0:
        out = []
        for parindex, parnum in enumerate(expressions):
            for i in range(start, len(parnum)):
                if parnum[i] in ["+", "-"] or (i + 1 < len(parnum) and parnum[i + 1] in ["+", "-"]) or parnum[i - 1] in ["+", "-"]:
                    continue

                # print(parnum[i])
                # print(parnum[i - 1:i + 2])
                # print(parnum[i + 1])

                a = parnum[:i] + "+" + parnum[i:]
                out.append(a)
                b = parnum[:i] + "-" + parnum[i:]
                out.append(b)

            expressions[parindex] = out

        operations_left -= 1
        start += 1
        expressions = flatten(expressions)

    return set(expressions) #the expression generation overcounts a lot so set removes overcounts

def solve(number, check):
    solutions = []
    for operation_count in range(len(number)):
        print(operation_count)
        for expression in insert_operations(number, operation_count):
            if eval(expression) == check:
                solutions.append(expression)

    return solutions

print(solve("123456789", 100))
