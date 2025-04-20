import os
import socket
import random
import openai
import speech_recognition as sr

# OpenAI API Key
openai.api_key = os.getenv("OPENAI_API_KEY")  # Or set directly: "sk-..."

# EV3 IP and port
EV3_IP = "your_EV3_ip_address"
EV3_PORT = 12345

# Speech recognition with microphone
def recognize_speech():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("\n🎤 Please speak your command (say '退出' to quit):")
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source)
        try:
            text = recognizer.recognize_google(audio, language="zh-CN")
            print("✅ Recognized:", text)
            return text
        except sr.UnknownValueError:
            print("❌ Speech not recognized")
            return None
        except sr.RequestError as e:
            print("❌ Speech service error:", e)
            return None

# Prompt to classify or reply
agent_info_prompt = ""

def ask_llm(question):
    system_prompt = (
        "你是一个机器人，接收用户的指令，判断是否为控制指令。如果是控制机器人移动的意图，"
        "则只严格返回以下标准关键词之一：{前进, 后退, 停止, 左转, 右转, 自动, 距离, 退出}。"
        "如果用户的输入不属于以上控制意图，请你作为普通对话助手简要回答，不要回复任何关键词。"
        + agent_info_prompt
    )
    try:
        response = openai.ChatCompletion.create(
            model="gpt-4",  # or "gpt-3.5-turbo"
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": question}
            ]
        )
        reply = response.choices[0].message.content.strip()
        print("🤖 LLM Reply:", reply)
        return reply
    except Exception as e:
        print("❌ LLM error:", e)
        return "无效指令"

# Send TCP command to EV3
def send_to_ev3(message):
    try:
        with socket.create_connection((EV3_IP, EV3_PORT), timeout=10) as sock:
            sock.sendall(message.encode("utf-8"))
            print("📤 Sent to EV3")
    except Exception as e:
        print("❌ Failed to connect/send to EV3:", e)

# Main loop
def main():
    print("🚀 Voice control started. Say '退出' to stop.")
    try:
        while True:
            question = recognize_speech()
            if question:
                if "退出" in question:
                    print("👋 Exit command received. Shutting down.")
                    break
                answer = ask_llm(question)
                send_to_ev3(answer)
    except KeyboardInterrupt:
        print("\n🛑 Interrupted manually. Exiting.")

if __name__ == "__main__":
    main()
