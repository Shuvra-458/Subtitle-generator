# 🎬 Real-Time Subtitle Generator

## 📌 Overview
The **Real-Time Subtitle Generator** is a Python-based tool that automatically transcribes audio and video files into accurate subtitles using OpenAI's Whisper model. It generates subtitles in **.srt**, **.txt**, and **.json** formats, making it ideal for content creators, researchers, and accessibility enhancements.

## 🚀 Features
✅ **Real-Time Speech-to-Text** – Converts speech into text with precise timestamps.
✅ **High Accuracy** – Uses Whisper's **large-v3** model (configurable) for high transcription quality.
✅ **Multiple Output Formats** – Generates **.srt** (subtitles), **.txt** (plain text), and **.json** (structured data).
✅ **GPU Acceleration Support** – Automatically utilizes CUDA if available for faster processing.
✅ **Batch Processing** – Processes multiple files in parallel to improve efficiency.
✅ **Automatic Language Detection** – Option to specify a language to prevent unintended translations.

## 🛠️ Installation
### **1️⃣ Install Dependencies**
Ensure you have Python 3.8+ installed. Then, install the required dependencies:
```bash
pip install openai-whisper tqdm torch torchvision torchaudio ffmpeg-python argparse
```
If you have an **NVIDIA GPU**, install the CUDA-optimized PyTorch version:
```bash
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118
```

### **2️⃣ Install FFmpeg**
The script relies on `ffmpeg` for audio processing. Install it using:
```bash
pip install ffmpeg-python
```
Or download it manually from [FFmpeg's official site](https://ffmpeg.org/download.html).

## 🎯 Usage
### **Basic Command**
To transcribe and generate subtitles, run:
```bash
python subtitle_generator.py "path/to/input/folder" "path/to/output/folder"
```
📌 **Example:**
```bash
python subtitle_generator.py "E:/Media" "E:/Media/Subtitles"
```

## ⚡ Performance Optimization
### **1️⃣ Speed vs. Accuracy**
The script defaults to `large-v3` for best accuracy, but you can switch to a smaller model for speed:
```python
model = whisper.load_model("medium")  # Change to 'small' or 'base' if needed
```

### **2️⃣ GPU Acceleration**
If a CUDA-compatible GPU is detected, the script automatically utilizes it for faster processing.

### **3️⃣ Process Video as Audio**
For faster performance, convert videos to audio before transcription:
```bash
ffmpeg -i input.mp4 -vn -acodec pcm_s16le -ar 16000 -ac 1 input.wav
```

## 📂 Output Files
For each media file, the following output files will be created:
📄 `example.txt` – Full text transcript
📂 `example.json` – Structured JSON transcript
📺 `example.srt` – Subtitle file with timestamps

### **Example .srt File:**
```
1
00:00:01,500 --> 00:00:05,200
Welcome to the real-time subtitle generator.

2
00:00:05,500 --> 00:00:10,000
This script automatically transcribes and generates subtitles.
```

## 🛠️ Troubleshooting
### **1️⃣ "Russian Language in Output"**
If transcription appears in the wrong language, explicitly set the language:
```python
result = model.transcribe(file_path, language="en")
```

### **2️⃣ "Slow Processing"**
- Use `medium` or `small` model instead of `large-v3`.
- Ensure GPU is available (`torch.cuda.is_available()`).
- Increase parallel processing (`max_workers=8`).

### **3️⃣ "Error: WindowsPath object has no attribute 'lower'"**
Ensure file paths are converted to strings:
```python
media_files = [str(f) for f in Path(input_folder).rglob("*") if f.suffix.lower() in {".mp3", ".wav", ".mp4", ".mkv", ".flac"}]
```


## 🙌 Contributing
Pull requests and improvements are welcome! Feel free to report issues or suggest enhancements.


---
🚀 **Transform your media into text with ease!** 🎬
