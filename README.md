# 🤖 LLM-Voice-Controlled LEGO EV3

This project enables voice-controlled communication with a LEGO EV3 robot using large language models (LLMs). The system interprets human voice commands, understands intent using OpenAI (or iFLYTEK SparkDesk), and sends control messages to the EV3 over TCP.

---

## 🔧 Features

- 🎤 Voice recognition via microphone (Google Speech API)
- 🧠 Intent recognition using OpenAI GPT or SparkDesk (ChatSparkLLM)
- 📡 TCP command transmission to EV3 robot
- 🤖 Real-time control: forward, backward, stop, turn, distance detection, autonomous navigation
- 🇬🇧 Fully internationalized: both English and Chinese versions included

---

## 🗂 Project Structure

| File | Description |
|------|-------------|
| `LLM_on_EV3.py` | English voice command client using LLM API |
| `LLM_on_EV3_CN.py` | Chinese voice command client using LLM API |
| `main.py` | EV3 server script for receiving and executing commands (English) |
| `main_CN.py` | EV3 server script for receiving and executing commands (Chinese) |

---

## 🚀 How It Works

1. Speak into your computer’s microphone.
2. Your command is transcribed using Google Speech Recognition.
3. The LLM determines whether it’s a robot control command or regular text.
4. If it’s a command (e.g., `forward`, `stop`), it is sent via TCP to the EV3 brick.
5. The EV3 receives the command and performs the action accordingly.

---

## 🧠 Supported Robot Commands

The LLM will only send **one of these control keywords** when robot intent is detected:

```text
forward, backward, stop, left, right, auto, distance, exit
