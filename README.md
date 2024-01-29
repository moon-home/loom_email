# Why is this worth doing?

[Clipio](https://clipio.com/) is a cheaper option than [pitchlane](https://pitchlane.com/?gclid=CjwKCAiAtt2tBhBDEiwALZuhAA6eUbE9iTTvlpcibtNnvmvJpO-58IX8LHac_woj7nIADLqF8qS2hBoCXV8QAvD_BwE), however, both of them have the following problems:
- the video doesn't actually scroll over, it's just a stactic website screenshot with a moving cursor
- It costs a significant amount of money. If you are ready to scale, it's a good deal, but if you are testing things out, you may not want to pay for that. Clipio still costs $97/mo to generate 5000 videos.

I found the first 2 problems embarrasing for my brand.

This solution does take longer time to run, but you can get better screenrecording videos with zero dollar cost:

# High Level Steps:
### Step 1 - Generate 10 second website recording (`website_recording.py`)
    - a python script
    - visit each URL with Selenium
    - interact the website as pause, scroll down, pause, and scroll up for 10 seconds in total
    - use an unblocking screenrecording solution, which means you can interact and record the scree at the same time 
    - iterate through URLs with each URL visit generates a video file

### Step 2 - Extends 10 seconds screen recording to 2 minutes video (`slow_elongate.sh`)
    - a shell script
    - slow down 10 seconds into 30 seconds video, because when Selenium scrolls the page, the Python API doesn't provde a good control over the scrolling speed and it looks unnatural.
    - use last frame to fill up another 90 seconds becuase your video should focus on your sales pitch, not the their website, their website is only grab the attention
    - wola, you got a 2 minute video

### Step 3 - Prepare talking head video (One time thing, `Final Cut Pro`)
    - manually by any video recorder
    - crop your 2 minutes talking head video into a circle
    - repositioned properly
    - background should be pure black for overlay mask in the next step

### Step 4 - Overlay the talking head on the website video(`overlay.py`)
    - Manual setup for the very first time
        1. resize the talking head video and the website/profile video (the automated recording videos we got earlier) to same frame size so that they can be overlayed using `cv2`
        2. inspect the video to set proper codec, fps, and frame size for the overlay output file
    - Each batch
        1. mask the black background of each talking head frame into transparent
        2. merge each mased talking head frame with website frame
        3. generate overlay video without audio
        4. add audio from original talking head video into the genreated overlay video
        5. I ran 100 videos each time which takes about 8 hours form URL to ready to send videos.

### Step 5 - Upload to Instantly or Gmails

    ** you need to track the view rate of your video, so you need a video host and tracking solution**
    **  only allows uploading 10 videos each time **

# Tech Challenges
1. find an unblocking screen recorder that works with Selenium interactions
2. sync audio back to the video after video is edited with CV2


# Final

This repo isn't actively mainteined, so if you encountered technical issues or have questions specific to your business operation, please join our [free community on skool](https://www.skool.com/ai-for-coaches-creators-2571/about). You can post your issues or attending free daily workshops to get the help you need. 