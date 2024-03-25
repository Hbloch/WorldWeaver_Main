from tkinter.messagebox import RETRY
from PIL import Image
import os
import cv2
from cv2 import dnn_superres
from alive_progress import alive_bar

def crop_to_square(image_path, cropped_output_path):
    try:
        with Image.open(image_path) as img:
            # Convertir en RGB si nécessaire
            if img.mode != 'RGB':
                img = img.convert('RGB')

            width, height = img.size
            new_size = min(width, height)

            left = (width - new_size) / 2
            top = (height - new_size) / 2
            right = (width + new_size) / 2
            bottom = (height + new_size) / 2

            img_cropped = img.crop((left, top, right, bottom))
            img_cropped.save(cropped_output_path, format='PNG')  # Sauvegarde au format PNG
        return True
    except Exception as e:
        print(f"Erreur lors du recadrage de l'image {image_path}: {e}")
        return False
    
def resize_image(image_path, output_size=(4033, 4033)):
    try:
        img = cv2.imread(image_path, cv2.IMREAD_UNCHANGED)  # Lire l'image avec tous les canaux
        if img is None:
            raise ValueError(f"L'image {image_path} n'a pas pu être chargée.")

        # Redimensionnement de l'image
        resized_img = cv2.resize(img, output_size)
        cv2.imwrite(image_path, resized_img)
        return True
    except Exception as e:
        print(f"Erreur lors du redimensionnement de l'image {image_path}: {e}")
        return False
    
def upscale_image(input_path, modelpath):
    try:
        img = cv2.imread(input_path)
        if img is None:
            raise ValueError(f"L'image {input_path} n'a pas pu être chargée.")

        # Initialisation du modèle de super-résolution
        sr = dnn_superres.DnnSuperResImpl_create()
        if cv2.cuda.getCudaEnabledDeviceCount() > 0:
            sr.setPreferableBackend(cv2.dnn.DNN_BACKEND_CUDA)
            sr.setPreferableTarget(cv2.dnn.DNN_TARGET_CUDA)
            print("Traitement sur GPU")
        else:
            print("Traitement sur CPU")

        # Lecture et configuration du modèle
        sr.readModel(modelpath)
        sr.setModel("edsr", 4)  # Facteur de mise à l'échelle

        # Mise à l'échelle de l'image
        result = sr.upsample(img)

        # Conversion de l'image en nuances de gris
        gray_result = cv2.cvtColor(result, cv2.COLOR_BGR2GRAY)
        if not resize_image(input_path, gray_result.shape[::-1]):  # Inversion de la forme pour obtenir (largeur, hauteur)
            raise Exception("Erreur lors du redimensionnement de l'image.")

        # Enregistrement de l'image en nuances de gris
        cv2.imwrite(input_path, gray_result)

        return True
    except Exception as e:
        print(f"Erreur lors de l'amélioration de la résolution de l'image {input_path}: {e}")
        return False


    
    
    
folder_path = 'ImagesDownloads'
cropped_folder = 'TraitedImages'
modelpath = "UpscalerModels\EDSR_x4.pb"




if not os.path.exists(cropped_folder):
    os.makedirs(cropped_folder)

total_files = [f for f in os.listdir(folder_path) if f.endswith('.tif')]
with alive_bar(len(total_files), title='Traitement des images') as bar:
    for filename in total_files:
        image_path = os.path.join(folder_path, filename)
        cropped_output_path = os.path.join(cropped_folder, os.path.splitext(filename)[0] + '.png')

        if crop_to_square(image_path, cropped_output_path):
            print(f"Image recadrée : {filename}")
            if upscale_image(cropped_output_path, modelpath):
                print(f"Image améliorée : {filename}")
        bar()

print("Toutes les images ont été recadrées et redimensionnées")
