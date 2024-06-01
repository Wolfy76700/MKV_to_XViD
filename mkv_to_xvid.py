from copy import deepcopy
import glob
import os
import json
import ffmpeg
from os.path import exists as file_exists
import shutil
from urllib.parse import unquote, urlparse
from pymediainfo import MediaInfo
import argparse
from pathlib import Path

def convert_video(filename, audio_track_index=0, crop=""):
    stream = ffmpeg.input(filename)
    media_info = MediaInfo.parse(filename)
    input_video = stream["v:0"]
    input_audio = stream[f"a:{audio_track_index}"]
    extension = filename.split(".")[-1]

    params = {
        "c:v": "mpeg4", "vtag": "xvid", "acodec": "ac3", "b:v": "2M", "b:a": "448k" 
    }
    
    for track in media_info.tracks:
        if track.track_type == "Video":
            framerate = float(track.frame_rate)
            width = int(track.width)
            height = int(track.height)
    params["aspect"]=f"{width}:{height}"
    if crop:
        params["aspect"]=crop
    output_width, output_height = width, height
    if output_width >= 720 or crop:
        output_width = 720
    if output_height >= 576 or crop:
        output_height = 576
    while framerate > 30:
        framerate = framerate/2
    params["vf"] = f"scale={output_width}:{output_height},fps={framerate}"

    if crop:
        params["vf"] = "crop=" + crop + "," + params["vf"]

    out = ffmpeg.output(input_video, input_audio, "out/" + filename.replace(f".{extension}", ".avi"), **params)
    out.run()

if __name__ == "__main__":
    Path("out").mkdir(parents=True, exist_ok=True)
    parser = argparse.ArgumentParser("MKV to XViD")
    parser.add_argument("--audio_track", default=0, help="Audio track to be used for the XViD output files\nPlease make sure all MKV files in the folder have the indicated track index", type=int, required=False)
    parser.add_argument("--crop", default="", help="Set a symmetrical FFmpeg crop for the input files, e.g. 1920:800", type=str, required=False)

    args = parser.parse_args()

    for format in ["mkv", "mp4", "webm"]:
        for filename in glob.glob(f"*.{format}"):
            convert_video(filename, args.audio_track, args.crop.replace(",", ""))

input("Press the <ENTER> key to close the program...")