import os


def getFileList(path):
    """输入文件夹路径,返回一个列表，包含文件夹下所有文件"""
    #fileList = []
    for root, dirs, files in os.walk(path):
        for file in files:
            #fileList.append(os.path.join(root, file))
            yield os.path.join(root, file)
    # return fileList


def hasChinese(check_str):
    for ch in check_str:
        if u'\u4e00' <= ch <= u'\u9fff':
            return True
    return False


def getNewName(fname: str):
    dotIndex = fname.find('.')
    if hasChinese(fname[:dotIndex]):
        return '['+fname[:dotIndex]+']'+fname[dotIndex:]
    else:
        return fname


def rename(path: str):
    """ 把文件夹path下文件由中文名.英文名重命名为[中文名].英文名, 方便emby削刮 """
    # fileList =
    for file in getFileList(path):
        fpath, fname = os.path.split(file)
        fname = getNewName(fname)
        newName = os.path.join(fpath, fname)
        try:
            os.rename(file, newName)
            print(newName)
        except:
            print('error')


if __name__ == '__main__':
    # fname = 'A计划.Project.A.1983.BluRay.1080p.x265.10bit.2Audio.MNHD-FRDS.mkv'
    # print(getNewName(fname))
    path = '/onedrive/mov/mov/电影/合集/成龙'
    rename(path)
