import random
import os
import subprocess
from termcolor import colored
from collections import Counter
from pathlib import Path
from enum import Enum


MAX_ATTEMPTS = 6
WORD_LEN     = 5

WORD_BANK_PATH = Path(__file__).parent.parent / "res" / "word_bank.txt"


class LetterState(Enum):
    RED    = 1
    YELLOW = 2
    GREEN  = 3

BG_COLORS = {
    LetterState.RED: "on_red",
    LetterState.YELLOW: "on_yellow",
    LetterState.GREEN: "on_green",
}


class BoardPrinter:
    def __init__(self):
        self.lines: list[str] = [" ".join("_" * WORD_LEN)] * MAX_ATTEMPTS
        self.last_index = 0
    
    def display_board(self, size=WORD_LEN * 2 - 1, padding=1):
        middle_len = size + padding * 2
        top_border = "    ┌" + "─" * middle_len + "┐"
        bottom_border = "    └" + "─" * middle_len + "┘"
        space = " " * padding

        print(colored("   WORDLE TERMINAL", "blue"))
        print(top_border)
        for line in self.lines:
            print("    │" + space + line + space + "│")
        print(bottom_border)

    def add_line(self, new_line: list[str], color_encoding: list[LetterState]) -> None:
        colored_line: str = self._convert_to_colored(new_line, color_encoding)
        self.lines[self.last_index] = colored_line
        self.last_index += 1

    def _convert_to_colored(self, line: list[str], color_encoding: list[LetterState]) -> str:
        return " ".join(
            colored(letter, color="black", on_color=BG_COLORS[state])
            for letter, state in zip(line, color_encoding)
        )
    

class Wordle:
    def __init__(self, secret_word: str) -> None:
        self.printer = BoardPrinter()
        self.secret_word = secret_word
        self.attempts: list[str] = []

    def is_game_over(self) -> bool:
        return self._attempts_remaining() <= 0 or self.player_has_won()

    def make_attempt(self, user_guess: str) -> None:
        self.attempts.append(user_guess)

    def player_has_won(self) -> bool:
        return len(self.attempts) > 0 and self.attempts[-1] == self.secret_word

    def validate_guess(self) -> None:
        result: list[LetterState] = [None] * WORD_LEN
        if len(self.attempts) == 0:
            return result
        
        counter = Counter()
        guess = self.attempts[-1]

        # First pass: mark green letters
        for i in range(WORD_LEN):
            if guess[i] == self.secret_word[i]:
                result[i] = LetterState.GREEN
            else:
                counter[self.secret_word[i]] += 1

        # Second pass: mark yellow and red letters
        for i in range(WORD_LEN):
            if result[i] == LetterState.GREEN:
                continue
            if counter[guess[i]] > 0:
                result[i] = LetterState.YELLOW
                counter[guess[i]] -= 1
            else:
                result[i] = LetterState.RED

        self.printer.add_line(self.attempts[-1], color_encoding=result)

    def update_display(self) -> None:
        clear_screen()
        self.printer.display_board()

    def _attempts_remaining(self) -> int:
        return MAX_ATTEMPTS - len(self.attempts)
    

def clear_screen() -> None:
    cmd = "cls" if os.name == "nt" else "clear"
    subprocess.run(cmd, shell=(os.name == "nt"), check=False)

def load_wordbank(path: str) -> list[str]:
    with open(path, "r") as f:
        words = (line.strip().upper() for line in f)
        return [w for w in words if len(w) == WORD_LEN]

def main():
    word_bank: list[str] = load_wordbank(WORD_BANK_PATH)
    secret_word: str = random.choice(word_bank)
    valid_words: set[str] = set(word_bank)
    
    wordle = Wordle(secret_word)

    message = ""
    while not wordle.is_game_over():
        wordle.update_display()
        if message:
            print(message)
            message = ""

        user_guess: str = input("\nType your guess: ").strip().upper()
    
        if len(user_guess) != WORD_LEN:
            message = colored(f"Words must be of {WORD_LEN} letters in length.", "red")
            continue
        if user_guess not in valid_words:
            message = colored(f"\"{user_guess}\" not in word list.", "red")
            continue
    
        wordle.make_attempt(user_guess)
        wordle.validate_guess()

    wordle.update_display()
    if wordle.player_has_won():
        print(colored("\nCORRECT - You won!\n", "green"))
    else:
        print(colored(f"\nWRONG - The word was {wordle.secret_word}\n", "red"))


if __name__ == "__main__":
    main()