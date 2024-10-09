import requests

class ModeDeJeu:
    def __init__(self, vies):
        self.vies = vies

    def display_Indice(self, type_de_mot):
        return f"Indice: It's a {type_de_mot}."

class ModeFacile(ModeDeJeu):
    def __init__(self):
        super().__init__(vies=10)  # Plus de vies

    def display_Indice(self, type_de_mot):
        return f"Indice (mode facile): Le type est {type_de_mot}. Vous avez {self.vies} vies!"

class ModeNormal(ModeDeJeu):
    def __init__(self):
        super().__init__(vies=6)  # Nombre de vies normal

    def display_Indice(self, type_de_mot):
        return f"Indice (mode normal): Le type est {type_de_mot}. Vous avez {self.vies} vies!"

class ModeDificile(ModeDeJeu):
    def __init__(self):
        super().__init__(vies=3)  # Moins de vies

    def display_Indice(self, type_de_mot):
        return f"Indice (mode dificile): Le type est {type_de_mot}. Attention, Vouz avez seulement {self.vies} vies!"

# Fonction pour récupérer un mot random et son type depuis l'API
def obtenir_mot_random():
    try:
        response = requests.get('http://localhost:5000/random_word')
        response.raise_for_status()
        data = response.json()
        return data['word'], data['type']  # Renvoie à la fois le mot et son type
    except requests.exceptions.RequestException as e:
        print(f"Erreur lors de la récupération du mot depuis l'API: {e}")
        return None, None

# Fonction pour ajouter un nouveau mot à la base de données avec son type depuis l'API
def add_new_word():
    username = input("Enter admin username: ")
    password = input("Enter admin password: ")
    new_word = input("Enter the new word to add: ")
    word_type = input("Enter the word type (e.g., fruit, car, school, etc.): ")

    try:
        response = requests.post('http://localhost:5000/add_word', json={
            'username': username,
            'password': password,
            'word': new_word,
            'type': word_type
        })
        response.raise_for_status()
        data = response.json()

        if 'error' in data:
            print(f"Error: {data['error']}")
        else:
            print(data['message'])

    except requests.exceptions.RequestException as e:
        print(f"Error adding word to the API: {e}")

# Main Hangman game logic
def hangman():
    print("Bienvenue à Hangman !")
    mode = ModeFacile()  # Choisissez le mode de jeu ici ; peut être changé en ModeNormal() ou ModeDificile()

    while True:
        command = input("Appuyez sur + pour ajouter un nouveau mot, ou sur n'importe quelle autre touche pour jouer :")

        if command == '+':
            add_new_word()  # Appelez la fonction pour ajouter un nouveau mot
        else:
            word, type_de_mot = obtenir_mot_random()  # Récupérer à la fois le mot et le type
            if not word:
                return
            word = word.lower()
            word_letters = set(word)
            alphabet = set('abcdefghijklmnopqrstuvwxyz')
            used_letters = set()
            vies = mode.vies  # Définir les vies en fonction du mode choisi

            print(f"(Indice: Le type est '{type_de_mot}')")  # Afficher le type comme indice

            while len(word_letters) > 0 and vies > 0:
                print('---------------------------------')
                print(f'Vous avez {vies} vies encore.')
                print('Lettres utilisées: ' + ' '.join(sorted(used_letters)))
                word_list = [letter if letter in used_letters else '_' for letter in word]
                print('Mot actuel: ' + ' '.join(word_list))

                user_letter = input('Devinez une lettre: ').lower()
                if user_letter in alphabet - used_letters:
                    used_letters.add(user_letter)
                    if user_letter in word_letters:
                        word_letters.remove(user_letter)
                        print(f"Bien vu ! '{user_letter}' est dans le mot.")
                    else:
                        vies -= 1
                        print(f"Oops! '{user_letter}' n'est pas dans le mot.")
                elif user_letter in used_letters:
                    print("Vous avez déjà utilisé cette lettre. Réessayez.")
                else:
                    print("Entrée invalide. Veuillez saisir une lettre de A à Z.")

            if vies == 0:
                print(f'Désolé, vous navez plus de vies. Le mot était "{word}".')
            else:
                print(f'Félicitations ! Vous avez deviné le mot  "{word}"!')

# Entry point for the script
if __name__ == '__main__':
    hangman()
