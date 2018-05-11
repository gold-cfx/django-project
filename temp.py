a = [1,2, 5, 8, 6, 3 ]
for i in range(len(a)):
    b = min(a)
    a.remove(b)



childs = '全部分类:0#酸奶乳酸菌:103537#牛奶豆浆:103538#面包蛋糕:103540'.split('#')
child = []
for i in childs:
    child.append(i.split(':'))
print(child)

# url(r'^static/(?P<path>.*)$', serve, {""})
# url(r'^static/(?P<path>.*)$', serve, {""})
