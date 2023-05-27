import threading
from typing import Any, Tuple, TypeAlias
import dxcam
from numpy import dtype, generic, ndarray

class Camera(object):
    def __init__(self):
        self._camera = dxcam.create()
        self.lock = threading.Lock()
    
    def start_recording(self, region: Tuple[int, int, int, int] = None, target_fps: int = 60):
        self._camera.start(region, target_fps)
        
    def stop_recording(self):
        self._camera.stop()
    
    def get_latest_frame(self) -> ndarray[Any]:
        return self._camera.get_latest_frame()
    
    def get_screenshot(self, region: Tuple[int, int, int, int] = None) ->  (ndarray[Any, dtype[generic]] | None):
        with self.lock:
            return self._camera.grab(region)