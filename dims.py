from textblob import TextBlob
from nltk.sentiment.vader import SentimentIntensityAnalyzer
import en_core_web_sm
nlp = en_core_web_sm.load()
# from allennlp.predictors.predictor import Predictor



# model_url = "C:/Users/tommy/Downloads/coref-spanbert-large-2020.02.27.tar.gz"
# predictor = Predictor.from_path(model_url)  # load the model


distancing = False
devaluing = False
stereotyping = False
passion = False
subjectivity = False





 # resolved text
# Result: "Eva and Martha didn't want Eva and Martha's friend Jenny to feel lonely so Eva and Martha invited their friend Jenny to the party."

def multidimensionality(text):
    
    checkDistancing(text)
    checkStereotyping(text)

    checkDevaluing(text)
    checkSubjectivity(text)
    

    


def checkDistancing(text):
    distancing = False
    # text = (predictor.coref_resolved(text))  # resolved text

    blobed = TextBlob((text))

    pronoun_list = ["PRP","PRP$","WP","WP$"]
    tribe_list = ["kikuyu","luo","luyha","luhya","kalenjin","meru","kisii","kuria","kamba","masai","masaai","mijikenda","taita","taveta","swahili"]
    plural = [tribe + "s" for tribe in tribe_list ]
    stereotyping_list = ["all","every","always","never","usually"]

    for (a,b) in blobed.tags:
        if(b in pronoun_list):
            print(b)
            distancing = True
        elif(a in tribe_list):
            print(a)
            distancing = True
        elif(a in plural):
            print(a)
            distancing = True
        else:
            continue
    print(distancing )

        
    
def checkStereotyping(text):
    # text = (predictor.coref_resolved(text))  # resolved text
    stereotyping = False
    blobed = TextBlob((text))

   
    tribe_list = ["kikuyu","luo","luyha","luhya","kalenjin","meru","kisii","kuria","kamba","masai","masaai","mijikenda","taita","taveta","swahili"]
    plural = [tribe + "s" for tribe in tribe_list ]
    stereotyping_list = ["all","every","always","never","usually"]

    for (a,b) in blobed.tags:

        if(a in plural):
            print(a)
            stereotyping = True
        else:
            continue

        for i in stereotyping_list:
            tokens = nlp(i+""+a)
            if (tokens[0].similarity(tokens[1]))>0.2:
                print(a)
                print(i)
                print(tokens[0].similarity(tokens[1]))
                stereotyping == True
    print(stereotyping )



def checkDevaluing(text):
    # text = (predictor.coref_resolved(text))  # resolved text
    devaluing = False
    blobed = TextBlob((text))
    score = SentimentIntensityAnalyzer().polarity_scores(text)
    if(score['neg']>0.5):
        print(score['neg'])
        devaluing = True
    print(devaluing)

def checkSubjectivity(text):
    # text = (predictor.coref_resolved(text))  # resolved text
    subjectivity = False

    blobed = TextBlob((text))
    adj_tag_list = ['JJ','JJR','JJS']
    adv_tag_list = ['RB','RBR','RBS']
    adj_count=0
    adv_count=0
    
    for (a,b) in blobed.tags:
        if (b in adj_tag_list):
            score = SentimentIntensityAnalyzer().polarity_scores(b)
            if(score['neg']>0.5):
                print(b)
                print(score['neg'])
                adj_count+=1               
        elif b in adv_tag_list:
            score = SentimentIntensityAnalyzer().polarity_scores(b)
            if(score['neg']>0.5):
                print(b)
                print(score['neg'])
                adv_count+=1 
        else: 
            pass

    if(adj_count>0 or adv_count>0):
        subjectivity = True
    print(subjectivity )


    
multidimensionality("Luos are horrible people. They will all burn in hell.")