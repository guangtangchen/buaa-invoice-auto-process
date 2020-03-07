import fitz
from get_all_files_relative_filepath import get_relative_filepath
import shutil


def pdf_to_jpg(target_path, save_path):
    #  打开PDF文件，生成一个对象
    doc = fitz.open(target_path)
    for pg in range(doc.pageCount):
        page = doc[pg]
        rotate = int(0)
        # 每个尺寸的缩放系数为2，这将为我们生成分辨率提高四倍的图像。
        zoom_x = 2.0
        zoom_y = 2.0
        trans = fitz.Matrix(zoom_x, zoom_y).preRotate(rotate)
        pm = page.getPixmap(matrix=trans, alpha=False)
        pm.writePNG(save_path)


def main_pdf_to_png(target_path=r'发票\PDF'):
    count = 0
    abs_path = get_relative_filepath(target_path)[0]
    for item in abs_path:
        if item.split('.')[-1] == 'pdf':
            count += 1
            save_path = f'发票/图片版/{count}.png'
            pdf_to_jpg(item, save_path)
            shutil.move(item, r'发票\PDF' + '\\' + str(count) + '.pdf')   # 保证pdf和png名称对应



