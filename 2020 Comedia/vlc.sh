/Applications/VLC.app/Contents/MacOS/VLC -vvv ~/Downloads/34750853_10213718474570170_2875072625728552960_o.jpg --sout '#transcode{vcodec=mp4v,acodec=mpga,vb=800,ab=128,deinterlace}:
rtp{mux=ts,dst=239.255.12.42,sdp=sap,name="TestStream"}'  
