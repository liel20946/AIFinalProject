# flow_free_gui.py
import tkinter as tk


class FlowFreeGUI:
    def __init__(self, root, board_width, board_height):
        self.root = root
        self.board_width = board_width
        self.board_height = board_height
        self.cells = [[None for _ in range(board_width)] for _ in
                      range(board_height)]
        self.setup_gui()
        self.center_window()

    def setup_gui(self):
        self.root.title("Flow Free")
        for i in range(self.board_height):
            for j in range(self.board_width):
                frame = tk.Frame(
                    master=self.root,
                    relief=tk.RAISED,
                    borderwidth=1
                )
                frame.grid(row=i, column=j)
                label = tk.Label(master=frame, text="", width=10, height=5)
                label.pack()
                self.cells[i][j] = label

    def update_board(self, game_board):
        for i in range(self.board_height):
            for j in range(self.board_width):
                color = game_board[i][j]
                display_color = color
                self.cells[i][j].config(bg=display_color)

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
