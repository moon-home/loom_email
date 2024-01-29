import subprocess, os, time
import cv2

directory = 'video/3-elongated'
website_vfiles = []
for fname in os.listdir(directory):
    if fname.endswith('.mov'):
        fname = os.path.join(directory, fname)
        website_vfiles.append(fname)
print(website_vfiles)

for i, ws in enumerate(website_vfiles):
    speaker_vfile = 'video/circle_head_3584x2160.mov'
    speaker = cv2.VideoCapture(speaker_vfile)
    foreground_width = int(speaker.get(cv2.CAP_PROP_FRAME_WIDTH))
    foreground_height = int(speaker.get (cv2.CAP_PROP_FRAME_HEIGHT)) 
    # print(f"talking head video width and height: {foreground_width, foreground_height}") # 3584 2160

    print(f"####{i}: {ws}")
    start_time = time.time()
    id_str = ws[len(directory)+1:-4]
    overlay_noaudio_vfile = 'overlay_' + id_str + '.mov'
    output_vfile = 'video/4-overlayed/' + id_str + '.mov'
    # print(f"    overlay_noaudio_vfile: {overlay_noaudio_vfile}")
    # print(f"    final_vfile: {output_vfile}")

    website = cv2.VideoCapture(ws)
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    output_video = cv2.VideoWriter(overlay_noaudio_vfile, fourcc, 24.0, (int(website.get(3)),int(website.get(4))))

    background_width = int(website.get(cv2.CAP_PROP_FRAME_WIDTH)) 
    background_height = int (website.get(cv2.CAP_PROP_FRAME_HEIGHT))
    # print(f"    talking head video width and height: {background_width, background_height}") # 3584 2160

    ct=0
    while True:
        background_success, background_frame = website.read() 
        foreground_success, foreground_frame = speaker.read()
        if not background_success or not foreground_success: break
        if ct%100 ==0: print(f"    keep going ... {ct}")

        foreground_frame_resized = cv2.resize(foreground_frame, (background_width, background_height))

        # Convert the foreground frame to grayscale and threshold it
        foreground_gray = cv2.cvtColor(foreground_frame_resized, cv2.COLOR_BGR2GRAY) 
        ret, mask = cv2.threshold(foreground_gray, 10, 255, cv2.THRESH_BINARY)
        # Invert the mask so that the foreground is white and the background is black 
        mask_inv = cv2.bitwise_not(mask)
        # Use the mask to extract the foreground from the foreground frame
        foreground_extracted = cv2.bitwise_and(foreground_frame_resized, foreground_frame_resized, mask=mask)
        # Use the inverted mask to extract the background from the background frame
        background_extracted = cv2.bitwise_and(background_frame, background_frame, mask=mask_inv)
        # Combine the foreground and background
        output_frame = cv2.add(foreground_extracted, background_extracted)
        # Write the output frame to the output video
        output_video.write(output_frame)
        # print(ct)
        ct += 1
        # print(output_frame[0][0])

    website.release()
    output_video.release()
    speaker.release()
    cv2.destroyAllWindows()
    subprocess.call('ls', shell=True) 

    cmd = f'ffmpeg -i {overlay_noaudio_vfile} -i video/circle_head_3584x2160.mov -map 0:v:0? -map 1:a:0 {output_vfile}'
    subprocess.call(cmd, shell=True)                               
    # os.remove(overlay_noaudio_vfile)

    end_time = time.time()
    elapsed_time = end_time - start_time
    hours, rem = divmod(elapsed_time, 3600)
    minutes, seconds = divmod(rem, 60)
    hours, minutes, seconds = int(hours), int(minutes), int(seconds)
    print(f"    this overlay took {minutes} minutes {seconds} seconds")

# ffmpeg -i overlay_3berkley_Angela_Berkley.mov -i circle_head_3584x2160.mov -map 0:v:0 -map 1:a:0 overlayed/3berkley_Angela_Berkley.mov