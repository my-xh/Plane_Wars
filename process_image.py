
import os

CMD = 'magick convert'
SOURCE_PATH = r'images'


def doStrip(path):
    data = {}
    print('当前路径:', path)
    for root, dirs, files in os.walk(path):
        for file in files:
            name = file.lower()
            if name.find('.png') != -1:
                path = os.path.join(root, file)
                os.system('"{0}" {1} -strip {1}'.format(CMD, path, path))
                print(name, '处理成功')

doStrip(SOURCE_PATH)
