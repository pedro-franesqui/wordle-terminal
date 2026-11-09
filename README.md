# Terminal Wordle

Play Wordle in your terminal. The player has six chances to guess a hidden five-letter word, with color-coded feedback after each attempt.

## How to Play

1. Run the game from the project root:

   ```bash
   python src/terminal_wordle.py
   ```

2. Enter a valid 5-letter word.
3. After each guess, the board highlights letters:
   - Green: correct letter in the correct position
   - Yellow: correct letter in the wrong position
   - Red: letter not in the word
4. You win if you guess the secret word within 6 tries.

## Rules

- The secret word is chosen randomly from a built-in word bank.
- Only valid dictionary words from the included list are accepted.
- Each guess must be exactly 5 letters long.
- The game ends when you either:
  - guess the word correctly, or
  - use all 6 attempts

## Features

- Terminal-based board display
- Randomized secret word selection
- Color-coded feedback using the `termcolor` package
- Clean screen refresh between guesses
- Simple word validation against a local word bank

## Project Structure

```text
terminal-wordle/
├── res/
│   └── word_bank.txt
├── src/
│   └── terminal_wordle.py
├── tests/
│   └── test_word_bank.txt
├── .gitignore
└── README.md
```

## Requirements

- Python 3
- `termcolor`

Install the dependency with:

```bash
pip install termcolor
```

## Future Ideas

- Add a replay option
- Include a difficulty setting
- Support a larger dictionary
- Add score tracking and win/loss stats
- Improve the terminal interface with custom ASCII styling
