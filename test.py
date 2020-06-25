list = [[1, 2424],[0, 342],[2, 34256],[3, 12]]
object = []
print(list)
list = sorted(list, key = lambda x : x[1])
list.reverse()
print(list)
