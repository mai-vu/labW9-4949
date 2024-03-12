from django.shortcuts import render, HttpResponseRedirect
from django.http import Http404
from django.urls import reverse
from django.views.generic import TemplateView

def homePageView(request):
    return render(request, 'home.html', {
        'mynumbers': [1, 2, 3, 4, 5, 6, ],
        'firstName': 'Mai',
        'lastName': 'Vu'})

def aboutPageView(request):
    # return request object and specify page.
    return render(request, 'about.html')

def maiPageView(request):
    return render(request, 'mai.html')


def homePost(request):
    # Create variable to store choice that is recognized through entire function.
    choice = -999
    gmat = -999  # Initialize gmat variable.

    try:
        # Extract value from request object by control name.
        currentChoice = request.POST['choice']
        gmatStr = request.POST['gmat']

        # Crude debugging effort.
        print("*** Years work experience: " + str(currentChoice))
        choice = int(currentChoice)
        gmat = float(gmatStr)

    # Enters 'except' block if integer cannot be created.
    except:
        return render(request, 'home.html', {
            'errorMessage': '*** The choice was missing please try again',
            'mynumbers': [1, 2, 3, 4, 5, 6, ]})
    else:
        # Always return an HttpResponseRedirect after successfully dealing
        # with POST data. This prevents data from being posted twice if a
        # user hits the Back button.
        return HttpResponseRedirect(reverse('results', kwargs={'choice':choice,'gmat':gmat},))


import pickle
import pandas as pd
import os

def results(request, choice, gmat):
    print("*** Inside reults()")
    # load saved model
    # Get the current working directory
    base_dir = os.path.dirname(os.path.abspath(__file__))
    # Navigate to the parent directory
    parent_dir = os.path.dirname(base_dir)

    # Construct the path to the pickle file relative to the parent directory
    pickle_file_path = os.path.join(parent_dir, 'model_pkl')
    with open(pickle_file_path, 'rb') as f:
        loadedModel = pickle.load(f)

    # Create a single prediction.
    singleSampleDf = pd.DataFrame(columns=['gmat', 'work_experience'])

    workExperience = float(choice)
    print("*** GMAT Score: " + str(gmat))
    print("*** Years experience: " + str(workExperience))
    singleSampleDf = singleSampleDf._append({'gmat': gmat,
                                             'work_experience': workExperience},
                                            ignore_index=True)

    singlePrediction = loadedModel.predict(singleSampleDf)

    print("Single prediction: " + str(singlePrediction))

    return render(request, 'results.html', {'choice': workExperience, 'gmat': gmat,
                                            'prediction': singlePrediction})





