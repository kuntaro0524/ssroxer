

img_list=[1, 10, 100, 1000, 10000]

for img_num in img_list:
    tmpi = img_num - 1
    n = int(tmpi / 100) + 1
    j = tmpi%100
    
    print(img_num ,n, j)
