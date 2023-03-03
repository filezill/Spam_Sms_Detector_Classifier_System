import nltk
import numpy as np
from pickle import load
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
from flask import Flask, render_template, request, redirect, url_for
import warnings
warnings.filterwarnings('ignore')

rF_model = load(open('model/randomF_classiF.bin', 'rb'))
tfidf_Vec = load(open('model/tfidf_Vec.bin', 'rb'))

app = Flask(__name__)


nltk.download('punkt')
nltk.download('stopwords')

def process_text(text):
  txt = []
  ps = PorterStemmer()  

  for word in nltk.word_tokenize(text.lower()):                             ## Normalizing text - lowercase
    if word.isalnum() and word not in stopwords.words("english"):           ## punc and special symbol and stopwords removal
      word = ps.stem(word)                                                  ## stemming
      txt.append(word)

  return " ".join(txt)

@app.route('/')
def home():
  return render_template('index.html')


@app.route('/detect', methods=["POST"])
def detect():
  usr_sms = str(request.form.get("sms"))
    
  if len(usr_sms) > 0:
    usr_sms = process_text(usr_sms)
    usr_sms_vec = tfidf_Vec.transform(np.array([usr_sms])).toarray()
    output = rF_model.predict(usr_sms_vec)

    output = "Not Spam" if output[0] == 0 else "Spam"

    return render_template('index.html', show_hidden=True, output=output)
  return redirect(url_for('home'))


@app.route('/about')
def about_load():
  return render_template('about.html')
  


@app.route('/contact')
def contact_load():
  return render_template('contact.html')


## Feedback transmission system via mail.. ;)
def feedback_mail(message):
    import smtplib
    from datetime import datetime

    message = message + "\nUTC time: " + datetime.isoformat(datetime.utcnow())
    s = smtplib.SMTP('smtp.gmail.com', 587)
    s.starttls()
    s.login("feedbackspamdetector@gmail.com", "eeyabulgekccdbty")
    s.sendmail("feedbackspamdetector@gmail.com", "deltagon@protonmail.com", message)
    s.quit()


@app.route('/8643edfg597067728dj8', methods=['POST'])
def fetch_feedback():
    name = str(request.form.get('name'))
    email = str(request.form.get('email'))
    message = str(request.form.get('message'))

    if len(name) > 0 or len(email) > 0 or len(message) > 0:
        feedback_mail(f"[Spam Detector Feedback Bot]\nName- {name}\nMail- {email}\nFeedback- {message}")

        return render_template('contact.html', tnx_feedback="Thank you for feedback!")
    return redirect(url_for('contact_load'))


if __name__ == "__main__":
    app.run(debug=True)
