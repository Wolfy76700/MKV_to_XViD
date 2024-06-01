# MKV to XViD

Simple Python script to convert an MKV file into an XViD file which is readable by older DivX-enabled DVD players and other devices.

## How to use

1. Install FFmpeg and add it to your PATH
1. Place the Python script/EXE in the folder with your MKV, MP4 or WEBM files
1. Run the script

## Advanced command line usage

| Option | Description |
| :---: | :--- |
| `--audio_track` | Audio track to be used for the XViD output files. Please make sure all MKV files in the folder have the indicated track index |
| `--crop` | Set a symmetrical FFmpeg crop for the input files, e.g. `1920:800` |
