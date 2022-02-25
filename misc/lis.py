# Longest increasing subsequence


def lis(a):
    n = len(a)
    maxpath = [{'path': [i], 'length': 0} for i in range(n)]

    changed = True
    while changed:
        changed = False
        for i in range(n):
            for j in range(i):
                if a[j] < a[i]:
                    if maxpath[j]['length'] + 1 > maxpath[i]['length']:
                        maxpath[i]['length'] = maxpath[j]['length'] + 1
                        maxpath[i]['path'] = maxpath[j]['path'] + [i]
                        changed = True

    best = sorted(maxpath, key=lambda x: x['length'])[-1]

    return ([a[i] for i in best['path']], best['length']+1)
    # return (best['path'], best['length']+1)


# Does not work
def lis2(a):
    if len(a) == 1:
        return 1

    maxlis = 0
    for i, x in enumerate(a):
        lis_i = lis2(a[:i+1])
        if x < a[-1]:
            lis_i += 1

        if maxlis < lis_i:
            maxlis = lis_i

    return maxlis


a = [3, 1, 8, 2, 5]
b = [5, 2, 8, 6, 3, 6, 9, 5]
print(lis(a))
print(lis(b))
