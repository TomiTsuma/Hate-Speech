from textblob import TextBlob
from nltk.sentiment.vader import SentimentIntensityAnalyzer
import spacy
import pickle
import gensim
from nltk.stem import WordNetLemmatizer

  
import en_core_web_sm
nlp = en_core_web_sm.load()



def preprocess(text):
    result = []
    for token in gensim.utils.simple_preprocess(text):
        if token not in gensim.parsing.preprocessing.STOPWORDS and len(token) > 3:
            result.append(lemmatize_stemming(token))
    return result
def lemmatize_stemming(text):
    return (WordNetLemmatizer().lemmatize(text, pos='v'))


dictionary = pickle.load(open('Dict.sav', 'rb'))
corpus = pickle.load(open('Corp.sav', 'rb'))
id2word = pickle.load(open('idtoword.sav', 'rb'))
topics = pickle.load(open('topics.sav', 'rb'))



def prepareText(text):
    arr = []
    
    blobed = TextBlob((text))

    score = SentimentIntensityAnalyzer().polarity_scores(text)
    arr.append(score['pos'])
    arr.append(score['neg'])
    arr.append(score['neu'])

    filename = 'Hashtags.sav'
    hashtag_list = pickle.load(open(filename, 'rb'))
    for word in text.split():
        # checking the first character of every word
        if word[0] == '#':
            # adding the word to the hashtag_list
            if word[1:] in hashtag_list:
                arr.append(1)
            else:
                arr.append(0)
                
    
    
    
    
    
    adj_tag_list = ['JJ','JJR','JJS']
    adv_tag_list = ['RB','RBR','RBS']
    adj_count=0
    adv_count=0
    
    for (a,b) in blobed.tags:
        if b in adj_tag_list:
            adj_count+=1               
        elif b in adv_tag_list:
            adv_count+=1
        else:
            pass
    arr.append(adj_count)
    arr.append(adv_count)
    
    
    
    
    
    lda_model = gensim.models.ldamodel.LdaModel(corpus=corpus, num_topics = 10, id2word=id2word, passes=15)

    unseen_document = text
    bow_vector = dictionary.doc2bow(preprocess(unseen_document))
    for index, score in sorted(lda_model[bow_vector], key=lambda tup: -1*tup[1]):
    
        
        if(lda_model.print_topic(index, 5) in topics[4][1]):
            arr.append(score) 
        
        if(lda_model.print_topic(index, 5) in topics[7][1]):
            arr.append(score) 
            
       
            
        if(lda_model.print_topic(index, 5) in topics[9][1]):
            arr.append(score) 
        
        if(lda_model.print_topic(index, 5) in topics[3][1]):
            arr.append(score) 
        
        if(lda_model.print_topic(index, 5) in topics[1][1]):
            arr.append(score) 
            
        if(lda_model.print_topic(index, 5) in  topics[6][1]):
            arr.append(score) 
        
        if(lda_model.print_topic(index, 5) in topics[8][1]):
            arr.append(score) 
        
        if(lda_model.print_topic(index, 5) in topics[0][1]):
            arr.append(score) 
        
        if(lda_model.print_topic(index, 5) in topics[2][1]):
            arr.append(score) 
        
        if(lda_model.print_topic(index, 5) in topics[5][1]):
            arr.append(score) 
    
    
    
    
    distancing = False
    stereotype = False
    
    pronoun_list = ["PRP","PRP$","WP","WP$"]
    tribe_list = ["kikuyu","luo","luyha","luhya","kalenjin","meru","kisii","kuria","kamba","masai","masaai","mijikenda","taita","taveta","swahili"]
    plural = [tribe + "s" for tribe in tribe_list ]
    stereotyping_list = ["all","every","always","never","usually"]

    for (a,b) in blobed.tags:
        if(b in pronoun_list):
            distancing = True
        elif(a in tribe_list):
            distancing = True
        elif(a in plural):
            stereotype = True
        else:
            continue
        for i in stereotyping_list:
            tokens = nlp(i+" "+a)
            if (tokens[0].similarity(tokens[1]))>0.3:
                stereotype == True
    if(distancing == True):
        arr.append(1)
    else:
        arr.append(0)
    # if(stereotype == True):
    #     arr.append(1)
    # else:
    #     arr.append(0)
    print(len(arr))

    return(arr)