import os
import azure.cognitiveservices.speech as speechsdk

# 设置环境变量或直接在代码中指定订阅密钥和区域
speech_key = os.environ.get('SPEECH_KEY')
speech_region = os.environ.get('SPEECH_REGION')

speech_config = speechsdk.SpeechConfig(subscription=speech_key, region=speech_region)

convert_name = "3"
# 指定输出音频文件路径
audio_output_path = os.path.join("..", "output", convert_name + ".wav")
audio_config = speechsdk.audio.AudioOutputConfig(filename=audio_output_path)

speech_synthesizer = speechsdk.SpeechSynthesizer(speech_config=speech_config, audio_config=audio_config)

# 读取SSML文本从文件
ssml_file_path = os.path.join("..", "input", convert_name + ".txt")  # 请确保这是正确的路径
with open(ssml_file_path, 'r', encoding='utf-8') as file:
    ssml_text = file.read()

# 使用SSML文本进行语音合成
speech_synthesis_result = speech_synthesizer.speak_ssml_async(ssml_text).get()

if speech_synthesis_result.reason == speechsdk.ResultReason.SynthesizingAudioCompleted:
    print(f"Speech synthesized for the given SSML and saved to {audio_output_path}")
elif speech_synthesis_result.reason == speechsdk.ResultReason.Canceled:
    cancellation_details = speech_synthesis_result.cancellation_details
    print("Speech synthesis canceled: {}".format(cancellation_details.reason))
    if cancellation_details.reason == speechsdk.CancellationReason.Error:
        if cancellation_details.error_details:
            print("Error details: {}".format(cancellation_details.error_details))
            print("Did you set the speech resource key and region values?")

