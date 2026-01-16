# YouTube Music Thumbnail Generator

This tool generates 1280x720 PNG thumbnails with fixed text placement.

## File structure

- generate.py
- requirements.txt
- input\background\  (put your background images here)
- output\            (generated thumbnails appear here)

## How to run (beginner steps)

1) Install Python 3.10+ (from python.org) and check the box "Add Python to PATH".
2) Open PowerShell and go to the project folder:

   cd C:\Users\jinhy\youtube-thumbnail-tool

3) Install the required library:

   python -m pip install -r requirements.txt

4) Put background images into:

   C:\Users\jinhy\youtube-thumbnail-tool\input\background

5) Run the generator:

   python generate.py

6) Check output PNGs in:

   C:\Users\jinhy\youtube-thumbnail-tool\output

## Notes

- The text lines are fixed to:
  PLAYLIST
  LOW NOISE SESSION
  Celestria Nova
- Font, position, and letter spacing are fixed in generate.py
- If you want a different font, edit FONT_PATH in generate.py
  Example: C:\Windows\Fonts\arial.ttf
