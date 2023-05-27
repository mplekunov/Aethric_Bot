from threading import Event, Thread
import time
from typing import Any, Dict, List, Tuple, Type, TypeAlias
import cv2

from numpy import dtype, generic, ndarray
from area import Area
from areaPainter import AreaPainter

import uuid
from uuid import UUID
from camera import Camera

from imageDetector import ImageDetector

class ObjectTracker(object):
    def __init__(self, painter: AreaPainter, imageDetector: ImageDetector, camera: Camera):
        self.painter = painter
        self._obect_counter = 0
        self._threadMap: Dict[UUID, Thread] = {}
        self._imageDetector = imageDetector
        self._camera = camera
        
    def _process_object_frame(self, template: Type[ndarray[int, dtype[generic]]], uid: UUID, delay: float = None, region: Tuple[int, int, int, int] = None,):
        while uid in self._threadMap:
            frame = self._camera.get_screenshot(region)
            
            if frame is not None:
                # Convert it from BGR(Blue, Green, Red) to
                # RGB(Red, Green, Blue)
                frameMat = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

                imageAreas = self._imageDetector.detectImageAreas(frameMat, template, 0.60, False)

                self.painter.clean_window()

                threads: List[Thread] = []

                # Draws border around the area asynchronously
                for area in imageAreas:            
                    thread = Thread(None, lambda: self.painter.draw_border(area))
                    threads.append(thread)
                    thread.start()       

                for thread in threads:
                    thread.join() 

                time.sleep(delay)
    
    def track_object(self, objectToTrack: Type[ndarray[int, dtype[generic]]], delay: float) -> UUID:
        uid = uuid.uuid4()
        
        thread = Thread(None, lambda: self._process_object_frame(objectToTrack, uid, delay))

        self._threadMap[uid] = thread
        
        thread.start()
        
        return uid

    def stop_tracking(self, uid: UUID) -> bool:
        if (uid not in self._threadMap):
            return False        
        
        thread = self._threadMap.pop(uid)
                
        thread.join()
        
        self.painter.clean_window()
            