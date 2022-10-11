# pixelArt
Convert image or video into pixelized render

## Execution
```bash
python pixelArt.py
```

## Requirements
`pip install -r requirements.txt`

ToDo: Trim packages, some are from itterative development and are no longer required
 
## Usage
For now, command line is not supported.  Modify the code at bottom of code.

Instantiate the PixelArt class

Call either convert_image or convert_video

Optional parameters:
 - file_name - original image or video filename (REQUIRED)
 - width - number or pixel's horizontally for resultant image
 - height - number of pixel's vertically for resultant image
 - method = [pixelate, greyscale, ascii]
 - pixelate - new "pixel" is average of those in block
 - greyscale - new "pixel" is greyscale of the Pixelate average of those in block
 - ascii - new "pixel" is ascii density representation of greyscale for this block
 - show_original - display original image prior to conversion
 
 ## ToDo
  - Save new image file
  - Change font size based on final image size
  - Only accept 1 param for pixel/chunks, interpolate other dimension
  - Clean up some dupe code in video section for image init
  - GUI front end
  - Command line front end
  - Input = webcam, Output = LiveView, stuttered framerate, but accecptable
  

## Contact
Caleb Cohen  
Caleb@Hail2Pitt.org  
https://github.com/PittCaleb  
Twitter: [@PittCaleb](https://www.twitter.com/PittCaleb)
