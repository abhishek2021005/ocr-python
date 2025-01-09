import cv2
import pytesseract
import time
import json
import datetime
import os

def extract_text_from_video(video_path):
    cap = cv2.VideoCapture(video_path)
    fps = cap.get(cv2.CAP_PROP_FPS)
    text_dict = {}
    video_name = video_path.split("/")[-1]
    start_time = time.time()
    frame_count = 0
    last_frame = None
    interval_frames = int(fps * 10)

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break
        if frame_count % interval_frames == 0:
            gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            if last_frame is None or cv2.norm(last_frame, gray_frame, cv2.NORM_L2) > 4000:
                if last_frame is not None:
                    gray_frame_resized = cv2.resize(gray_frame, (last_frame.shape[1], last_frame.shape[0]))
                    print("Frame difference (L2 norm):", cv2.norm(last_frame, gray_frame_resized, cv2.NORM_L2))
                else:
                    print("First frame, no comparison.")
                text = pytesseract.image_to_string(gray_frame)
                timestamp = int(frame_count / fps)
                text_dict[timestamp] = text
                print(f"Extracted Text at {timestamp}s: {text}")
                last_frame = gray_frame
        frame_count += 1

    cap.release()
    cv2.destroyAllWindows()
    end_time = time.time()
    total_time = end_time - start_time
    processing_datetime = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    output_data = {
        "video_name": video_name,
        "text_data": text_dict,
        "total_processing_time_seconds": total_time,
        "processing_datetime": processing_datetime
    }
    results_file = "Results.json"
    if os.path.exists(results_file):
        with open(results_file, "r") as f:
            existing_data = json.load(f)
        existing_data.append(output_data)
        with open(results_file, "w") as f:
            json.dump(existing_data, f, indent=4)
    else:
        with open(results_file, "w") as f:
            json.dump([output_data], f, indent=4)

    print(f"Extracted text saved to {results_file}")
    print(f"Total processing time: {total_time:.2f} seconds")
    return text_dict

if __name__ == "__main__":
    video_path = "./data/AI1_Kohlhase.m4v" # Replace this with video path
    extracted_text = extract_text_from_video(video_path)
    print("Extracted Text Dictionary:")
    print(extracted_text)
