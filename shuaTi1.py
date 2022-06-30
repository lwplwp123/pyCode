# 针对给定单词列表，做字符串索引和索引列表
# 要求通过字符串索引和索引列表来回复原有字符串列表，可用索引字符串在索引列表中的index开始找到“#” 结束，来回复原有字符串列表
# 例如 随机给 ["time","me","tell"] 单词组，做出的索引字符串为s="time#tell#" 索引列表为indexes=[0,2,5]

word = ["time","me","tell","me","ll","e","aa",'tell','goodtime']

word2=word.copy()
word2.sort( key= lambda a:len(a) ,reverse= True)


print(word2)
s=""
indexes=[]
for x in word2:
    if s.find(x)>=0:
        indexes.append(s.index(x))
    else:
        indexes.append(len(s))
        s+= x+"#"

print(s)
print('use new list.')
print(word2)
print(indexes)
indexes.clear()

for x in word:
    indexes.append(s.index(x))
print('use original list.')
print(word)
print(indexes)



# word = ["time","me","tell","me","ll","e","aa",'tell','goodtime']
# s=''
# list_s = []
# indexes = []
# for i in word:
#     if len(list_s)==0:
#         list_s.append(i)
#         indexes.append(0)
#     else:
#         is_ok = 0
#         for j in list_s:
#             if j[-len(i):] == i:
#                 is_ok = 0
#                 temp_index = j.index(i) + list_s.index(j) + sum([len(list_s[ii]) for ii in range(list_s.index(j))])
#                 break
#             else:
#                 is_ok = 1
#         if is_ok == 1:            
#             temp_index = sum([len(i) for i in list_s]) + len(list_s)
#             list_s.append(i)
#         indexes.append(temp_index)

# for i in list_s:
#     s = s + i + "#"
# print(s,indexes)
# print(len(s))

