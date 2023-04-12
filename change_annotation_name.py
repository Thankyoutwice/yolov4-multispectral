import os
import os.path
from xml.etree.ElementTree import parse, Element
#批量修改xml中filename
def test():
    path = "kaist_wash/kaist_wash_annotation_test" # xml文件所在的目录
    files = os.listdir(path)  # 遍历文件夹下所有文件名称
    n=1
    for xmlFile in files:  # 对所有文件进行循环遍历处理
        path1 = "kaist_wash/kaist_wash_annotation_test"+xmlFile #定位当前处理的文件的路径
        newStr = os.path.join(path, xmlFile)
 
        dom = parse(newStr)  # 获取xml文件中的参数
        root = dom.getroot()  # 获取数据结构
 
        for obj in root.iter('annotation'): # 获取object节点中的name子节点（此处如果要换成别的比如bndbox）
            name = obj.find('filename').text # 获取相应的文本信息
            #  以下为自定义的修改规则，把文本信息为的内容改成000001，依次类推
            used_name = name
            print(used_name)
            new_name = str(n).zfill(6)+'.jpg'#标签名长度对齐为6位，通过在前面补0
            new_filename = str(n).zfill(6)+'.xml'#文件名长度对齐为6位，通过在前面补0
            # os.rename(os.path.join(path,used_name),os.path.join(path,new_name))
            n = n + 1
            print("新文件名：")
            print(new_filename)  #是一个字符串集合
            print("\n")
    
            obj.find('filename').text = new_name # 修改标签filename
        dom.write(new_filename, xml_declaration=True) # 保存到指定文件
        pass
if __name__ == '__main__':
    test()