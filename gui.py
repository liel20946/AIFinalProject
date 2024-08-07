import tkinter as tk


class FlowFreeGUI:
    def __init__(self, root, board_width, board_height):
        self.root = root
        self.board_width = board_width
        self.board_height = board_height
        self.cell_size = 100
        self.cells = [[None for _ in range(board_width)] for _ in
                      range(board_height)]
        self.moves = 0
        self.search_time = 0.0  # To store the search algorithm time
        self.pipe_filled = 0.35  # Example pipe filled percentage
        self.setup_gui()
        self.center_window()

    def setup_gui(self):
        self.root.title("Flow Free")

        # Create a frame for the "You Win" message
        self.win_frame = tk.Frame(self.root)
        self.win_frame.grid(row=0, column=0, columnspan=self.board_width)

        self.win_label = tk.Label(self.win_frame, text="",
                                  font=("Helvetica", 20), fg="green")
        self.win_label.pack()

        # Create a frame for the labels
        label_frame = tk.Frame(self.root)
        label_frame.grid(row=1, column=0, columnspan=self.board_width)

        self.moves_label = tk.Label(label_frame, text=f"moves: {self.moves}",
                                    font=("Helvetica", 16), fg="orange")
        self.moves_label.pack(side=tk.LEFT, padx=20)

        self.search_time_label = tk.Label(label_frame,
                                          text=f"time: {self.search_time:.2f} s",
                                          font=("Helvetica", 16), fg="orange")
        self.search_time_label.pack(side=tk.LEFT, padx=20)

        self.pipe_filled_label = tk.Label(label_frame,
                                          text=f"pipe: {int(self.pipe_filled * 100)}%",
                                          font=("Helvetica", 16), fg="white")
        self.pipe_filled_label.pack(side=tk.LEFT, padx=20)

        for i in range(self.board_height):
            for j in range(self.board_width):
                canvas = tk.Canvas(master=self.root, width=self.cell_size,
                                   height=self.cell_size, bg='black',
                                   highlightthickness=0.5,
                                   highlightbackground='#808080')
                canvas.grid(row=i + 2,
                            column=j)  # Adjusted row to make space for labels
                self.cells[i][j] = canvas

    def update_board(self, game_board):
        for i in range(self.board_height):
            for j in range(self.board_width):
                color = game_board[i][j]
                self.cells[i][j].delete("all")
                if color != 'black':
                    self.cells[i][j].create_oval(self.cell_size // 5,
                                                 self.cell_size // 5,
                                                 self.cell_size * 4 // 5,
                                                 self.cell_size * 4 // 5,
                                                 fill=color, outline="")
        self.connect_adjacent_cells(game_board)
        self.update_labels()

    def connect_adjacent_cells(self, game_board):
        directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
        for i in range(self.board_height):
            for j in range(self.board_width):
                color = game_board[i][j]
                if color != 'black':
                    for di, dj in directions:
                        ni, nj = i + di, j + dj
                        if 0 <= ni < self.board_height and 0 <= nj < self.board_width:
                            if game_board[ni][nj] == color:
                                self.cells[i][j].lift("all")
                                self.cells[i][j].create_line(
                                    self.cell_size // 2, self.cell_size // 2,
                                    self.cell_size // 2 + self.cell_size * dj,
                                    self.cell_size // 2 + self.cell_size * di,
                                    fill=color, width=20)

    def update_labels(self):
        self.moves_label.config(text=f"moves: {self.moves}")
        self.search_time_label.config(text=f"time: {self.search_time:.2f} s")

    def increment_moves(self):
        self.moves += 1
        self.update_labels()

    def set_search_time(self, search_time):
        self.search_time = search_time
        self.update_labels()

    def display_win_message(self):
        self.win_label.config(text="You Win!")

    def center_window(self):
        self.root.update_idletasks()
        window_width = self.root.winfo_width()
        window_height = self.root.winfo_height()
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        position_right = int(screen_width / 2 - window_width / 2)
        position_down = int(screen_height / 2 - window_height / 2)
        self.root.geometry(
            f'{window_width}x{window_height}+{position_right}+{position_down}')