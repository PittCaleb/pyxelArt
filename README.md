# pyxelArt
Convert image or video into pixelized render

## Execution
Web Interface:
```bash
python web.py
```
 - Open browser to: http://127.0.0.1:8000/

via Code:
```bash
python pyxelart.py
```

## Requirements
`pip install -r requirements.txt`
 
## Usage
Best practice, use via *web interface*

**Via Code:**

Instantiate the PyxelArt class

Call either convert_image or convert_video

Optional parameters:
 - file_name - original image or video filename (REQUIRED)
 - width - number of pixel's horizontally for resultant image
 - height - number of pixel's vertically for resultant image
 - method = [pyxelate, greyscale, ascii]
   - pyxelate - new "pixel" is average of those in block
   - greyscale - new "pixel" is greyscale of the Pyxelate average of those in block
   - ascii - new "pixel" is ascii density representation of greyscale for this block
 - show_original - display original image prior to conversion
 
 ## Notes
  - You may add additional fonts in the /fonts directory and they will automagically be available to the user
  - This was written for local, it is not offered as "safe" from a file or validation POV
 
 ## ToDo
  - Web front end (flack/jinja)
    - Change file button on process entry screen
    - Style forms nicely
    - Proper intro and explainer
    - About/Help Page 
    - Interactive screen, respond to changes in process form
    - Modify Settings and re-PyxelArt underneath resultant image/video
  - Change font size based on final image size
  - Clean up some dupe code in video section for image init
  - Input = webcam, Output = LiveView, stuttered framerate, but accecptable
  - ASCII Options: Simplified/Complex (web interface & class init)
  - Use is_image everywhere
  - Clean up static files
  - Get video to play natively
  - Save thumbnail from video
  - pre-count video frames
  - Estimate time based on frame-rate for video processing
  - Progres feedback for video processing
  

## Done/Scraped
  - ~~Clean up requirements.txt~~
  - ~~GUI front end~~
  - ~~Command line front end~~
  - ~~Save new image file~~
  - ~~Only accept 1 param for pixel/chunks, interpolate other dimension~~
  - ~~Rename app from pixelArt to pyxelArt~~
  - ~~Build web frontend~~


## Contact
Caleb Cohen  
Caleb@Hail2Pitt.org  
https://github.com/PittCaleb  
Twitter: [@PittCaleb](https://www.twitter.com/PittCaleb)
