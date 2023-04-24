# coding=utf8
import sys
from daciuk import MinDict, display_automaton
import pickle


def print_choices():
    print("Was möchstest du tun?\n\n"
          "(1) Wort abfragen\n"
          "(2) Sprache abfragen\n"
          "(3) Automaten zeichnen\n"
          "(4) Automaten speichern und anzeigen\n"
          "(5) Tarjan Tabelle erstellen, anzeigen und speichern\n"
          "(6) Tarjan Tabelle laden und anzeigen\n"
          "(7) oder leeres String: Exit\n")


if __name__ == '__main__':
    print("*" * 70)
    print("Daciuk-Algorithmus zur Konstruktion eines minimalen Lexikonautomaten")
    print("*" * 70 + "\n")

    print("Automat erstellen")
    print("(1) Einen minimalen Automat aus einer Wortliste erstellen")
    print("(2) Einen gespeicherten Automat laden")
    user_input = input("Bitte eine Nummer eingeben: ")

    success = False
    ask = True

    wordlist = []

    if user_input == '1':
        while not success:
            filepath = input("Bitte den Dateinamen eingeben: ")
            try:
                with open(filepath, "r") as file:
                    print(f"Die Datei {filepath} hat den folgenden Inhalt...\n")
                    for line in file:
                        word = line.strip()
                        print(f"\t {word}", end="\n")
                        wordlist.append(word)
                success = True
                print("Der Automat wird mit diesen Wörtern erstellt.")
            except FileNotFoundError as error:
                print(error)

        min_dict = MinDict.from_wordlist(wordlist)  # Instantiate a minimal dictionary.
        min_dict.compute_language()

    elif user_input == '2':
        # Load the saved automaton
        while not success:
            print("Der abgespeicherte Automaten wird geladen...\n")
            automat_path = input("Bitte den Dateinamen eingeben: ")
            min_dict = MinDict.from_pickle(automat_path)
            print(min_dict.language)
            success = True
    else:
        print("Die Eingabe ist ungultig.")
        sys.exit()

    while ask:
        print("---" * 10)
        print_choices()
        answer = input("Bitte eine Nummer eingeben: ")
        if answer == '1':
            # (1) Wort abfragen
            word_to_check = input("Bitte ein Wort eingeben: ")
            if word_to_check in min_dict.language:
                print(f"Ja, das Wort '{word_to_check}' ist Teil der Sprache des Automaten.")
            else:
                print(f"Nein, das Wort '{word_to_check}' ist NICHT Teil der Sprache des Automaten.")

        elif answer == '2':
            # (2) Sprache abfragen
            print("Wortliste: ", min_dict.word_list)
            print("Sprache des Automaten: ", min_dict.language)

        elif answer == '3':
            # (3) Automaten zeichnen
            print("Der Automaten wird gezeichnet...")
            display_automaton(min_dict)

        elif answer == '4':
            # (4) Automaten speichern
            print("Der Automaten wird gespeichert...")
            out_path = "automat.pkl"
            min_dict.save_automat_to_pkl(file_name=out_path)
            print("=====================Min DEA===================")
            print(f"Sprache: {min_dict.language} \n")
            print(f"Übergangfunktionen \n")
            for state, targets in min_dict.tr.items():
                for label, target_state in targets.items():
                    print(state, "  ", label, "  ", target_state)
            print(f"Der Automaten wurde als '{out_path}' gespeichert.")

        elif answer == '5':
            # (5) Eine Tarjan Tabelle erstellen und speichern
            print("Tarjan Tabelle wird erstellt...")
            print("Wörter: ", min_dict.word_list)
            if min_dict.tarjan == [(), ()]:
                min_dict = MinDict.from_wordlist(min_dict.word_list)
            min_dict.print_tarjan()

            print(f"Startpunkt(e) der Tarjan-Tabelle", min_dict.tarjan_start)

            data_to_save = (min_dict.tarjan, min_dict.tarjan_start, min_dict.word_list)
            file_name = "tarjan.pkl"
            min_dict.save_pkl_file(data_to_save, file_name)
            print(f"Die Tarjan-Tabelle wurde als '{file_name}' gespeichert.")

        elif answer == '6':
            # (6) Tarjan Tabelle laden
            file_name = input("Pickle Datei von der gespeicherte Tarjan Tabelle eingeben: ")
            try:
                min_dict.load_tarjan_file(file_name)
                print(f"Die Tarjan-Tabelle aus {file_name} wird geladen...")
                print("Wortliste: ", min_dict.word_list)
                min_dict.print_tarjan()
                print(f"Die Startpunkt(e) der Tarjan-Tabelle sind: ", min_dict.tarjan_start)
            except FileNotFoundError as err:
                print(err)

        elif answer == "":
            print("Bis dann!")
            sys.exit()
        elif answer == "7":
            # (7) Exit
            ask = False
            print("Bis dann!")
            sys.exit()
        else:
            print("Eingabe ungültig. Bitte nochmal versuchen.\n")
            ask = True
