import random
import pyttsx3
import speech_recognition as sr
import nltk
nltk.download('punkt')
#import nltk
nltk.download('stopwords')
#import nltk
nltk.data.path.append("/path/to/your/nltk_data")

from nltk import sent_tokenize,word_tokenize,PorterStemmer #doc to sent, sent to word, word to root word
from nltk.corpus import wordnet,stopwords #collection of words, general words
from nltk.tokenize import PunktSentenceTokenizer #abbreavited words
from nltk.stem import WordNetLemmatizer  #converting to base word
from nltk.tag import pos_tag #parts of speech
import math,re   #for score calculations
from collections import Counter
import numpy as np
import cv2

import model_answers as mans
import model_questions as mques
print("Enter your required company for an interiew")
company=input()

def tokenize(text,key):
        

        def normalise(word):
            word = word.lower()
            word = ps.stem(word)
            return word


        def get_cosine(vec1, vec2):
             intersection = set(vec1) & set(vec2.keys())
             numerator = sum([vec1[x] * vec2[x] for x in intersection])

             sum1 = sum([vec1[x]**2 for x in vec1.keys()])
             sum2 = sum([vec2[x]**2 for x in vec2.keys()])
             denominator = math.sqrt(sum1) * math.sqrt(sum2)

             if not denominator:
                return 0.0
             else:
                return numerator / denominator


        def text_to_vector(text):
             words = word_tokenize(text)
             vec=[]
             for word in words:
                 if(word not in stop_words):
                     if(word not in special):
                         w=normalise(word);
                         vec.append(w);
             #print Counter(vec)
             return Counter(vec)



        def docu_to_vector(sent):
             vec=[]
             for text in sent:
                 words = word_tokenize(text)
                 for word in words:
                     if(word not in stop_words):
                         if(word not in special):
                             w=normalise(word);
                             vec.append(w);
             #print Counter(vec)
             return Counter(vec)


        def f_s_to_s(sent):
            cosine_mat=np.zeros(N+1)
           
            row=0
            for text in sentences:
                maxi=0
                vector1 = text_to_vector(text)
                for text1 in sent:
                    vector2 = text_to_vector(text1)
                    cosine = get_cosine(vector1, vector2)
                    if(maxi<cosine):
                        maxi=cosine
                        
                cosine_mat[row]=maxi
                     
                row+=1
                
            return cosine_mat
        if(company=='TechM'):
            Mtext=mans.TechM[key]
        elif(company=='IBM'):
            Mtext=mans.IBM[key]
        elif(company=='HCL'):
            Mtext=mans.HCL[key]
        elif(company=='Infosys'):
            Mtext=mans.Infosys[key]
        elif(company=='Wipro'):
            Mtext=mans.Wipro[key]
        elif(company=='Amazon'):
            Mtext=mans.Amazon[key]
        elif(company=='Apple'):
            Mtext=mans.Apple[key]
        elif(company=='Capgemini'):
            Mtext=mans.Capgemini[key]
        elif(company=='Cognizant'):
            Mtext=mans.Cognizant[key]
        elif(company=='Deloitte'):
            Mtext=mans.Deloitte[key]
        elif(company=='Google'):
            Mtext=mans.Google[key]
        elif(company=='Microsoft'):
            Mtext=mans.Microsoft[key]
        elif(company=='AWS'):
            Mtext=mans.AWS[key]
        elif(company=='AI'):
            Mtext=mans.AI[key]
        elif(company=='Front_End'):
            Mtext=mans.Front_End[key]
        elif(company=='Deveops'):
            Mtext=mans.Deveops[key]
        elif(company=='Cyber_Security'):
            Mtext=mans.Cyber_Security[key]
        elif(company=='ML'):
            Mtext=mans.ML[key]
        else:
            Mtext=mans.ans[key]
        print(Mtext)
        sentences=sent_tokenize(Mtext)   #model answer
        sentences1=sent_tokenize(text)   #received answer
        N=len(sentences)
        N1=len(sentences1)

        ps=PorterStemmer()
        lemmatizer=WordNetLemmatizer()
        stop_words=stopwords.words('english')
        special=['.',',','\'','"','-','/','*','+','=','!','@','$','%','^','&','``','\'\'','We','The','This','is','a','A','and']

        sent = sentences1
        max_mark=3
        mat = f_s_to_s(sentences1)

        cnt = docu_to_vector(sent)
        try:
                cnt = cnt.most_common(5)

                thematic=[]
                thematic.append(cnt[0][0])
        except:
                pass
                
        #for i in range(10):
        #        thematic.append(cnt[i][0])

        sum1=0

        thematic = ",".join(str(x) for x in thematic)
        thematic = text_to_vector(thematic)
        for i in sentences1:
                i = text_to_vector(i)
                sum1=sum1+ get_cosine(thematic,i)
        

        point1= sum(mat)
        score1=point1*  max_mark*3/(4*N)
        if score1>1.5 and score1<2:
                score1=2.5
        print(score1)
        return score1

        

    

