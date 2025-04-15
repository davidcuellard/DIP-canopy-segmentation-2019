"""
Pontificia Universidad Javeriana
Departamento de electrónica
TG1907
Objetivo 2: Refinamiento Guided filter

@author: David Felipe Cuellar Diaz
"""

import cv2

class refinement:
    
    def __init__(self,channel="rgb",imagegf="imageguide.bmp",maskgf="mask.bmp",imageoutgf="cfimage.bmp"):
        self.channel=channel
        if channel=="rgb":
            self.radius=60
            self.eps=0.000001
        if channel=="ir":
            self.radius=50
            self.eps=0.001
        self.imagegf=imagegf
        self.maskgf=maskgf
        self.imageoutgf=imageoutgf
            
    def guidedFilter(self):

        
        imageguide=cv2.imread(self.imagegf)
        maskguide=cv2.imread(self.maskgf,0)
        
        #Guided filter
        guided=cv2.ximgproc.guidedFilter(guide=imageguide, src=maskguide, radius=self.radius, eps=self.eps, dDepth=-1)
        
        #Umbralización por Otsu
        ret2,thotsu = cv2.threshold(guided,0,255,cv2.THRESH_BINARY+cv2.THRESH_OTSU)
        resultg = cv2.bitwise_and(imageguide, imageguide, mask=thotsu)
        
        #Guarda las imágenes necesarias de Guided Filter
        cv2.imwrite(self.imageoutgf + 'imagegf.bmp', resultg)
        cv2.imwrite(self.imageoutgf + 'maskotsu.bmp', thotsu)
        cv2.imwrite(self.imageoutgf + 'maskgf.bmp', guided)
        
        #Información en pantalla
        print("Gracias por utilizar Grabcut estándar, en el folder se guardó: ")
        print(" - maskotsu.bmp")
        print(" - imagegf.bmp")
        print(" - maskgf.bmp")

        #cv2.waitKey(0)
        cv2.destroyAllWindows()    
        
    
