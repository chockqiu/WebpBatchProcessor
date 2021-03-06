import os
import time
from PIL import Image
import File
import argparse


if __name__ == "__main__":
    parser = argparse.ArgumentParser(prog="webper", description="webp图片批处理工具, 支持将jpg/jpeg/png/webp转成Webp格式图片[不支持.9图]")
    parser.add_argument("-d", "--dir", type=str, metavar="directory", required=False, dest="directory", default=".",
                        help="运行文件夹")
    parser.add_argument("-q", "--quality", type=int, metavar="quality", required=False, dest="quality", default=85,
                        help="质量百分比[0-100]")
    parser.add_argument("-r", "--reformat", action="store_true", dest="reformat", default=False,
                        help="webp文件是否需要重新压缩")
    parser.add_argument("-o", "--overwrite", action="store_true", dest="overwrite", default=False,
                        help="是否覆盖源文件")
    parser.add_argument("-p", "--pause", action="store_true", dest="pause", default=False,
                        help="执行完是否暂停窗口以便查看输出")
    parser.add_argument("-j", "--jump", type=int, metavar="kbs", dest="jump", default=5,
                        help="webp文件重新压缩时压缩字节数小于多少个kb时跳过不处理")

    args = parser.parse_args()
    quality = args.quality
    reformat = args.reformat
    overwrite = args.overwrite
    pause = args.pause
    jump = args.jump * 1024
    # print("reformat: %s" % reformat)
    # print("overwrite: %s" % overwrite)
    # print("jump: %s" % jump)
    print("Working on: [%s]" % (args.directory + File.separator))
    if args.directory:
        directory = File.File(args.directory)
        if directory.exists() and directory.isDirectory():
            tempDir = File.File(args.directory + File.separator + "webptemp")
            outputDir = File.File(args.directory + File.separator + "output")
            if outputDir.exists():
                outputDir.delete()
            if not tempDir.exists():
                tempDir.makedirs()
            else:
                # 删除临时文件夹内文件
                for t in tempDir.listFile():
                    t.delete()
            d_list = []
            s_list = []
            for file in directory.listFile():
                if file.isFile():
                    filename = file.getName()
                    if not filename.endswith(".9.png"):
                        if filename.endswith(".png") or filename.endswith(".jpg") or filename.endswith(".jpeg"):
                            try:
                                im = Image.open(file.getPath()).convert("RGBA")
                                tmp_file_path = tempDir.getPath() + File.separator + filename[:filename.index(".")] + ".webp"
                                if quality == 100:
                                    im.save(tmp_file_path, "WEBP", lossless=True, method=6)
                                else:
                                    im.save(tmp_file_path, "WEBP", quality=quality, method=6)
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
                                    d_list.append(tmp_file)
                                    s_list.append(file)
                            except Exception:
                                print("文件处理异常[%s]" % filename)
                        elif filename.endswith(".webp") and reformat:
                            im = Image.open(file.getPath()).convert("RGBA")
                            tmp_file_path = tempDir.getPath() + File.separator + filename
                            im.save(tmp_file_path, "WEBP", quality=quality, method=6)
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
                                d_list.append(tmp_file)
                                s_list.append(file)
                        else:
                            # print("ignore:[%s]" % filename)
                            pass
                    else:
                        # print("ignore:[%s]" % filename)
                        pass
            if len(s_list) > 0 and overwrite:
                print("overwriting...")
                for i in range(0, len(s_list)):
                    files = s_list[i]
                    if files.isFile():
                        files.delete()
                    filed = d_list[i]
                    filed.moveTo(args.directory + File.separator + filed.getName())

                print("Done")
                tempDir.delete()
            else:
                tempDir.rename(outputDir.getPath())
                if len(outputDir.listFile()) == 0:
                    outputDir.delete()
                print("Done")
        else:
            print("directory不存在或者不是一个文件夹")
    else:
        print("directory参数缺失")
    if pause:
        print("\n")
        print("-" * 30)
        input("程序执行完毕，按回车结束程序")
