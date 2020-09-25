import cv2
import urllib.request
import numpy as np

with urllib.request.urlopen("http://localhost:5500/stream/0/annotated") as url:
    stream = bytes()
    while True:
        stream += url.read(1024)
        a = stream.find(b'\xff\xd8')
        b = stream.find(b'\xff\xd9')
        if a != -1 and b != -1:
            jpg = stream[a:b+2]
            stream = stream[b+2:]
            i = cv2.imdecode(np.fromstring(jpg, dtype=np.uint8), cv2.IMREAD_COLOR)
            cv2.imshow('i', i)
            if cv2.waitKey(1) == 27:
                exit(0)   
