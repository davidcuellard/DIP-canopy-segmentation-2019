"""
Pontificia Universidad Javeriana
Departamento de electrónica
TG1907
Objetivo 2: Segmentación Grabcut

@author: David Felipe Cuellar Diaz
"""

# importar paquetes
import cv2
import numpy as np
import segMCS

class segmentacion: 

    def __init__(self,image="image.jpg",folder="",scalefactor=1,resize=False,rgb=True):        
        self.image=image
        self.folder=folder
        self.scalefactor=scalefactor
        self.resize=resize
        self.rgb=rgb
 
        self.refPt = []
        self.draw = 0
        
    #Define las funciones del mouse
    def click_and_crop(self,event, x, y, flags, param):
        #Pinta el cuadrado y lo define
        
        if event == cv2.EVENT_LBUTTONDOWN:
            self.draw = 1
        elif event == cv2.EVENT_LBUTTONUP:
            self.draw = 2
        
        if event == cv2.EVENT_RBUTTONDOWN:
            self.draw = 3
        elif event == cv2.EVENT_RBUTTONUP:
            self.draw = 4

    
        if self.draw == 1:
            if event == cv2.EVENT_MOUSEMOVE:
                cv2.circle(self.imagein,(x, y),2,(0,0,255),-1)
                cv2.circle(self.mask,(x, y),2,0,-1)
                cv2.imshow("input", self.imagein)
                #cv2.imwrite("mask2.png", self.mask)        
        elif self.draw == 3:
            if event == cv2.EVENT_MOUSEMOVE:
                cv2.circle(self.imagein,(x, y),2,(0,255,0),-1)
                cv2.circle(self.mask,(x, y),2,1,-1)
                cv2.imshow("input", self.imagein)
                #cv2.imwrite("mask2.png", self.mask)
    
    def grabcut(self):

	# carga la imagen        
        self.imagein = cv2.imread(self.image)

	# cambia el tamaño de la imagen si es necesario
        if self.resize == True:
            height, width = self.imagein.shape[:2]
            self.imagein = cv2.resize(self.imagein,(int(self.scalefactor*width), int(self.scalefactor*height)), interpolation = cv2.INTER_NEAREST)

	# crea copias de la imagen        
        imagecopy=self.imagein.copy()
        imageout=self.imagein.copy()
        
	# Llama la función segMCS para crear las máscaras de FG y BG
        print("Utilice los sliders para crear la mascara de FG obvio")
        skm=segMCS.segmentacion(image = self.image, folder = self.folder+str(1) ,onlymask=True, scalefactor=self.scalefactor, resize=self.resize)
        
        if self.rgb == True:
            skm.canalrgb()    
        else:
            skm.canalir()
            
        print("Utilice los sliders para crear la mascara de BG obvio")
        skm=segMCS.segmentacion(image=self.image , folder = self.folder + str(0) ,onlymask=True, scalefactor=self.scalefactor, resize=self.resize)
        
        if self.rgb == True:
            skm.canalrgb()    
        else:
            skm.canalir()
        
        # Crea mask FG            
        self.maskin11 = cv2.imread(self.folder + "1mask.bmp")
        self.maskin111 = cv2.cvtColor(self.maskin11, cv2.COLOR_BGR2GRAY)
        self.mask = np.where(self.maskin111>0,1,2).astype('uint8')
        
        # Crea mask BG
        self.maskin00 = cv2.imread(self.folder + "0mask.bmp")
        self.maskin000 = cv2.cvtColor(self.maskin00, cv2.COLOR_BGR2GRAY)
        self.mask = np.where(self.maskin000>0,0,3).astype('uint8')
            

        print("Utilice el click izquierdo para corregir BG obvio")
        print("Utilice el click derecho para corregir FG obvio")
        print("Para ver realizar una iteración, presione c")
        print("Presione la letra q para salir y guardar")            
    
#        GC_BGD    = 0  //!< an obvious background pixels
#        GC_FGD    = 1  //!< an obvious foreground (object) pixel
#        GC_PR_BGD = 2  //!< a possible background pixel
#        GC_PR_FGD = 3   //!< a possible foreground pixel
    
        bgdModel = np.zeros((1,65),np.float64)
        fgdModel = np.zeros((1,65),np.float64)
            
        #Muestra las impagenes de entrada y salida
        cv2.imshow("input", self.imagein)
        cv2.imshow("output", imageout)

        #Empieza el ciclo
        while True:
            key = cv2.waitKey(1) & 0xFF
            #espera que haya movimiento del mouse
            cv2.setMouseCallback("input", self.click_and_crop)
            
            #Realiza los grabcut manuales
            if key == ord("c"):
                cv2.grabCut(imagecopy,self.mask,None,bgdModel,fgdModel,1,cv2.GC_INIT_WITH_MASK)
                print("iteración")
            
            #Modifica la imágen con la máscara
            mask2 = np.where((self.mask==1) + (self.mask==3), 255, 0).astype('uint8')
            
            imageout = cv2.bitwise_and(imagecopy, imagecopy, mask=mask2)   
            
            #Muestra el resultado
            cv2.imshow("output", imageout)
            cv2.imshow("mask", mask2)
            
            #Espera la tecla q para salir
            if key == ord("q"):
                break

        print("Gracias por utilizar Grabcut, en el folder se guardó: ")
        print(" - imagecopy.bmp")
        print(" - imagegc.bmp")
        print(" - mask.bmp")
        print(" - result.bmp")
        
        cv2.imwrite(self.folder + "imagecopy.bmp",imagecopy)
        cv2.imwrite(self.folder + "imagegc.bmp",self.imagein)
        cv2.imwrite(self.folder + "mask.bmp",mask2)
        cv2.imwrite(self.folder + "result.bmp",imageout)
            
        cv2.destroyAllWindows()
