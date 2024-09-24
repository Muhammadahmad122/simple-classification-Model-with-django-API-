from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .serializers import FileUploadSerializer
from django.core.files.storage import FileSystemStorage
from keras.models import load_model
import keras
import os
from django.conf import settings
from PIL import Image
import numpy as np
from django.shortcuts import render

# Load your pre-trained model (ensure the model path is correct)
model = load_model(os.path.join(settings.BASE_DIR, 'mlapi', 'model2.h5'))


def upload_file_view(request):
    return render(request, 'upload.html')

@api_view(['GET', 'POST'])
def process_file(request):
    if request.method == 'POST':
        serializer = FileUploadSerializer(data=request.data)
        
        if serializer.is_valid():
            file_uploaded = request.FILES['file_uploaded']  # Retrieve the uploaded file
            fs = FileSystemStorage(location='media/uploads/')  # Save file in 'media/uploads/' directory
            filename = fs.save(file_uploaded.name, file_uploaded)  # Save file
            file_path = fs.path(filename)  # Get the full file path

            # Process the file (assume it's an image)
            img = Image.open(file_path)
            img = img.resize((180, 180)) 
            img_array = keras.utils.img_to_array(img)
            img_array = keras.ops.expand_dims(img_array, 0)
            # img_array = np.array(img) / 255.0  
            # img_array = np.expand_dims(img_array, axis=0)
            print(f"Processed image shape: {img_array.shape}")
  

            
            prediction = model.predict(img_array)
            print(f"Model Prediction Output: {prediction}")
            predicted_class = 'Dog' if prediction[0][0] >= 0.5 else 'Cat'  
            
            return Response({'prediction': predicted_class}, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    
    return Response({"message": "Upload an image to process."})
