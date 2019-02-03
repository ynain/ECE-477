import facenet_recognition

def align(infaces='input_images', aligned='aligned_images'):
    """
        Align faces from one folder to another
    """
    facenet_recognition.align_input(infaces, aligned)

def testAndTrain(aligned='aligned_images', pre_model='./facenet_trials/pretrained/20180402-114759/20180402-114759.pb', my_class='./facenet_trials/myclassifier/my_classifier.pkl', test_classifier_type='svm', weight='./facenet_trials/myclassifier/model_small.yaml'):
    """
        Train & Test Classifier on Images
        After we have aligned images now we can train our classifier.

    aligned ='aligned_images'
    pre_model='./facenet_trials/pretrained/20180402-114759/20180402-114759.pb' #locaiton of pret-trained model from Facenet
    my_class ='./facenet_trials/myclassifier/my_classifier.pkl' #location where we want to save
    test_classifier_type = 'svm' #type of model either svm or nn
    weight= './myclassifier/model_small.yaml' #local stored weights
    """

    facenet_recognition.test_train_classifier(aligned,pre_model,my_class,weight,test_classifier_type,nrof_train_images_per_class=30, seed=102)

def trainClass(aligned='aligned_images', pre_model='./facenet_trials/pretrained/20180402-114759/20180402-114759.pb', my_class='./facenet_trials/myclassifier/my_classifier.pkl', test_classifier_type='svm', weight='./facenet_trials/myclassifier/model_small.yaml'):
    """
        Train Classifer on Images (only Training)
        This API is used to Train our Classifier on Aligned Images

    aligned ='aligned_images'
    pre_model='./facenet_trials/pretrained/20180402-114759/20180402-114759.pb' #locaiton of pret-trained model from Facenet
    my_class ='./facenet_trials/myclassifier/my_classifier.pkl' #location where we want to save
    test_classifier_type = 'svm' #type of model either svm or nn
    weight= './myclassifier/model_small.yaml' #local stored weights
    """

    facenet_recognition.create_classifier(aligned,pre_model,my_class,weight,test_classifier_type)

def testClass(aligned='aligned_images', pre_model='./facenet_trials/pretrained/20180402-114759/20180402-114759.pb', my_class='./facenet_trials/myclassifier/my_classifier.pkl', test_classifier_type='svm', weight='./facenet_trials/myclassifier/model_small.yaml'):
    """
        Test Classifer on Images
        This API is used to test our Trained Classifer

    aligned ='aligned_images'
    pre_model='./facenet_trials/pretrained/20180402-114759/20180402-114759.pb' #locaiton of pret-trained model from Facenet
    my_class ='./facenet_trials/myclassifier/my_classifier.pkl' #location where we want to save
    test_classifier_type = 'svm' #type of model either svm or nn
    weight= './myclassifier/model_small.yaml' #local stored weights
    """

    facenet_recognition.test_classifier(aligned,pre_model,my_class,weight,test_classifier_type)

if __name__ == "__main__":
    testClass(aligned='aligned_images')
    """
    align()
    trainClass(aligned='aligned_images')
    """