import itertools

a_list = [1, 2, 3]
# perm = list()
# for i in range(1, len(a_list) + 1):
#     perm.extend([list(x) for x in itertools.permutations(a_list, i)])
# print(perm)

perm = [list(x) for i in range(1, len(a_list)+1) for x in itertools.permutations(a_list, i)]
print(perm)
