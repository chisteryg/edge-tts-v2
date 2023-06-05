# 标准库
import os
import time
import asyncio
import subprocess
from os import path, popen as po
# 第三方库
import edge_tts


class EdgeTTsApi:
    def __init__(self):
        self.voice = {
            # 女性角色
            "Female": ["zh-CN-XiaoxiaoNeural", "zh-CN-XiaoyiNeural", "zh-CN-liaoning-XiaobeiNeural", "zh-CN-shaanxi-XiaoniNeural"],
            # 男性角色
            "Male": ["zh-CN-YunjianNeural", "zh-CN-YunxiNeural", "zh-CN-YunxiaNeural", "zh-CN-YunyangNeural"]
        }
        prjPath = os.path.abspath('.')
        # print(prjPath)
        self.outputPath = prjPath + '\\static\\audio'
        self.loop = asyncio.get_event_loop()


    def digitalTransStr(self, digital):
        # 将数字转为字符串
        return str(digital) if digital <= 0 else '+' + str(digital)

    def outputName(self, text):
        # 截取文件名
        return text if len(text) < 5 else text[0:6]

    def tts(self, text='', role='zh-CN-YunxiNeural', rate=1, volume=1):
        # 单tts，text转换文本, role使用角色, rate转换速度(正加负减), volume转换音量(正加负减)
        if text == '':
            # print('文本为空')
            return False
        if not path.exists(self.outputPath):
            os.mkdir(self.outputPath)
        output_name = self.outputPath + '\\' + self.outputName(text) + str(int(time.time())) + '.mp3'
        rate = self.digitalTransStr(rate)
        volume = self.digitalTransStr(volume)
        command = f'edge-tts --voice {role} --rate={rate}% --volume={volume}% --text "{text}" --write-media {output_name}'
        print(command)
        code = os.system(command)
        if code == 0:
            return output_name
        return False

    def tts_v2(self, text='', role='zh-CN-YunxiNeural', rate=1, volume=1):
        # 单tts，text转换文本, role使用角色, rate转换速度, volume转换音量
        if text == '':
            # print('文本为空')
            return False
        if not path.exists(self.outputPath):
            os.mkdir(self.outputPath)
        output_name = self.outputPath + '\\' + self.outputName(text) + str(int(time.time())) + '.mp3'
        rate = self.digitalTransStr(rate)
        volume = self.digitalTransStr(volume)
        command = f'edge-tts --voice {role} --rate={rate}% --volume={volume}% --text "{text}" --write-media {output_name}'
        print(command)
        # subprocess.Popen隐藏命令窗口
        code = subprocess.Popen(command, shell=True)
        code.wait()
        code = code.returncode
        if code == 0:
            return output_name
        return False

    def tts_v3(self, text='', role='zh-CN-YunxiNeural', rate=1, volume=1):
        # 单tts，text转换文本, role使用角色, rate转换速度, volume转换音量
        if text == '':
            # print('文本为空')
            return False
        if not path.exists(self.outputPath):
            os.mkdir(self.outputPath)
        count = str(len(os.listdir(self.outputPath)))
        output_name = self.outputPath + '\\' + count + '_' + self.outputName(text) + str(int(time.time())) + '.mp3'
        rate = self.digitalTransStr(rate)
        volume = self.digitalTransStr(volume)
        command = f'edge-tts --voice {role} --rate={rate}% --volume={volume}% --text "{text}" --write-media {output_name}'
        # subprocess.Popen隐藏命令窗口
        code = subprocess.Popen(command, shell=True)
        code.wait()
        code = code.returncode
        if code == 0:
            return output_name
        return False

    def batch_tts(self, role='zh-CN-YunxiNeural', rate=4, volume=4):
        # 异步批量tts，txt_list批量转换的文本列表，role使用角色，rate转换速度，volume转换音量

        # 检测路径
        txt_path = '..\\static\\txt'
        if not path.exists(txt_path):
            return False, ''

        def get_text(file_path):
            # 读取文本
            with open(file_path, 'rb') as f:
                data = f.read()
                text = data.decode('utf-8')
                text = text.replace('\n', '')
            return text

        text = ''
        output = '.mp3'
        voice = role
        rate = self.digitalTransStr(rate) + '%'
        volume = self.digitalTransStr(volume) + '%'

        async def my_function():
            # 单项异步合成
            tts = edge_tts.Communicate(text=text, voice=voice, rate=rate, volume=volume)
            await tts.save(output)  # 保存


        outputList = ''
        for item in os.scandir(txt_path):
            if item.is_file():
                text = get_text(item.path)
                if text != '':
                    output = self.outputPath + self.outputName(text) + str(int(time.time())) + '.mp3'
                    loop = asyncio.get_event_loop()
                    loop.run_until_complete(my_function())
                    outputList += '\n' + output
        return True, outputList

    def async_tts_v2(self, text, role='zh-CN-YunxiNeural', rate=4, volume=4):
        # 异步单项tts，txt_list批量转换的文本列表，role使用角色，rate转换速度，volume转换音量
        if text == '':
            # print('文本为空')
            return False
        if not path.exists(self.outputPath):
            os.mkdir(self.outputPath)
        count = str(len(os.listdir(self.outputPath)))
        output_name = self.outputPath + '\\' + count + '_' + self.outputName(text) + str(int(time.time())) + '.mp3'
        rate = self.digitalTransStr(rate) + '%'
        volume = self.digitalTransStr(volume) + '%'

        async def tts(text, role, rate, volume):
            # 单项异步合成
            tts = edge_tts.Communicate(text=text, voice=role, rate=rate, volume=volume)
            await tts.save(output_name)  # 保存



        self.loop.run_until_complete(tts(text, role, rate, volume))
        return True, output_name




if __name__ == '__main__':
    e = EdgeTTsApi()
    # example
    e.tts(text='只因你太美', role=e.voice['Female'][0], rate=10, volume=10)
    e.async_tts_v2(text='只因你太美', role=e.voice['Female'][0], rate=10, volume=10)
