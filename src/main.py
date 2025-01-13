import cv2
import pytesseract
import time
import json
import datetime
import os
from rapidfuzz import fuzz

def extract_text_from_video(video_path):
    cap = cv2.VideoCapture(video_path)
    fps = cap.get(cv2.CAP_PROP_FPS)
    text_dict = {}
    video_name = video_path.split("/")[-1]
    start_time = time.time()
    frame_count = 0
    interval_frames = int(fps * 10)  
    last_extracted_text = ""
    last_timestamp = None
    similarity_threshold = 60  

    while cap.isOpened():
        ret, frameWithWaterMark = cap.read()
        if not ret or frameWithWaterMark is None:
            print()
            break
       
        
        height, width, _ = frameWithWaterMark.shape
        watermark_height_percentage = 0.05  

        watermark_height = int(height * watermark_height_percentage)
        frame = frameWithWaterMark[0:height-watermark_height, 0:width]

        if frame_count % interval_frames == 0:
            gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            extracted_text = pytesseract.image_to_string(gray_frame).strip()

            if extracted_text:  
                if last_extracted_text:
                    similarity = fuzz.partial_ratio(last_extracted_text, extracted_text)
                    print(f"Similarity: {similarity}")

                    if similarity > similarity_threshold:
                        appended_text = extracted_text[len(last_extracted_text):].strip()
                        last_extracted_text += f"\n{appended_text}" if appended_text else ""
                        if last_timestamp is not None:
                            text_dict[last_timestamp] = last_extracted_text
                    else:
                        timestamp = int(frame_count / fps)
                        last_extracted_text = extracted_text
                        text_dict[timestamp] = extracted_text
                        last_timestamp = timestamp
                else:
                    last_timestamp = int(frame_count / fps)
                    last_extracted_text = extracted_text
                    text_dict[last_timestamp] = extracted_text

                print(f"Extracted Text at {int(frame_count / fps)}s: {last_extracted_text}")
    
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
    video_path = "./data/AI1_Kohlhase.m4v"  
    extracted_text = extract_text_from_video(video_path)
    print("Extracted Text Dictionary:")
    print(extracted_text)
