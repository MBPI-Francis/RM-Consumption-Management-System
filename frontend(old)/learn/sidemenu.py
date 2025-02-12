import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from ttkbootstrap.scrolled import ScrolledFrame


class App(ttk.Window):
    def __init__(self):
        super().__init__(themename="cosmo")  # Choose the ttkbootstrap theme
        self.title("TTKBootstrap Sidebar Navigation")
        self.geometry("800x600")

        # Configure row/column for responsiveness

        self.rowconfigure(0, weight=1)

        # Create custom styles
        style = ttk.Style()
        style.configure("Sidebar.TFrame", background="white")  # Brown color

        # Sidebar Frame
        self.sidebar = ttk.Frame(self, width=200, padding=10, style="Sidebar.TFrame")
        self.sidebar.grid(row=0, column=0, sticky=N+S)

        # Vertical Separator
        self.separator = ttk.Separator(self, orient=VERTICAL)
        self.separator.grid(row=0, column=1, sticky=N+S)

        # Main Content Frame
        self.content_frame = ttk.Frame(self, padding=10)
        self.content_frame.grid(row=0, column=2, sticky=N+S+E+W)

        # Sidebar Buttons
        self.create_sidebar_buttons()

        # Default view
        self.show_warehouse_content()

    def create_sidebar_buttons(self):
        """Creates the sidebar buttons for navigation."""
        ttk.Button(
            self.sidebar,
            text="Warehouse",
            command=self.show_warehouse_content,
            bootstyle=PRIMARY,
            width=15,
        ).pack(pady=10)

        ttk.Button(
            self.sidebar,
            text="Department",
            command=self.show_department_content,
            bootstyle=SUCCESS,
            width=15,
        ).pack(pady=10)

        ttk.Button(
            self.sidebar,
            text="User",
            command=self.show_user_content,
            bootstyle=INFO,
            width=15,
        ).pack(pady=10)

    def clear_content_frame(self):
        """Clears all widgets from the content frame."""
        for widget in self.content_frame.winfo_children():
            widget.destroy()

    def show_warehouse_content(self):
        """Displays the Warehouse content."""
        self.clear_content_frame()
        label = ttk.Label(
            self.content_frame,
            text="Warehouse Content",
            font=("Helvetica", 18),
            bootstyle=PRIMARY,
        )
        label.pack(pady=20)

        # Example ScrolledFrame content for Warehouse
        scroll_frame = ScrolledFrame(self.content_frame)
        scroll_frame.pack(fill=BOTH, expand=YES, pady=10)

        for i in range(20):  # Add example items
            ttk.Label(
                scroll_frame,
                text=f"Warehouse Item {i+1}",
                bootstyle=SECONDARY,
            ).pack(pady=5)

    def show_department_content(self):
        """Displays the Department content."""
        self.clear_content_frame()
        label = ttk.Label(
            self.content_frame,
            text="Department Content",
            font=("Helvetica", 18),
            bootstyle=SUCCESS,
        )
        label.pack(pady=20)

    def show_user_content(self):
        """Displays the User content."""
        self.clear_content_frame()
        label = ttk.Label(
            self.content_frame,
            text="User Content",
            font=("Helvetica", 18),
            bootstyle=INFO,
        )
        label.pack(pady=20)


if __name__ == "__main__":
    app = App()
    app.mainloop()
