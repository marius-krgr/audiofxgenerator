import scipy.io.wavfile as wavfile
from scipy import signal
import os
import sys

def audioConvolution(rateInput, rateEffect, dataInput, dataEffect):
    print("Deine Analyse beginnt...")

    try:
        assert (rateInput == rateEffect)
    except AssertionError:
        print("Fehler: Die Samplerates stimmen nicht überein!")
        sys.exit(1)

    dataInput = dataInput.mean(axis=1) if len(dataInput.shape) > 1 else dataInput
    dataEffect = dataEffect.mean(axis=1) if len(dataEffect.shape) > 1 else dataEffect

    dataOutput = signal.fftconvolve(dataInput, dataEffect)

    dataOutput /= max(abs(dataOutput))
    dataOutput *= (2 ** 15 - 1)
    dataOutput = dataOutput.astype('int16')
    return dataOutput

def genOutput(dataOutput, rateInput):
    answer = input("Bitte gib einen Namen für die Ausgabedatei ein: ")
    answer = answer + ".wav"
    filepath = os.path.join("export/", answer)
    wavfile.write(filepath, rateInput, dataOutput)
    print("Faltung abgeschlossen.")
    print("Danke für dein Vertrauen in unser super duper tolles und seriöses Programm und bis zum nächsten mal! :)")


def fileImport(filename, folder):
    filepath = os.path.join(folder, filename)
    rate, data = wavfile.read(filepath)
    return rate, data

def analyse(rate, data, filename):
    N1 = data.shape[0]
    CHN1 = data.shape[1] if len(data.shape) > 2 else 1
    print(f"Hier ein paar Daten zu deiner Datei {filename}.")
    print(f"Audiofile {filename}: {N1} samples, {CHN1} channels, {rate} Hz, Duration {N1/rate:.3f}s")
    print(data[:4])

def welcome():
    print("Willkommen zu Deinem persönlichen Raumakustiksimulationsassistenten. :)")

def queryInput():
    print("Bitte lege deine Audiodatei im Ordner 'Import' ab.")
    input("Um weiterzugehen, drücke Enter.")

    while True:
        answer = input("Wie heißt die Datei, die du verwenden möchtest?\nEingabe: ")
        if not answer.lower().endswith(".wav"):
            answer += ".wav"
        path = os.path.join("Import", answer)

        if os.path.isfile(path):
            return answer
        else:
            print(f"ACHTUNG: Datei '{answer}' wurde nicht gefunden!")
            print("Bitte stelle sicher, dass die Datei im Ordner 'Import' liegt und überprüfe deine Schreibweise.\n")

def queryEffect():
    answer = input("Bitte wähle deinen Effekt aus.\n 1 für 'Big-Hall-Effekt'\n 2 für 'Classroom-Effekt'\nEingabe: ")
    if answer == "1":
        return "big_hall.wav"
    elif answer == "2":
        return "classroom.wav"
    else:
        print("Ungültige Eingabe. Bitte 1 oder 2 eingeben.")
        queryEffect()
        return()





def main():
    welcome()
    audioinput = queryInput()
    audioeffekt = queryEffect()
    rateInput, dataInput = fileImport(audioinput, "import/")
    rateEffect, dataEffect = fileImport(audioeffekt, "effect/")
    analyse(rateInput, dataInput, audioinput)
    analyse(rateEffect, dataEffect, audioeffekt)
    dataOutput = audioConvolution(rateInput, rateEffect, dataInput, dataEffect)
    genOutput(dataOutput, rateEffect)

if __name__ == "__main__":
    main()