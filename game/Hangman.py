import requests

class GameMode:
    def __init__(self, lives):
        self.lives = lives

    def display_hint(self, word_type):
        return f"Hint: It's a {word_type}."

class EasyMode(GameMode):
    def __init__(self):
        super().__init__(lives=10)  # Plus de vies

    def display_hint(self, word_type):
        return f"Hint (easy mode): It's a {word_type}. You have {self.lives} lives!"

class NormalMode(GameMode):
    def __init__(self):
        super().__init__(lives=6)  # Plus de vies

    def display_hint(self, word_type):
        return f"Hint (normal mode): It's a {word_type}. You have {self.lives} lives!"

class HardMode(GameMode):
    def __init__(self):
        super().__init__(lives=3)  # Moins de vies

    def display_hint(self, word_type):
        return f"Hint (hard mode): It's a {word_type}. Be careful, only {self.lives} lives!"

# Function to fetch a random word and its type from the API
def get_random_word():
    try:
        response = requests.get('http://localhost:5000/random_word')
        response.raise_for_status()
        data = response.json()
        return data['word'], data['type']  # Return both the word and its type
    except requests.exceptions.RequestException as e:
        print(f"Error fetching word from API: {e}")
        return None, None

# Function to add a new word to the database
def add_new_word():
    username = input("Entrer le nom d'utilisateur admin: ")
    password = input("Entrer le mot de passe administrateur: ")
    new_word = input("Entrez le nouveau mot à ajouter: ")
    word_type = input("Saisissez le type de mot (par exemple, fruit, voiture, école), etc.): ")

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
    mode = EasyMode()  # Choose the game mode here; can be changed to HardMode()

    while True:
        command = input("Appuyez sur " + "  pour ajouter un nouveau mot, ou sur n'importe quelle autre touche pour jouer :")

        if command == '+':
            add_new_word()  # Call the function to add a new word
        else:
            word, word_type = get_random_word()  # Fetch both word and type
            if not word:
                return
            word = word.lower()
            word_letters = set(word)
            alphabet = set('abcdefghijklmnopqrstuvwxyz')
            used_letters = set()
            lives = mode.lives  # Set lives based on the chosen mode

            print(f"(Hint: It's a '{word_type}')")  # Display the type as a hint

            while len(word_letters) > 0 and lives > 0:
                print('---------------------------------')
                print(f'You have {lives} lives left.')
                print('Used letters: ' + ' '.join(sorted(used_letters)))
                word_list = [letter if letter in used_letters else '_' for letter in word]
                print('Current word: ' + ' '.join(word_list))

                user_letter = input('Guess a letter: ').lower()
                if user_letter in alphabet - used_letters:
                    used_letters.add(user_letter)
                    if user_letter in word_letters:
                        word_letters.remove(user_letter)
                        print(f"Bien vu ! '{user_letter}' est dans le mot.")
                    else:
                        lives -= 1
                        print(f"Oops! '{user_letter}' n'est pas dans le mot.")
                elif user_letter in used_letters:
                    print("Vous avez déjà utilisé cette lettre. Réessayez.")
                else:
                    print("Entrée invalide. Veuillez saisir une lettre de A à Z.")

            if lives == 0:
                print(f'Désolé, vous navez plus de vies. Le mot était "{word}".')
            else:
                print(f'Félicitations ! Vous avez deviné le mot  "{word}"!')

# Entry point for the script
if __name__ == '__main__':
    hangman()
