from board import Board


DIFFICULTIES = {
    "easy": (6, 6, 6),
    "medium": (8, 8, 12),
    "hard": (10, 10, 20),
}


class Minesweeper:
    def __init__(self, difficulty="easy"):
        rows, cols, mines = DIFFICULTIES[difficulty]
        self.difficulty = difficulty
        self.board = Board(rows, cols, mines)

    def display(self, reveal_mines=False):
        print(f"\nDifficulty: {self.difficulty.capitalize()}")
        print(f"Board: {self.board.rows}x{self.board.cols} | Mines: {self.board.mine_total}")

        print("   " + " ".join(f"{c:2}" for c in range(1, self.board.cols + 1)))

        for r in range(self.board.rows):
            row = []
            for c in range(self.board.cols):
                pos = (r, c)

                if reveal_mines and pos in self.board.mines:
                    cell = "*"
                elif pos in self.board.flags:
                    cell = "F"
                elif pos not in self.board.revealed:
                    cell = "#"
                else:
                    mines = self.board.adjacent_mines(r, c)
                    cell = str(mines) if mines else "."

                row.append(f"{cell:2}")

            print(f"{r + 1:2} " + " ".join(row))

    def choose_difficulty(self):
        print("Choose difficulty:")
        print("1. Easy   - 6x6, 6 mines")
        print("2. Medium - 8x8, 12 mines")
        print("3. Hard   - 10x10, 20 mines")

        while True:
            choice = input("Difficulty (1/2/3): ").strip().lower()

            if choice in {"1", "easy"}:
                return "easy"
            if choice in {"2", "medium"}:
                return "medium"
            if choice in {"3", "hard"}:
                return "hard"

            print("Invalid difficulty. Choose 1, 2, or 3.")

    def run(self):
        difficulty = self.choose_difficulty()
        self.difficulty = difficulty

        rows, cols, mines = DIFFICULTIES[difficulty]
        self.board = Board(rows, cols, mines)

        print("\nMinesweeper")
        print("Commands: r row col | f row col | q")

        while True:
            self.display()

            raw = input("> ").strip().lower()

            if raw == "q":
                print("Game ended.")
                return

            parts = raw.split()

            if len(parts) != 3 or parts[0] not in {"r", "f"}:
                print("Action: Invalid command.")
                print("Use r row col or f row col.")
                continue

            try:
                r, c = int(parts[1]) - 1, int(parts[2]) - 1
            except ValueError:
                print("Action: Invalid coordinates.")
                print("Coordinates must be numbers.")
                continue

            if not self.board.in_bounds(r, c):
                print(f"Action: {parts[0].upper()} ({r + 1}, {c + 1}) rejected - outside the board.")
                print("Outside the board.")
                continue

            pos = (r, c)

            if parts[0] == "f":
                if not self.board.toggle_flag(pos):
                    print(f"Action: Flag ({r + 1}, {c + 1}) rejected - cell is already revealed.")
                    print("Cannot flag a revealed cell.")
                else:
                    state = "flagged" if pos in self.board.flags else "unflagged"
                    print(f"Action: Flag ({r + 1}, {c + 1}) -> {state}.")
                continue

            print(f"Action: Reveal ({r + 1}, {c + 1}).")

            if self.board.reveal(pos):
                self.display(reveal_mines=True)
                print("BOOM! You hit a mine.")
                return

            if self.board.won():
                self.display()
                print("You cleared the board!")
                return