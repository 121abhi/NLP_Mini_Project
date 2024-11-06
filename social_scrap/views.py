import pandas as pd
from django.shortcuts import render
from .forms import LinkedInForm
from .linkedin import LinkedInBot
import nltk
from nltk.sentiment import SentimentIntensityAnalyzer

# Initializing Sentiment Intensity Analyzer
sia = SentimentIntensityAnalyzer()

def index(request):
    return render(request, 'social_scrap/index.html')


# https://www.freecodecamp.org/news/how-to-build-a-text-summarizer-using-huggingface-transformers/
# text summarization for the linkedin activity

def analyze_sentiment(text):
    if text is None:
        return {'compound': 0.0}
    sentiment_score = sia.polarity_scores(text)
    return sentiment_score

def analyze_linkedin(request):
    if request.method == 'POST':
        form = LinkedInForm(request.POST)
        if form.is_valid():
            linkedin_url = form.cleaned_data['linkedin_url']

            # initialize linkedinbot and scrape data
            bot = LinkedInBot()
            bot.open_url(linkedin_url)
            linkedin_profile = bot.scrape_data()  # scrape the profile
            experiences_text = bot.scrape_experience()  # scrape the experiences
            education_text = bot.scrape_education()  # scrape the education
            activities_text = bot.scrape_activities()  # scrape the activities
            certifications_text = bot.scrape_certifications()  # scrape the certificates

            # analyze sentiment for different sections of the linkedin profile
            experience_sentiment = analyze_sentiment(experiences_text)
            activities_sentiment = analyze_sentiment(activities_text)
            certifications_sentiment = analyze_sentiment(certifications_text)

            # prepare the context for rendering the analysis
            context = {
                'profile': linkedin_profile,
                'experience': experiences_text,
                'education': education_text,
                'activities': activities_text,
                'certification': certifications_text,
                'experience_sentiment': experience_sentiment['compound'],
                'activities_sentiment': activities_sentiment['compound'],
                'certifications_sentiment': certifications_sentiment['compound'],
            }

            return render(request, 'social_scrap/linkedin_analysis.html', context)

    else:
        # This block handles the GET request
        form = LinkedInForm()  # Initialize the form for the GET request

    # Render the form for GET request or invalid form submission
    return render(request, 'social_scrap/linkedin_form.html', {'form': form})
