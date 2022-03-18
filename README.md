# WebpBatchProcessor
webp图片批处理工具, 支持将jpg/jpeg/png/webp转成webp格式图片

```
usage: webper [-h] [-d directory] [-q quality] [-r] [-o] [-j percentage]

webp图片批处理工具, 支持将jpg/jpeg/png/webp转成Webp格式图片[不支持.9图]

optional arguments:
  -h, --help            show this help message and exit
  -d directory, --dir directory
                        运行文件夹
  -q quality, --quality quality
                        质量百分比[0-100]
  -r, --reformat        webp文件是否需要重新压缩
  -o, --overwrite       是否覆盖源文件
  -j percentage, --jump percentage
                        webp文件重新压缩时压缩字节数小于多少个百分比时跳过不处理
```

##### 使用示例
##### - Windows环境
下载 webper.exe
> 链接: https://pan.baidu.com/s/1FzhA2HXUBcr56MEYvLVtiw?pwd=46rd 
提取码: 46rd 
```
webper.exe -d ./testimgs -r -q 80
```

###### - Python环境
```
python webper.py -d ./testimgs -r -q 80
```