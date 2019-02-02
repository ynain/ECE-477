import facenet_recognition
print(facenet_recognition.align_input('input_images','aligned_images'))

"""
    Train & Test Classifier on Images
    After we have aligned images now we can train our classifier.
"""

pre_model='./pretrained/20180402-114759/20180402-114759.pb' #locaiton of pret-trained model from Facenet
my_class ='./myclassifier/my_classifier.pkl' #location where we want to save
test_classifier_type = 'svm' #type of model either svm or nn
weight = './myclassifier/model_small.yaml' #local stored weights

facenet_recognition.test_train_classifier('aligned_images',pre_model,my_class,weight,test_classifier_type,nrof_train_images_per_class=30, seed=102)

"""
    Train Classifer on Images(only Training)
    This API is used to Train our Classifier on Aligned Images
"""

pre_model='./pretrained/20180402-114759/20180402-114759.pb' #locaiton of pret-trained model from Facenet
my_class ='./myclassifier/my_classifier.pkl' #location where we want to save
test_classifier_type = 'nn' #type of model either svm or nn
weight= './myclassifier/model_small.yaml' #local stored weights

facenet_recognition.create_classifier('aligned_images',pre_model,my_class,weight,test_classifier_type)

"""
    Test Classifer on Images
    This API is used to test our Trained Classifer
"""

pre_model='./pretrained/20180402-114759/20180402-114759.pb' #locaiton of pret-trained model from Facenet
my_class ='./myclassifier/my_classifier.pkl' #location where we want to save
test_classifier_type = 'nn' #type of model either svm or nn
weight= './myclassifier/model_small.yaml' #local stored weights

facenet_recognition.test_classifier('aligned_images',pre_model,my_class,weight,test_classifier_type)