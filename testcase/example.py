import random
# data = [( "2290110100003",  "123456","first"),( "2290110100004",  "123456","second")]
# data=[['2290110100003', '123456', 'normal'], '("3390110100004",  "123456","aa")', '("2290110100004",  "123456","second")']
data=[['S3', '0001010202^', 2, '3D-单选单式--2号码相同'], ['S3', '000101020304^', 2, '3D-单选单式--号码个数为4']]
ids=[]
for x in data:
    print(x)
    print(type(x))
    ids.append(x[3])
print(data[0][3])
print(ids)


a=str(random.randrange(1, 9999))
print(a)

def get_ids(item):
    return item[1]

print(get_ids)