# Hangman
import random


word_list = ['Overlord',
             'SwordArtOnline',
             'MyHeroAcademy',
             'TokyoGhoul',
             'YourAprilLie',
             'Evangelion',
             'SailorMoon',
             'Boruto',
             'DecaDence'
             ]


def get_word():
    word = random.choice(word_list)
    return word.upper()


def play(word):
    word_completion = "_" * len(word)
    guessed = False
    attempts = 6
    guessed_letters = []
    guessed_words = []

    while guessed is False and attempts > 0:
        guess = input("Please guess a letter or word: ").upper()
        if len(guess) == 1 and guess.isalpha():
            if guess in guessed_letters:
                print("You already guessed the letter ", guess)
            elif guess not in word:
                print(guess, "is not in the word.")
                attempts -= 1
                guessed_letters.append(guess)
            else:
                print("Good job,", guess, "is in the word!")
                guessed_letters.append(guess)
                word_as_list = list(word_completion)
                indices = [i for i, letter in enumerate(word) if letter == guess]
                for index in indices:
                    word_as_list[index] = guess
                word_completion = "".join(word_as_list)
                if "_" not in word_completion:
                    guessed = True
        elif len(guess) == len(word) and guess.isalpha():
            if guess in guessed_words:
                print("You already guessed the word ", guess)
            elif guess != word:
                print(guess, "is not the word.")
                attempts -= 1
                guessed_words.append(guess)
            else:
                guessed = True
                word_completion = word
        else:
            print("Wrong input.")
        print(word_completion, '\n')
    if guessed:
        print('Nice! You guessed the word ;)')
    else:
        print('Oh...seems like you lose it ;( The word was ' + word + '. Next time you should try better!')

def main():
    word = get_word()
    play(word)
    while input("Play Again? (Y/N) ").upper() == "Y":
        word = get_word()
        play(word)


main()
