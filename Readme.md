# Video OCR Extraction Project

This project is designed to extract text from video frames using Optical Character Recognition (OCR). It processes video files, extracts text from frames at 10-second intervals (or configurable), and stores the results in a JSON file.

## Features

- Extract text from video frames at specified intervals.
- Skip frames with minimal differences using frame comparison.
- Save OCR results in a `Results.json` file, appending new results each time.
- Uses `Tesseract OCR` for text extraction and `OpenCV` for frame processing.

## Requirements

- Python 3.6 or higher
- Required Python libraries (listed in `requirements.txt`)

## Setup Instructions

### 1. Clone the Repository

Start by cloning the repository to your local machine:

git clone `https://github.com/abhishek2021005/ocr-python.git`

### 2. Create a Virtual Environment

Create a virtual environment to isolate the project dependencies:

Activate the virtual environment:

- **macOS/Linux**:
  source venv/bin/activate

- **Windows**:
  venv\Scripts\activate

### 3. Install Dependencies

pip install -r requirements.txt

### 4. Set the Video File Path

Replace the `video_path` in the script (`src/main.py`) with the path to the video file you wish to process.

video_path = `/path/to/your/video/file.mp4`

### 5. Run the script

python src/main.py
or
python3 src/main.py

### Customize frame interval(optional)

The script processes frames at 10-second intervals by default. You can change the interval by modifying the following line in main.py

interval_frames = int(fps \* 10) # Change 10 to your desired interval (in seconds)

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
