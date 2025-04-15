"""
Pontificia Universidad Javeriana
Departamento de electrónica
TG1907
Objetivo 2: Segmentación Grabcut automático

@author: David Felipe Cuellar Diaz
"""

# importar paquetes
import cv2
import numpy as np
import guidedFilter

class segmentacion: 

    def __init__(self,image="image.jpg",folder="",scalefactor=1,resize=False):        
        self.image=image
        self.folder=folder
        self.scalefactor=scalefactor
        self.resize=resize
 
        self.refPt = []
        self.draw = 0
    
    def grabcut(self):

	# carga la imagen        
        self.imagein = cv2.imread(self.image)

	# cambia el tamaño de la imagen si es necesario
        if self.resize == True:
            height, width = self.imagein.shape[:2]
            self.imagein = cv2.resize(self.imagein,(int(self.scalefactor*width), int(self.scalefactor*height)), interpolation = cv2.INTER_NEAREST)

	# crea una copia de la imagen                
        imagecopy=self.imagein.copy()
        
        # Filtro mediana para eliminar ruido
        median = cv2.medianBlur(self.imagein, 5)
        hsv_median= cv2.cvtColor(median, cv2.COLOR_BGR2HSV)

        #Valores de mask
        #GC_BGD    = 0  //!< an obvious background pixels
        #GC_FGD    = 1  //!< an obvious foreground (object) pixel
        #GC_PR_BGD = 2  //!< a possible background pixel
        #GC_PR_FGD = 3   //!< a possible foreground pixel

        
        # Crea mask FG
        max_green1 = (80,255,255)
        min_green1 = (35,60,60)
            
        mask1 = cv2.inRange(hsv_median, min_green1, max_green1)    
        self.mask = np.where(mask1>0,1,2).astype('uint8')
               
        
        # Crea mask BG
        max_green2 = (25,255,195)
        min_green2 = (0,0,0)
        
        mask0 = cv2.inRange(hsv_median, min_green2, max_green2)
        self.mask = np.where(mask0>0,0,3).astype('uint8')
            
        bgdModel = np.zeros((1,65),np.float64)
        fgdModel = np.zeros((1,65),np.float64)
        
        #Realiza una iteración de Grabcut
        cv2.grabCut(imagecopy,self.mask,None,bgdModel,fgdModel,1,cv2.GC_INIT_WITH_MASK)
            
        #Modifica la imágen con la máscara
        mask2 = np.where((self.mask==1) + (self.mask==3), 255, 0).astype('uint8')
        imageout = cv2.bitwise_and(imagecopy, imagecopy, mask=mask2)       
        
        
        #Guarda las imágenes necesarias de grabcut
        cv2.imwrite(self.folder + "mask1.bmp",mask1)
        cv2.imwrite(self.folder + "mask0.bmp",mask0)        
        cv2.imwrite(self.folder + "imagecopy.bmp",imagecopy)
        cv2.imwrite(self.folder + "mask.bmp",mask2)
        cv2.imwrite(self.folder + "imagegc.bmp",imageout)
        
        #Realiza refinamiento con Guided Filter
        gf=guidedFilter.refinement(imagegf=self.folder + "imagecopy.bmp",maskgf=self.folder + "mask.bmp",imageoutgf=self.folder)
    
        guidedFilter.refinement()   
        gf.guidedFilter()

        #Información en pantalla
        print("Gracias por utilizar Grabcut automático, en el folder se guardó: ")
        print(" - imagecopy.bmp")
        print(" - mask0.bmp")
        print(" - mask1.bmp")
        print(" - mask.bmp")
        print(" - imagegc.bmp")

        cv2.destroyAllWindows()
