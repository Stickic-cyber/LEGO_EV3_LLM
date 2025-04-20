import os
import socket
import openai
import speech_recognition as sr

# Set your OpenAI API Key
openai.api_key = os.getenv("OPENAI_API_KEY")  # Or hardcode here: "sk-..."

# EV3 connection settings
EV3_IP = "your_EV3_ip_address"
EV3_PORT = 12345

# Use microphone to recognize voice commands
def recognize_speech():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("\n🎤 Please speak your command (say 'exit' to quit):")
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source)
        try:
            # You can change "zh-CN" to "en-US" for English input
            text = recognizer.recognize_google(audio, language="zh-CN")
            print("✅ Recognized:", text)
            return text
        except sr.UnknownValueError:
            print("❌ Could not understand the audio")
            return None
        except sr.RequestError as e:
            print("❌ Speech recognition error:", e)
            return None

# Prompt template for LLM
agent_info_prompt = ""

def ask_llm(question):
    system_prompt = (
        "You are a robot assistant. Your job is to determine whether the user's command is intended "
        "to control the robot. If so, you must reply with one and only one of the following standardized "
        "control keywords: {forward, backward, stop, left, right, auto, distance, exit}. "
        "If the input is not related to control, respond briefly as a friendly assistant without using any keywords."
        + agent_info_prompt
    )
    try:
        response = openai.ChatCompletion.create(
            model="gpt-4",  # or use "gpt-3.5-turbo"
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": question}
            ]
        )
        reply = response.choices[0].message.content.strip()
        print("🤖 LLM Reply:", reply)
        return reply
    except Exception as e:
        print("❌ LLM Error:", e)
        return "invalid"

# Send command to EV3 robot via TCP
def send_to_ev3(message):
    try:
        with socket.create_connection((EV3_IP, EV3_PORT), timeout=10) as sock:
            sock.sendall(message.encode("utf-8"))
            print("📤 Sent to EV3:", message)
    except Exception as e:
        print("❌ Could not send to EV3:", e)

# Main control loop
def main():
    print("🚀 Voice-controlled robot started. Say 'exit' to stop.")
    try:
        while True:
            user_input = recognize_speech()
            if user_input:
                if "exit" in user_input.lower():
                    print("👋 Exit command received. Shutting down.")
                    break
                response = ask_llm(user_input)
                send_to_ev3(response)
    except KeyboardInterrupt:
        print("\n🛑 Program interrupted manually.")

if __name__ == "__main__":
    main()
