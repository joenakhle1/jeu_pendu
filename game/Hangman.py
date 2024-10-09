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
    print("Welcome to Hangman!")
    mode = EasyMode()  # Choose the game mode here; can be changed to HardMode()

    while True:
        command = input("Press '+' to add a new word, or any other key to play: ")

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
                        print(f"Good guess! '{user_letter}' is in the word.")
                    else:
                        lives -= 1
                        print(f"Oops! '{user_letter}' is not in the word.")
                elif user_letter in used_letters:
                    print("You have already used that letter. Try again.")
                else:
                    print("Invalid input. Please enter a letter from A-Z.")

            if lives == 0:
                print(f'Sorry, you ran out of lives. The word was "{word}".')
            else:
                print(f'Congratulations! You guessed the word "{word}"!')

# Entry point for the script
if __name__ == '__main__':
    hangman()
