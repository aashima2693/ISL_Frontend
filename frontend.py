import gradio as gr
import requests
import cv2
import tempfile
import os

def save_video(video_frames, video_path, fps=20.0):
    height, width, _ = video_frames[0].shape
    video_writer = cv2.VideoWriter(video_path, cv2.VideoWriter_fourcc(*'mp4v'), fps, (width, height))
    for frame in video_frames:
        video_writer.write(frame)
    video_writer.release() 

def sendVideoInputToBackend(video_input):
    with tempfile.NamedTemporaryFile(suffix=".mp4", delete=False) as temp_video_file:
        temp_video_path = temp_video_file.name
        save_video(video_input, temp_video_path)  

    with open(temp_video_path, "rb") as video_file:
        response = requests.post(" ", files={"video": video_file})  
        os.remove(temp_video_path)
        return response.json().get("text_output", "Error: Unable to fetch output")


isl = gr.Interface(
    fn=sendVideoInputToBackend,
    inputs="video",
    outputs=gr.Textbox(label="Text output", lines=5),
    title="Indian Sign language",
    description="This interface converts Indian Sign Language to text",
    theme="default",
    article="<p style='text-align: center;'>Please allow access to your webcam.</p>",
    css=".container{max-width:800px; margin:40px auto;}"
)
if __name__ == "__main__":
    isl.launch()