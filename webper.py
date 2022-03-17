import os
import sys
from PIL import Image
import File
import argparse


if __name__ == "__main__":
    parser = argparse.ArgumentParser(prog="webper", description="webp图片批处理工具, 支持 pg/jpeg/png/webp后缀图片 不支持.9图")
    parser.add_argument("-d", "--dir", type=str, metavar="directory", required=True, dest="directory", help="运行文件夹")
    parser.add_argument("-q", "--quality", type=int, metavar="quality", required=True, dest="quality", default=85,
                        help="质量百分比[0-100]")
    parser.add_argument("-r", "--reformat", type=bool, metavar="reformat", dest="reformat", default="false", help="webp文件是否需要重新压缩")
    parser.add_argument("-rw", "--overwrite", type=bool, metavar="overwrite", dest="overwrite", default="false", help="是否覆盖源文件")

    args = parser.parse_args()
    quality = args.quality
    reformat = args.reformat
    overwrite = args.overwrite
    if args.directory:
        directory = File.File(args.directory)
        if directory.exists() and directory.isDirectory():
            tempDir = File.File(args.directory + File.separator + "webptemp")
            if not tempDir.exists():
                tempDir.makedirs()
            else:
                #删除临时文件夹内文件
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
                                im = Image.open(file.getPath())
                                tmp_file_path = tempDir.getPath() + File.File.separator + filename[:filename.index(".")] + ".webp"
                                im.save(tmp_file_path, "WEBP", quality=quality)
                                tmp_file = File.File(tmp_file_path)
                                s_size = file.length()
                                t_size = tmp_file.length()
                                pp = (s_size - t_size) / s_size*100
                                print("%s -> 压缩: %s%%  save bytes: %s" % (filename, pp, (s_size - t_size)/1024))
                                d_list.append(tmp_file)
                                s_list.append(file)
                            except Exception:
                                print("文件处理异常(%s)" % filename)
                        elif filename.endswith(".webp") and reformat:
                            im = Image.open(file.getPath())
                            tmp_file_path = tempDir.getPath() + File.File.separator + filename
                            im.save(tmp_file_path, "WEBP", quality=quality)
                            tmp_file = File.File(tmp_file_path)
                            s_size = file.length()
                            t_size = tmp_file.length()
                            pp = (s_size - t_size) / s_size * 100
                            if pp < 0:
                                print("%s 无法再压缩" % filename)
                            else:
                                print("%s -> 压缩: %s%%  save bytes: %s" % (filename, pp, (s_size - t_size) / 1024))
                                d_list.append(tmp_file)
                                s_list.append(file)
                        else:
                            print("跳过文件:%s", filename)
            if len(s_list) > 0 and overwrite:
                for i in range(0, len(s_list)):
                    files = s_list[i]
                    if files.isFile():
                        print("%s deleting..." % files.getName())
                        files.delete()
                    filed = d_list[i]
                    filed.moveTo(directory + File.separator + filed.getName())
                    print("%s moving..." % files.getName())
                print("Done")
                tempDir.delete()
            else:
                tempDir.rename(args.directory + File.separator + "output")

        else:
            print("directory不是一个文件夹")
    else:
        print("directory参数缺失")
