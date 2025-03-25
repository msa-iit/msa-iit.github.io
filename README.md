# IIT MSA TV Display

This is the code for the TV display in IIT's MSA prayer space. It provides a list of prayer times, the time left until the next prayer, and a slideshow of images from a Dropbox folder. Works only on Windows.

## Requirements and Setup

1. To run the display you need to have Python and Node.js installed. Install Node.js from their [website](https://nodejs.org/en).

2. Next install the necessary Python packages using `pip install -r requirements.txt` and install bootstrap using `npm install -g npm`.

3. Google Chrome should be installed. If you want to use another browser, modify the `start_display.bat` file accordingly.

4. Make sure all API keys and files are added to the `flask_api` folder. These are ommitted from the Github for privacy reasons, they need to be provided separately. The files are on the MSA laptop and can be distributed as needed for development.

## Starting the Display

Start the display by running the `start_display.bat` file. It will open a couple terminals (do not close them) and after a few seconds will open the display in Chrome. You can toggle full screen by using Fn+F11.

To stop the display, simply close out all active terminals. 

## Common Errors

If the slideshow isn't loading images, or the prayer times show as NaN, then check that there is an active internet connection.