# -*- coding:utf-8 -*-
with open("./titles.txt", 'rb') as fk:
    for line in fk:
        line = line.decode("gbk")
        line = line.strip()
        if "[zls]" in line:
            line_arr = line.split("[zls]")
            newline = line_arr[1]
            newline_arr = newline.split("-")
            if len(newline_arr) == 4:
                temp = newline_arr[0]
                newtemp = temp[:-2]
                if len(newtemp.strip()) > 0:
                    print(newline + " ------>>>> " + temp + " ------>>>> " + newtemp)
                    with open("./newtitles.txt", 'a+') as fr:
                        fr.write(newtemp + "\n")
print("处理完成！！！")
