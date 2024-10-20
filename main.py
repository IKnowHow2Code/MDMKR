import tkinter as tk
from tkinter import filedialog, messagebox, simpledialog
from markdown import markdown

# Did you know otters hold hands while sleeping so they don’t drift apart? True friendship.
class MDMKR(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("MDMKR - Markdown Creator")
        self.geometry("1000x600")
        
        # Sidebar: The control center of our spaceship. Blue is for calm, like outer space.
        self.sidebar = tk.Frame(self, width=180, bg="#ddeeff")
        self.sidebar.pack(side="left", fill="y")
        
        # The canvas, where your stories come alive like a vibrant blue ocean.
        self.canvas = tk.Frame(self, bg="white", width=600)
        self.canvas.pack(side="left", fill="both", expand=True)
        
        # The preview pane - think of it as the crystal ball of your Markdown journey.
        self.preview = tk.Text(self, bg="#eef2ff", state="disabled", width=40)
        self.preview.pack(side="right", fill="y")

        # Setting up the command station (aka, sidebar buttons).
        self.create_sidebar_buttons()
        
        # Content list, storing the memories of your hard work.
        self.content_list = []

        # Listen for changes in size or configuration to update the magic preview.
        self.bind("<Configure>", self.update_preview)
        
        # When someone clicks the canvas, give them the space they deserve.
        self.canvas.bind("<Button-1>", self.clear_selection)

    def create_sidebar_buttons(self):
        # Group for headings and text
        tk.Label(self.sidebar, text="Text Elements", bg="#ddeeff", font=("Arial", 10, "bold")).pack(pady=(10, 0))
        
        heading_btn = tk.Button(self.sidebar, text="Add Heading", bg="#99ccff", command=self.add_heading)
        heading_btn.pack(padx=10, pady=5, fill="x")

        text_btn = tk.Button(self.sidebar, text="Add Text", bg="#99ccff", command=self.add_text)
        text_btn.pack(padx=10, pady=5, fill="x")

        blockquote_btn = tk.Button(self.sidebar, text="Add Blockquote", bg="#99ccff", command=self.add_blockquote)
        blockquote_btn.pack(padx=10, pady=5, fill="x")

        hr_btn = tk.Button(self.sidebar, text="Add Horizontal Line", bg="#99ccff", command=self.add_horizontal_line)
        hr_btn.pack(padx=10, pady=5, fill="x")

        code_btn = tk.Button(self.sidebar, text="Add Code Block", bg="#99ccff", command=self.add_code_block)
        code_btn.pack(padx=10, pady=5, fill="x")

        inline_code_btn = tk.Button(self.sidebar, text="Add Inline Code", bg="#99ccff", command=self.add_inline_code)
        inline_code_btn.pack(padx=10, pady=5, fill="x")

        link_btn = tk.Button(self.sidebar, text="Add Link", bg="#99ccff", command=self.add_link)
        link_btn.pack(padx=10, pady=5, fill="x")

        # Group for lists and images
        tk.Label(self.sidebar, text="Lists & Media", bg="#ddeeff", font=("Arial", 10, "bold")).pack(pady=(20, 0))

        bulleted_list_btn = tk.Button(self.sidebar, text="Add Bulleted List", bg="#99ccff", command=self.add_bulleted_list)
        bulleted_list_btn.pack(padx=10, pady=5, fill="x")

        numbered_list_btn = tk.Button(self.sidebar, text="Add Numbered List", bg="#99ccff", command=self.add_numbered_list)
        numbered_list_btn.pack(padx=10, pady=5, fill="x")

        image_btn = tk.Button(self.sidebar, text="Add Image", bg="#99ccff", command=self.add_image)
        image_btn.pack(padx=10, pady=5, fill="x")

        # Save and Import group
        tk.Label(self.sidebar, text="File Actions", bg="#ddeeff", font=("Arial", 10, "bold")).pack(pady=(20, 0))

        save_btn = tk.Button(self.sidebar, text="Save Markdown", bg="#6699ff", command=self.save_markdown)
        save_btn.pack(padx=10, pady=5, fill="x")

        open_btn = tk.Button(self.sidebar, text="Open Markdown", bg="#6699ff", command=self.open_markdown)
        open_btn.pack(padx=10, pady=5, fill="x")

    def add_heading(self):
        text = simpledialog.askstring("Input", "Enter the heading text:")
        if text:
            self.add_to_canvas("Heading", f"# {text}")

    def add_text(self):
        text = simpledialog.askstring("Input", "Enter the text:")
        if text:
            self.add_to_canvas("Text", text)

    def add_blockquote(self):
        text = simpledialog.askstring("Input", "Enter the blockquote text:")
        if text:
            self.add_to_canvas("Blockquote", f"> {text}")

    def add_horizontal_line(self):
        self.add_to_canvas("Horizontal Line", "---")

    def add_code_block(self):
        language = simpledialog.askstring("Input", "Enter the programming language (or leave blank):")
        code = simpledialog.askstring("Input", "Enter your code:")
        if code:
            code_md = f"```{language}\n{code}\n```" if language else f"```\n{code}\n```"
            self.add_to_canvas("Code Block", code_md)

    def add_inline_code(self):
        code = simpledialog.askstring("Input", "Enter the inline code:")
        if code:
            self.add_to_canvas("Inline Code", f"`{code}`")

    def add_link(self):
        url = simpledialog.askstring("Input", "Enter the URL:")
        text = simpledialog.askstring("Input", "Enter the link text:")
        if url and text:
            self.add_to_canvas("Link", f"[{text}]({url})")

    def add_bulleted_list(self):
        items = []
        while True:
            item = simpledialog.askstring("Input", "Enter a list item (or leave blank to finish):")
            if not item:
                break
            items.append(f"- {item}")
        if items:
            self.add_to_canvas("Bulleted List", "\n".join(items))

    def add_numbered_list(self):
        items = []
        index = 1
        while True:
            item = simpledialog.askstring("Input", f"Enter item {index} (or leave blank to finish):")
            if not item:
                break
            items.append(f"{index}. {item}")
            index += 1
        if items:
            self.add_to_canvas("Numbered List", "\n".join(items))

    def add_image(self):
        file_path = filedialog.askopenfilename(filetypes=[("Image Files", "*.png *.jpg *.jpeg *.gif")])
        if file_path:
            alt_text = simpledialog.askstring("Input", "Enter the image alt text:")
            caption = simpledialog.askstring("Input", "Enter an optional caption (leave blank if none):")
            image_md = f"![{alt_text}]({file_path})"
            if caption:
                image_md += f"\n*{caption}*"
            self.add_to_canvas("Image", image_md)

    def add_to_canvas(self, element_type, content):
        element_frame = tk.Frame(self.canvas, bg="white", padx=5, pady=5, relief="solid", borderwidth=1)
        element_frame.pack(pady=5, fill="x")
        
        label = tk.Label(element_frame, text=element_type)
        label.pack(side="left")
        
        edit_button = tk.Button(element_frame, text="Edit", command=lambda: self.edit_element(element_frame, element_type, content))
        edit_button.pack(side="right")

        delete_button = tk.Button(element_frame, text="Delete", command=lambda: self.delete_element(element_frame))
        delete_button.pack(side="right")

        move_up_button = tk.Button(element_frame, text="↑", command=lambda: self.move_element_up(element_frame))
        move_up_button.pack(side="right")

        move_down_button = tk.Button(element_frame, text="↓", command=lambda: self.move_element_down(element_frame))
        move_down_button.pack(side="right")

        element_frame.content = content
        self.content_list.append(element_frame)
        self.update_preview()

    def edit_element(self, element_frame, element_type, content):
        new_content = simpledialog.askstring("Edit Content", f"Edit the {element_type.lower()}:", initialvalue=content)
        if new_content:
            element_frame.content = new_content
            self.update_preview()

    def delete_element(self, element_frame):
        element_frame.destroy()
        self.content_list.remove(element_frame)
        self.update_preview()

    def move_element_up(self, element_frame):
        index = self.content_list.index(element_frame)
        if index > 0:
            self.content_list.pop(index)
            self.content_list.insert(index - 1, element_frame)
            element_frame.pack_forget()
            element_frame.pack(before=self.content_list[index])
            self.update_preview()

    def move_element_down(self, element_frame):
        index = self.content_list.index(element_frame)
        if index < len(self.content_list) - 1:
            self.content_list.pop(index)
            self.content_list.insert(index + 1, element_frame)
            element_frame.pack_forget()
            element_frame.pack(after=self.content_list[index])
            self.update_preview()

    def clear_selection(self, event):
        self.focus_set()

    def update_preview(self, event=None):
        markdown_content = "\n\n".join([element.content for element in self.content_list])
        self.preview.config(state="normal")
        self.preview.delete(1.0, tk.END)
        self.preview.insert(tk.END, markdown(markdown_content))
        self.preview.config(state="disabled")

    def save_markdown(self):
        file_path = filedialog.asksaveasfilename(defaultextension=".md", filetypes=[("Markdown Files", "*.md")])
        if file_path:
            with open(file_path, 'w') as file:
                markdown_content = "\n\n".join([element.content for element in self.content_list])
                file.write(markdown_content)
            messagebox.showinfo("Success", "Markdown file saved successfully!")

    def open_markdown(self):
        file_path = filedialog.askopenfilename(filetypes=[("Markdown Files", "*.md")])
        if file_path:
            with open(file_path, 'r') as file:
                markdown_content = file.read()
            self.load_markdown(markdown_content)

    def load_markdown(self, markdown_content):
        # Clear current content
        for element in self.content_list:
            element.destroy()
        self.content_list.clear()

        # Simple parser to break down the Markdown content
        lines = markdown_content.splitlines()
        for line in lines:
            line = line.strip()
            if line.startswith("#"):
                self.add_to_canvas("Heading", line)
            elif line.startswith(">"):
                self.add_to_canvas("Blockquote", line)
            elif line.startswith("- "):
                self.add_to_canvas("Bulleted List", line)
            elif line.isdigit() and line[1:].strip().startswith("."):
                self.add_to_canvas("Numbered List", line)
            elif line == "---":
                self.add_to_canvas("Horizontal Line", line)
            elif line.startswith("```"):
                code_block = "\n".join(lines[lines.index(line):lines.index("```", lines.index(line) + 1) + 1])
                self.add_to_canvas("Code Block", code_block)
            elif line.startswith("!["):
                self.add_to_canvas("Image", line)
            elif line.startswith("`") and line.endswith("`"):
                self.add_to_canvas("Inline Code", line)
            elif line.startswith("[") and "](" in line:
                self.add_to_canvas("Link", line)
            else:
                self.add_to_canvas("Text", line)
        self.update_preview()


if __name__ == "__main__":
    app = MDMKR()
    app.mainloop()
