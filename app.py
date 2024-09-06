from flask import Flask, request, jsonify, render_template
import random
import pyttsx3
import speech_recognition as sr
import nltk
from nltk import sent_tokenize, word_tokenize, PorterStemmer
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from collections import Counter
import math
import model_answers as mans
import model_questions as mques

app = Flask(__name__)

nltk.download('punkt')
nltk.download('stopwords')

@app.route('/')
def index():
    company = request.args.get('company', 'TechM')
    questions = []
    if company == 'TechM':
        for i in range(len(mques.TechM)):
            questions.append((i + 1, mques.TechM[i]))
    elif company == "ML":
        for i in range(len(mques.ML)):
            questions.append((i + 1, mques.ML[i]))
    elif company == "AWS":
        for i in range(len(mques.AWS)):
            questions.append((i + 1, mques.AWS[i]))
    return render_template('index.html', company=company, questions=questions)


@app.route('/evaluate', methods=['POST'])
def evaluate():
    company = request.form['company']
    l = []
    if company == 'TechM':
        for i in range(len(mques.TechM)):
            l.append(mques.TechM[i])
    elif company == "ML":
        for i in range(len(mques.ML)):
            l.append(mques.ML[i])
    elif company == "AWS":
        for i in range(len(mques.AWS)):
            l.append(mques.AWS[i])
            
    i = 5
    total_sum = 0
    while i > 0:
        myText = random.choice(l)
        SpeakText(myText)
        text = SpeechRecognize()
        total_sum += tokenize(str(text), myText)
        l.remove(myText)
        i -= 1

    final_score = "{:.0f}".format(total_sum / (5 * 3) * 100)
    return render_template('result.html', final_score=final_score)

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
        elif(company=='AWS'):
            Mtext=mans.AWS[key]
        elif(company=='ML'):
            Mtext=mans.ML[key]
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

if __name__ == '__main__':
    app.run(debug=True)
