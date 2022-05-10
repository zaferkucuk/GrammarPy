from rich.prompt import Prompt
from rich.console import Console
from random import choice
from words import word_list

SQUARES = {
    'correct_place': '🟩',
    'correct_letter': '🟨',
    'incorrect_letter': '⬛'
}

WELCOME_MESSAGE = f'\n[white on blue] WELCOME TO WORDLE [/]\n'
PLAYER_INSTRUCTIONS = "You may start guessing\n"
GUESS_STATEMENT = "\nEnter your guess"
ALLOWED_GUESSES = 6

def correct_place(letter):
    return f'[black on green]{letter}[/]'


def correct_letter(letter):
    return f'[black on yellow]{letter}[/]'


def incorrect_letter(letter):
    return f'[black on white]{letter}[/]'


def check_guess(guess, answer):
    guessed = []
    wordle_pattern = []
    for i, letter in enumerate(guess):
        if answer[i] == guess[i]:
            guessed += correct_place(letter)
            wordle_pattern.append(SQUARES['correct_place'])
        elif letter in answer:
            guessed += correct_letter(letter)
            wordle_pattern.append(SQUARES['correct_letter'])
        else:
            guessed += incorrect_letter(letter)
            wordle_pattern.append(SQUARES['incorrect_letter'])
    return ''.join(guessed), ''.join(wordle_pattern)


def game(console, chosen_word):
    end_of_game = False
    already_guessed = []
    full_wordle_pattern = []
    all_words_guessed = []

    while not end_of_game:
        guess = Prompt.ask(GUESS_STATEMENT).upper()
        while len(guess) != 5 or guess in already_guessed:
            if guess in already_guessed:
                console.print("[red]You've already guessed this word!!\n[/]")
            else:
                console.print('[red]Please enter a 5-letter word!!\n[/]')
            guess = Prompt.ask(GUESS_STATEMENT).upper()
        already_guessed.append(guess)
        guessed, pattern = check_guess(guess, chosen_word)
        all_words_guessed.append(guessed)
        full_wordle_pattern.append(pattern)

        console.print(*all_words_guessed, sep="\n")
        if guess == chosen_word or len(already_guessed) == ALLOWED_GUESSES:
            end_of_game = True
    if len(already_guessed) == ALLOWED_GUESSES and guess != chosen_word:
        console.print(f"\n[red]WORDLE X/{ALLOWED_GUESSES}[/]")
        console.print(f'\n[green]Correct Word: {chosen_word}[/]')
    else:
        console.print(f"\n[green]WORDLE {len(already_guessed)}/{ALLOWED_GUESSES}[/]\n")
    console.print(*full_wordle_pattern, sep="\n")


if __name__ == '__main__':
    console = Console()
    chosen_word = choice(word_list)
    console.print(WELCOME_MESSAGE)
    console.print(PLAYER_INSTRUCTIONS)
    game(console, chosen_word)




# import random

# words = ['programming', 'tiger', 'lamp', 'television',
# 'laptop', 'water', 'microscope', 'doctor', 'youtube',
# 'projects']

# random_word = random.choice(words)
# st.write(random_word)
# user_guesses = ''
# chances = 10
# while chances > 0:
#     wrong_guesses = 0
#     for character in random_word:
#         if character in user_guesses:
#             st.write(f"Correct guess: {character}")
#             #print(f"Correct guess: {character}")
#         else:
#             wrong_guesses += 1
#             st.write('_')
#             #print('_')
    
#         if wrong_guesses == 0:
#             st.write("Correct.")
#             st.write(f"Word : {random_word}")
#             #print("Correct.")
#             #print(f"Word : {random_word}")
#         break
#     #guess = input('Make a guess: ')
#     guess=st.text_input("make a guess")
#     user_guesses += guess

#     if guess not in random_word:
#         chances -= 1
#         st.write(f"Wrong. You have {chances} more chances")
#         #print(f"Wrong. You have {chances} more chances")

#         if chances == 0:
#             st.write('game over')
#             #print('game over')












# import string 
# import random 


# width = 8
# height = 10 



# def place_word(word, grid):
#     word = random.choice([word, word[::-1]])
    
#     direction = random.choice([[1,0], [0,1], [1,1]])
#     print(f'Placing {word} in direction {direction}...')
#     xstart = width if direction[0] == 0 else width - len(word) - 1
#     ystart = height if direction[1] == 0 else height - len(word) - 1

#     x = random.randrange(0, xstart)
#     y = random.randrange(0, ystart)

#     print([x, y])

#     for c in range(len(word)):
#         grid[x + direction[0]*c][y + direction[1]*c] = word[c]
#     return grid

# grid = [[random.choice(string.ascii_uppercase) for i in range(width)] 
#         for j in range(height)]

# for word in ["HELLO","lotr","NINE","EIGHT"]:
#     place_word(word, grid)



# print("\n".join(map(lambda row: " ".join(row), grid)))

# """Example output:

# Placing OLLEH in direction [1, 1]...
# [0, 3]
# Placing DOOR in direction [0, 1]...
# [0, 3]
# Placing ENIN in direction [1, 0]...
# [0, 0]
# Placing THGIE in direction [1, 1]...
# [1, 2]
# e N L d o o r N\n
# n T t B l J U Q\n
# i Z G h L l D Q\n
# n K S Y g M e D\n
# Q V O I H i C h\n
# K U W H K L e X\n
# A A V M K X W N\n
# G X D Q U E S B\n
# W C G R E P R J\n
# N G P V Q X N W\n
# """


# st.write("\n".join(map(lambda row: " ".join(row), grid)))