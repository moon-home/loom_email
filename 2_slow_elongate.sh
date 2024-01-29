#!/bin/bash

# video/1-recording/ is 18 characters
for FILE in video/1-recording/*; do 
    video_name=${FILE:18}
    ffmpeg -i $FILE -filter:v "setpts=3*PTS" video/2-slowed/$video_name
done

# video/2-slowed/ is 16 characters
for FILE in video/2-slowed/*; do 
    video_name=${FILE:15}
    ffmpeg -i $FILE -vf tpad=stop_mode=clone:stop_duration=92,scale=3584x2160,setsar=1:1 video/3-elongated/$video_name
done