def SpeakText(command):
	engine = pyttsx3.init()
	engine.say(command)
	engine.runAndWait()

def SpeechRecognize():
        r = sr.Recognizer()
        with sr.Microphone() as source:
                r.adjust_for_ambient_noise(source,duration=0.5)
                print("Tell your answer :")
                r.pause_threshold=1
                audio = r.listen(source)
                
                text=""
                try:
                        text = r.recognize_google(audio,language='en-in')
                        print(text)
                        return text

                except:
                    myText="Sorry could not recognize what you said"
                    print("Sorry could not recognize what you said")
                    SpeakText(myText)
                    SpeechRecognize()
        

#l=["what is oops","What is polymorphism?","Why is python trending","What are your hobbies","Tell me your strengths","Tell me your weeknesses","Which programming language you are good with"]
#l1=["that's great","Good to hear that","That's Nice","You rocked it"]
#myText = input()

l=[]
# for i in range(len(mques.TechM)):
#     l.append(mques.TechM[i])
if(company=='TechM'):
    for i in range(len(mques.TechM)):
        l.append(mques.TechM[i])
elif(company=="IBM"):
    for i in range(len(mques.IBM)):
        l.append(mques.IBM[i])
elif(company=="HCL"):
    for i in range(len(mques.HCL)):
        l.append(mques.HCL[i])
elif(company=="Infosys"):
    for i in range(len(mques.Infosys)):
        l.append(mques.Infosys[i])
elif(company=="Wipro"):
    for i in range(len(mques.Wipro)):
        l.append(mques.Wipro[i])
elif(company=="Amazon"):
    for i in range(len(mques.Amazon)):
        l.append(mques.Amazon[i])
elif(company=="Apple"):
    for i in range(len(mques.Apple)):
        l.append(mques.Apple[i])
elif(company=="Capgemini"):
    for i in range(len(mques.Capgemini)):
        l.append(mques.Capgemini[i])
elif(company=="Cognizant"):
    for i in range(len(mques.Cognizant)):
        l.append(mques.Cognizant[i])
elif(company=="Deloitte"):
    for i in range(len(mques.Deloitte)):
        l.append(mques.Deloitte[i])
elif(company=="Google"):
    for i in range(len(mques.Google)):
        l.append(mques.Google[i])
elif(company=="Microsoft"):
    for i in range(len(mques.Microsoft)):
        l.append(mques.Microsoft[i])
elif(company=="AWS"):
    for i in range(len(mques.AWS)):
        l.append(mques.AWS[i])
elif(company=="AI"):
    for i in range(len(mques.AI)):
        l.append(mques.AI[i])
elif(company=="Front_End"):
    for i in range(len(mques.Front_End)):
        l.append(mques.Front_End[i])
elif(company=="Deveops"):
    for i in range(len(mques.Deveops)):
        l.append(mques.Deveops[i])
elif(company=="Cyber_Security"):
    for i in range(len(mques.Cyber_Security)):
        l.append(mques.Cyber_Security[i])
elif(company=="ML"):
    for i in range(len(mques.ML)):
        l.append(mques.ML[i])
else:
    for i in range(len(mques.l)):
        l.append(mques.l[i])
i=5	
j=i
total_sum=0
while(i>0):
    myText = random.choice(l)
   
    print(myText)
    SpeakText(myText)
    text=SpeechRecognize()  #recorded answer
    total_sum+=tokenize(str(text),myText)
    l.remove(myText)
    i=i-1
    print(total_sum)





print("Final Score is ",end="")
print("{:.0f}".format(total_sum/(j*3)*100),"%")

