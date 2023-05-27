
import heapq
from typing import List

import cv2
from cv2 import Mat
import numpy as np

from point import Point
from area import Area

class ImageDetector:
    def _is_overlap(self, a: Area, b: Area) -> bool:
            topLeftA = a.top_left
            topLeftB = b.top_left
            
            bottomRightA = a.bottom_right
            bottomRightB = b.bottom_right
            
            if bottomRightA.x < topLeftB.x or bottomRightB.x < topLeftA.x:
                return False
            
            if bottomRightA.y < topLeftB.y or bottomRightB.y < topLeftA.y:
                return False
            
            return True
    
    def _filterImages(self, imageAreas) -> List[Area]:
        if len(imageAreas) == 0:
            return []        
                        
        areaHeap = []
        for curr in imageAreas:
            heapq.heappush(areaHeap, curr)
        
        uniqueAreasWithMaxConfidence = []
        
        while len(areaHeap) > 0:
            curr: Area = areaHeap.pop()
            # curr = (point, Point(point.x + width, point.y + height, point.confidence))

            if len(uniqueAreasWithMaxConfidence) == 0:
                uniqueAreasWithMaxConfidence.append(curr)
            else:
                last = uniqueAreasWithMaxConfidence[-1]    
                
                if self._is_overlap(last, curr):
                    if last.confidence <= curr.confidence:
                        uniqueAreasWithMaxConfidence[-1] = curr
                else:
                    uniqueAreasWithMaxConfidence.append(curr)
                    
        return uniqueAreasWithMaxConfidence        
        
    
    def detectImageAreas(self, targetImageMat: Mat, templateImageMat: Mat, threshold: float, useColors: bool) -> List[Area]:
        targetMat = targetImageMat.copy()
        templateMat = templateImageMat.copy()

        if useColors:
            targetMat = cv2.cvtColor(targetImageMat, cv2.COLOR_BGR2GRAY)
            templateMat = cv2.cvtColor(templateImageMat, cv2.COLOR_BGR2GRAY)

        normalizedTemplateMat = cv2.normalize(templateMat, None, 0.0, 255.0, cv2.NORM_MINMAX, cv2.CV_32F)
        normalizedTargetMat = cv2.normalize(targetMat, None, 0.0, 255.0, cv2.NORM_MINMAX, cv2.CV_32F)

        # Perform template matching
        resultImagesMat = cv2.matchTemplate(normalizedTargetMat, normalizedTemplateMat, cv2.TM_CCOEFF_NORMED)

        resultPointsMat = np.where(resultImagesMat >= threshold)
        
        imageAreas = []
        
        for pt in zip(*resultPointsMat[::-1]):
            confidence = resultImagesMat[pt[1], pt[0]]

            top_left = Point(pt[0], pt[1])
            bottom_right = Point(pt[0] + templateImageMat.shape[1], pt[1] + templateImageMat.shape[0])
            
            imageAreas.append(Area(top_left, bottom_right, confidence))
        
        filteredImageAreas = self._filterImages(imageAreas)
             
        return filteredImageAreas
    