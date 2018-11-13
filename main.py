#!/usr/bin/env python
import argparse
import random
import tempfile

import gtts
import gtts.lang
import numpy as np
import vlc

DEFAULT_ALPHABET = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
DEFAULT_END_NUMBER = 99
DEFAULT_LANG = 'en'
DEFAULT_LENGTH = 5
DEFAULT_START_NUMBER = 0


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Game to practice acronyms spelling by listening and writing.")
    parser.add_argument('--add-number', action='store_true',
                        help="adds a number sampled from [start-number, end-number] to some part of the acronym")
    parser.add_argument('--alphabet', default=DEFAULT_ALPHABET,
                        help="alphabet to use for the random sampling (default: English alphabet)")
    parser.add_argument('--end-number', default=DEFAULT_START_NUMBER, type=int,
                        help=f"highest number to sample, if --add-number is used (default: {DEFAULT_END_NUMBER})")
    parser.add_argument('--lang', default=DEFAULT_LANG, choices=gtts.lang.tts_langs(),
                        help=f"language to use (default: {DEFAULT_LANG})."
                             " If you change it, you may likely want to change the alphabet)")
    parser.add_argument('--length', default=DEFAULT_LENGTH, type=int,
                        help=f"acronym length (default: {DEFAULT_LENGTH})")
    parser.add_argument('--slow', action='store_true',
                        help="makes the speaker talk slowly")
    parser.add_argument('--start-number', default=DEFAULT_START_NUMBER, type=int,
                        help=f"lowest number to sample, if --add-number is used (default: {DEFAULT_START_NUMBER})")
    return parser.parse_args()


def wait_for_enter() -> None:
    print("Press ENTER to continue...", end='')
    input()
    print()


def say(text: str, lang: str = DEFAULT_LANG, slow: bool = False) -> None:
    tts = gtts.gTTS(text, lang=lang, slow=slow)
    with tempfile.NamedTemporaryFile() as file:
        tts.write_to_fp(file)
        vlc.MediaPlayer(file.name).play()


def game(add_number: bool = False, alphabet: str = DEFAULT_ALPHABET, end_number: int = DEFAULT_START_NUMBER,
         lang: str = DEFAULT_LANG, length: int = DEFAULT_LENGTH, slow: bool = False,
         start_number: int = DEFAULT_END_NUMBER) -> None:
    alphabet_list = list(alphabet)

    print("Spelling Practice: a game to practice acronym spelling.")
    print()
    print(f"Hear a speaker saying a random acronym of length {length}{' + a number' if add_number else ''}"
          f" and write it. Press Ctrl+C anytime to exit.")
    print()

    wait_for_enter()

    correct_count = total = 0

    try:
        while True:
            # Use NumPy because it provides sampling with replacement.
            spelling_list = np.random.choice(alphabet_list, size=length, replace=True)

            if add_number:
                number = random.randint(start_number, end_number)
                index = random.randint(0, len(spelling_list))
                spelling_list.insert(index, str(number))

            spelling_to_play = ' '.join(spelling_list)
            spelling_to_compare = ''.join(spelling_list)

            say(spelling_to_play, lang=lang, slow=slow)

            print("Acronym: ", end='')
            guess = input()
            is_correct = guess.upper() == spelling_to_compare

            if is_correct:
                print("Correct!")
                correct_count += 1
            else:
                print(f"Incorrect. It was {spelling_to_compare}.")

            total += 1

            wait_for_enter()
    except KeyboardInterrupt:
        if total > 0:
            print()
            print()
            print(f"Correct answers: {correct_count}/{total} ({100.0 * correct_count / total}%)")
        else:
            raise


def main() -> None:
    args = parse_args()
    game(**args.__dict__)


if __name__ == '__main__':
    main()
