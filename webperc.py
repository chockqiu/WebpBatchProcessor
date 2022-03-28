import os
import time
from PIL import Image
import File
import argparse


if __name__ == "__main__":
    parser = argparse.ArgumentParser(prog="webperc", description="webp图片转换工具, 支持将jpg/jpeg/png/webp转成Webp格式图片[不支持.9图]")
    parser.add_argument("files", type=str, nargs="+")
    parser.add_argument("-q", type=int, metavar="quality", required=False, dest="quality", default=85,
                        help="质量百分比[0-100]")
    parser.add_argument("-j", "--jump", type=int, metavar="kbs", dest="jump", default=5,
                        help="webp文件重新压缩时压缩字节数小于多少个kb时跳过不处理")

    args = parser.parse_args()
    quality = args.quality
    files = args.files
    jump = args.jump * 1024
    # print("jump: %s" % jump)
    # print("files: %s" % files)

    for f in files:
        file = File.File(f)
        if file.exists() and file.isFile():
            filename = file.getName()
            if not filename.endswith(".9.png"):
                if filename.endswith(".png") or filename.endswith(".jpg") or filename.endswith(".jpeg"):
                    try:
                        im = Image.open(file.getPath()).convert("RGBA")
                        tmp_file_path = filename[:filename.index(".")] + ".webp"
                        im.save(tmp_file_path, "WEBP", quality=quality)
                        im.close()
                        tmp_file = File.File(tmp_file_path)
                        s_size = file.length()
                        t_size = tmp_file.length()
                        ps = s_size - t_size
                        pp = (s_size - t_size) / s_size*100
                        if pp < 0:
                            print("膨胀:%.5G%%\t 多了%.5g bytes\t [%s]\t不处理..." % (-pp, ((t_size - s_size) / 1024), filename))
                            tmp_file.delete()
                        elif ps < jump:
                            print("压缩:%.5G%%\t 节省%.5g bytes\t [%s]\t不处理..." % (pp, ((s_size - t_size) / 1024), filename))
                            tmp_file.delete()
                        else:
                            print("压缩:%.5G%%\t 节省%.5g bytes\t [%s]" % (pp, ((s_size - t_size) / 1024), filename))
                    except Exception as e:
                        print("文件处理异常[%s]" % filename)
                        print("%s" % e)
                elif filename.endswith(".webp"):
                    im = Image.open(file.getPath()).convert("RGBA")
                    tmp_file_path = filename[:filename.index(".")] + "_%s.webp" % time.time()
                    im.save(tmp_file_path, "WEBP", quality=quality)
                    im.close()
                    tmp_file = File.File(tmp_file_path)
                    s_size = file.length()
                    t_size = tmp_file.length()
                    ps = s_size - t_size
                    pp = (s_size - t_size) / s_size * 100
                    if pp < 0:
                        print("膨胀:%.5G%%\t 多了%.5g bytes\t [%s]\t不处理..." % (-pp, ((t_size - s_size) / 1024), filename))
                        tmp_file.delete()
                    elif ps < jump:
                        print("压缩:%.5G%%\t 节省%.5g bytes\t [%s]\t不处理..." % (pp, ((s_size - t_size) / 1024), filename))
                        tmp_file.delete()
                    else:
                        print("压缩:%.5G%%\t 节省%.5g bytes\t [%s]" % (pp, ((s_size - t_size) / 1024), filename,))
                        file.delete()
                        tmp_file.rename(filename)
                else:
                    print("[%s] not support" % filename)
                    pass
            else:
                print("[%s] not support" % filename)
        else:
            print("[%s] not found" % file.getPath())
