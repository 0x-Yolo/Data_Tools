import os

import PIL.Image as Image




def resize_by_width(infile, image_size):
    """按照宽度进行所需比例缩放,调整为image_size的大小"""
    print(infile)
    im = Image.open(infile)
    (x, y) = im.size
    lv = round(y / image_size, 2) + 0.01
    x_s = int(x // lv)
    y_s = int(y // lv)
    print("x_s", x_s, y_s)
    out = im.resize((x_s, y_s), Image.ANTIALIAS)
    return out

def get_new_img_xy(infile, image_size):
    """返回一个图片的宽、高像素"""
    im = Image.open(infile)
    (x, y) = im.size
    lv = round(x / image_size, 2) + 0.01
    x_s = x // lv
    y_s = y // lv
    # print("x_s", x_s, y_s)
    # out = im.resize((x_s, y_s), Image.ANTIALIAS)
    return x_s, y_s

# 定义图像拼接函数
def image_compose(rownum, colnum, image_paths, x_new, y_new,image_size):
    '''
    输入 行数/列数/图片名称列表/变换后的长/变换后的宽/
    '''
    to_image = Image.new('RGB', (colnum * x_new, rownum * y_new), 'white')  # 创建一个新图
    # 循环遍历，把每张图片按顺序粘贴到对应位置上
    total_num = 0
    for y in range( rownum ):
        for x in range( colnum):
            # 抓取图片
            dir_ = image_paths[y  + x ]
            
            # * 按照比例缩放 所有图等比例/每行图片宽度统一
            from_image = Image.open(dir_).resize(
                (x_new, y_new), Image.ANTIALIAS)
            # from_image = resize_by_width(dir_, image_size)

            to_image.paste(from_image, (x * x_new, y * y_new))

            total_num+=1
            if total_num == len(image_paths):
                break
    # to_image.show()
    return to_image.save('./tmp/final.jpg')  # 保存新图

def merge_image(image_paths,x_new,y_new,colnum,image_size=400*2):


    image_rownum_yu = len(image_paths) % colnum
    if image_rownum_yu == 0:
        rownum = len(image_paths) // colnum
    else:
        rownum = len(image_paths) // colnum + 1
    
    if len(image_paths) == 1:
        rownum, colnum = 1,1
    
    print(rownum, colnum)


    # 计算最佳x_new, y_new
    # x_list = []
    # y_list = []
    # for img in image_names:
    #     img_file = IMAGES_PATH + img
    #     img_x, img_y = get_new_img_xy(img_file, image_size)
    #     x_list.append(img_x)
    #     y_list.append(img_y)
    # print("x_list", sorted(x_list))
    # print("y_list", sorted(y_list))
    # x_new = int(x_list[len(x_list) // 5 * 4])
    # y_new = int(y_list[len(y_list) // 5 * 4])
    # print(x_new,y_new)


    image_compose(rownum, colnum, image_paths, x_new, y_new,image_size)


def merge(figs, img_size =(600*2,400*2),colnum=2):
    x_new, y_new = img_size
    image_paths=[]
    for i in range(len(figs)):
        f = figs[i] 
        f.savefig( './tmp/{}.jpg'.format(str(i+1)), bbox_inches='tight',dpi = 300)
        image_paths.append('./tmp/{}.jpg'.format(str(i+1)))
    merge_image(image_paths, x_new, y_new, colnum)
    return './tmp/final.jpg'
# 输出的是一张包含多个子图的画布
# 画布大小取决于x_new,y_new
# x_new,y_new来源于原图经过imagesize的限制下计算得到，这是因为各子图的原图比例尺不一样

# figsize只决定框的大小
# 因此mpl出图的时候需要尽量保证比例的一致（问题无法避免）


# * test
# IMAGES_PATH = '/Users/wdt/Desktop/tpy/Data_Tools/【数据库更新】/报告/生成的报告/周报图片输出地址/'
# IMAGES_FORMAT = ['.jpg', '.JPG'] 
# image_names = [IMAGES_PATH+name for name in os.listdir(IMAGES_PATH) for item in IMAGES_FORMAT if
#                os.path.splitext(name)[1] == item]
# merge_image(image_names,1000,400, 2)




# import ReportGenerator as rg
# report = rg.weeklyReport()
# fig1 = report.cash_cost('2020-01-06','2021-01-01')
# fig2 = report.prmy_mkt_weekly_issue('2021-05-17', '2021-05-23')

# figs = [fig1, fig2]

# merge(figs)

