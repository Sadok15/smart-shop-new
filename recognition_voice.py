import speech_recognition as sr

r = sr.Recognizer()

with sr.Microphone() as source :
    print('Speak : ')
    audio = r.listen(source)

    try :
        text = r.recognize_google(audio)
        print(f"You said this : {text}")

    except:
        print("Sorry Try Again")