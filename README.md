# edge-tts-v1
对edge-tts库的二次封装
### 注意
禁止一切商业使用行为

### 使用方法
#### 合成参数：
- text是转换成声音的文本
- role使用哪个角色进行合成
- rate语速(正加负减)
- volume音量(正加负减)
#### 单项合成
- tts() 执行cmd命令进行合成
- tts_v2() 隐藏命令窗口
- tts_v3() 对最后文件命名加入了序号
EdgeTTsApi().tts(text='只因你太美', role=e.voice['Female'][0], rate=10, volume=10)
#### 异步合成
EdgeTTsApi().async_tts_v2(text='只因你太美', role=e.voice['Female'][0], rate=10, volume=10)

### 注意
切记禁止一切商业使用行为，否则小心律师函警告

