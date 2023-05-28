from classes.camera import Camera

from imageDetector import ImageDetector
from GUI.areaPainter import AreaPainter
from GUI.interface import Interface

from objectTracker import ObjectTracker

painter = AreaPainter("RenderWindow")
imageDetector = ImageDetector()
camera = Camera()
tracker = ObjectTracker(painter, imageDetector, camera)

interface = Interface(tracker)
interface.run_interface()

tracker.cleanup()