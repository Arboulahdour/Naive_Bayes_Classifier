import os
import io
import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB
from Tkinter import *
from tkMessageBox import *
from tkSimpleDialog import *
import sys
from PIL import ImageTk, Image
import tkFileDialog as filedialog
from tkfilebrowser import *


window = Tk()

window.geometry("0x0")

#showinfo(title="Welcome", message="Openning the spam-filter")
window.geometry("435x326")
window.resizable(0,0)

window.title("Spam-filter")

font15= "-family {DejaVu Sans} -size 20 -weight normal -underline 0 -overstrike 0"

def get_email():
    wid1 = Label(window, width=0, height=0)
    wid1.place(x=0,y=0)
    file_name = filedialog.askopenfile(parent=wid1, title="select file", initialdir='/',
                                      filetypes=[("text files", "*.txt"), ("All files","*")])
    #lines = file_name.read().splitlines()
    lines = file_name.read().split('#', 1)
    return lines

# global variables specify the repertories to our collection data
PATH_TO_HAM_DIR = "/home/ubuntu18/Naive_Bayes_Spam_Classifier/emails/ham"
PATH_TO_SPAM_DIR = "/home/ubuntu18/Naive_Bayes_Spam_Classifier/emails/spam"

SPAM_TYPE = "This email is <SPAM>"
HAM_TYPE = "This email is <not SPAM>"

# X and Y must be with the same size
X = [] # This array repesents input Data (mails)
# Y tells us if there is an email or not
Y = [] # labels useful for training set

def readFilesFromDirectory(path, classification):
    os.chdir(path)
    files_name = os.listdir(path)
    for current_file in files_name:
        message = extract_mail_body(current_file)
        X.append(message)
        Y.append(classification)

#function reads the content of a given file.
#here, we do a little processing to take into account only the "body of the mail".
# We ignore email headers

def extract_mail_body(file_name_str):
    inBody = False
    lines = []
    file_descriptor = io.open(file_name_str,'r', encoding='latin1')
    for line in file_descriptor:
        if inBody:
            lines.append(line)
        elif line == '\n':
            inBody = True
        message = '\n'.join(lines)
    file_descriptor.close()
    return message

#create another function, it will be used by our tkinter application 

def Applique():
    readFilesFromDirectory(PATH_TO_HAM_DIR, HAM_TYPE)
    readFilesFromDirectory(PATH_TO_SPAM_DIR, SPAM_TYPE)
    training_set = pd.DataFrame({'X': X, 'Y': Y})


    #------------------


    vectorizer = CountVectorizer()
    counts = vectorizer.fit_transform(training_set['X'].values)

    classifier = MultinomialNB()
    targets = training_set['Y'].values
    classifier.fit(counts, targets)

    examples = get_email()
    #examples = ['Free products here!!!', "Hi Bob, how about a game of golf tomorrow?"]
    example_counts = vectorizer.transform(examples)
    global predictions 
    predictions = classifier.predict(example_counts)
    #print predictions
    #return predictions

wid = Button(window, text='Load an E-mail..', font=font15, fg="white", height=4, width=22, background="#0070c0", command=Applique)
wid.place(x=16,y=20)

def printR():
    print predictions
    showinfo(title="Result..", message=predictions[0])

wid = Button(window, text='Check', height=4, width=22, font=font15, fg="white", background="#0070c0", command=printR)
wid.place(x=16,y=165)

window.mainloop()
