#效果：把旧的名字清理掉，统一换成000000，递增加1
import os
import os.path
# 将可见光图片和热红外图片修改为新名称
path = "kaist_wash/kaist_wash_picture_test/visible"#可见光
#path = "kaist_wash/kaist_wash_picture_test/lwir"#热红外
filename_list=os.listdir(path)
n = 1
for filename in filename_list:
    used_name=filename
    print(used_name)    
    new_name=str(n).zfill(6)+'.jpg'#文件名长度对齐为6位，通过在前面补0
 
    os.rename(os.path.join(path,used_name),os.path.join(path,new_name))
 
    n+=1
    print("新文件名：")
    print(new_name)  #是一个字符串集合
    print("\n")
'''
zfill函数功能：
    为字符串定义长度，如不满足，缺少的部分y右侧会用0填补
 
zfill函数用法：
    newstr = string.zfill(width)
    参数：
    width新字符串希望的宽度
zfill函数注意事项：
    与字符串的字符无关
    如果定义长度小于当前字符串长度，则不发生变化
'''
#后面可以调用 script_for_file_rename_prefix.py脚本，加英文前缀，比如：chapter1