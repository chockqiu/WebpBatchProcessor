import os
import time
from PIL import Image
import File
import argparse


if __name__ == "__main__":
    parser = argparse.ArgumentParser(prog="webpera", description="webp图片(动图)工具, 支持将动图进行压缩")
    parser.add_argument("files", type=str, nargs="+")
    parser.add_argument("-q", type=int, metavar="quality", required=False, dest="quality", default=85,
                        help="质量百分比[0-100]")
    parser.add_argument("-j", "--jump", type=int, metavar="kbs", dest="jump", default=5,
                        help="webp文件重新压缩时压缩字节数小于多少个kb时跳过不处理")
    parser.add_argument("-p", "--pause", action="store_true", dest="pause", default=False,
                        help="执行完是否暂停窗口以便查看输出")

    args = parser.parse_args()
    quality = args.quality
    files = args.files
    pause = args.pause
    jump = args.jump * 1024
    # print("jump: %s" % jump)
    # print("files: %s" % files)

    for f in files:
        file = File.File(f)
        if file.exists() and file.isFile():
            filename = file.getName()
            if not filename.endswith(".9.png"):
                if filename.endswith(".webp"):
                    print("Processing %s" % filename)
                    im = Image.open(file.getPath())
                    tmp_file_path = filename[:filename.index(".")] + "_%s.webp" % time.time()
                    im.save(tmp_file_path, "WEBP", quality=quality, method=6, save_all=True, allow_mixed=True, minimize_size=True)
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
                    print("Saved %s" % filename)
                else:
                    print("[%s] not support" % filename)
                    pass
            else:
                print("[%s] not support" % filename)
        else:
            print("[%s] not found" % file.getPath())
    if pause:
        print("\n")
        print("-" * 30)
        input("程序执行完毕，按回车结束程序")
