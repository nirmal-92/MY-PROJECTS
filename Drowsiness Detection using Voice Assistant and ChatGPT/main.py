import openai
import speech_recognition as sr
import pyttsx3
import os
import json
import tkinter as tk
# OpenAI configuration
openai.api_key = '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'
personality = "p.txt"
with open(personality, "r") as file:
    mode = file.read()
messages = [{"role": "system", "content": f"{mode}"}]

# pyttsx3 setup
engine = pyttsx3.init()
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[1].id)  # 0 for male, 1 for female

# Speech recognition setup
r = sr.Recognizer()
mic = sr.Microphone(device_index=0)
r.dynamic_energy_threshold = False
r.energy_threshold = 400
usewhisper = False


def whisper(audio):
    with open('speech.wav', 'wb') as f:
        f.write(audio.get_wav_data())
    speech = open('speech.wav', 'rb')
    wcompletion = openai.Audio.transcribe(
        model="whisper-1",
        file=speech
    )
    print(wcompletion)
    user_input = wcompletion['text']
    print(user_input)
    return user_input


def save_conversation(save_foldername):
    os.makedirs(save_foldername, exist_ok=True)

    base_filename = 'conversation'
    suffix = 0
    filename = os.path.join(save_foldername, f'{base_filename}_{suffix}.txt')

    while os.path.exists(filename):
        suffix += 1
        filename = os.path.join(save_foldername, f'{base_filename}_{suffix}.txt')

    with open(filename, 'w') as file:
        json.dump(messages, file, indent=4)

    return suffix


def save_inprogress(suffix, save_foldername):
    os.makedirs(save_foldername, exist_ok=True)
    base_filename = 'conversation'
    filename = os.path.join(save_foldername, f'{base_filename}_{suffix}.txt')

    with open(filename, 'w') as file:
        json.dump(messages, file, indent=4)


# Main execution
script_dir = os.path.dirname(os.path.abspath(_file_))
foldername = "voice_assistant"
save_foldername = os.path.join(script_dir, f"conversations/{foldername}")
suffix = save_conversation(save_foldername)


def loop():

    while True:
        with mic as source:
            print("\nListening...")
            r.adjust_for_ambient_noise(source, duration=0.5)
            audio = r.listen(source)
            try:
                if usewhisper:
                    user_input = whisper(audio)
                else:
                    user_input = r.recognize_google(audio)
                print("Recognized:", user_input)
            except sr.UnknownValueError:
                print("Could not understand audio")
                continue
            except sr.RequestError:
                print("Could not request results from the speech recognition service. Check your internet connection.")
                continue

        messages.append({"role": "user", "content": user_input})

        completion = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=messages,
            temperature=0.8,
            max_tokens=50
        )

        response = completion.choices[0].message.content
        messages.append({"role": "assistant", "content": response})
        print(f"\nAssistant: {response}\n")
        save_inprogress(suffix, save_foldername)

        engine.say(response)
        engine.runAndWait()

        if 'exit' in user_input.lower():
            break


def main():

    window = tk.Tk()
    window.configure(bg="#FFFF34")
    label = tk.Label(window, text="DROWSINESS DETECTOR")
    label.pack(pady=30)
    label.config(font=("Arial", 40, "bold"))

    b = tk.Button(window, text='listen', command=loop, fg='blue', bg='white')
    a = window.title("DROWSINESS DETECTOR")
    b.pack(side="left")
    b.place(x=50, y=50)
    b.pack(anchor="center")
    '''b.grid(row=100,column=200)'''
    window.mainloop()


main()
