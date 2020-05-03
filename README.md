# Distance-Estimator
## Introduction
We created this project aiming to achieve an AI model capable to estimate the distance of defined objects.
This guide provides instructions for realising this as well as using the trained models.
ps: as a starter the object we worked with for now is faces.
## 1.How to use the trained models:
We provided a script to test the models in a real-time camera feed.
###Install requirements 

```
pip3 install -r using-requirements.txt
pip3 install -U scikit-learn
```
###Run the script
The *Running-Model* folder contains the trained MLP regression model as *MLP_model.h5* and the SVM regression model *Final_estimator.pickle* also the ML model for face detection.
```
cd Running-Model
python3 distance_estimator.py
```

## Acknowledgement
This project was realised by Mohamed Chebbi and Fedi Abdelaoui, supervised by Lilia Ennouri as part of the Engineering Department of Data Co-Lab
