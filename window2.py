import tkinter as tk
from tkinter import ttk
import openai
import json

openai.api_key  = 

def get_completion_from_messages(messages, model="gpt-3.5-turbo", temperature=0):
    response = openai.ChatCompletion.create(
        model=model,
        messages=messages,
        temperature=temperature, # this is the degree of randomness of the model's output
    )
#     print(str(response.choices[0].message))
    return response.choices[0].message["content"]

class ChatApp:
    def __init__(self, master, my_list):
        self.master = master
        self.my_list = my_list
        self.createWidgets()
    
    def createWidgets(self):
        self.frame0 = ttk.Frame(self.master, padding="10")
        self.frame0.grid(row=0, column=0, sticky=(tk.E, tk.N, tk.S, tk.W))
        
        # Create a label and button
        self.label1 = tk.Label(self.frame0, text="My List:")
        self.label1.pack()
        
        self.button1 = tk.Button(self.frame0, text="Refresh", command=None)
        self.button1.pack(pady=5)
        # Create a Tkinter Treeview widget
        self.tree = ttk.Treeview(self.frame0, columns=("Index", "Item"), show="headings")
        self.tree.pack(fill=tk.BOTH, expand=True)
        
        # Set column widths and headings
        self.tree.column("#0", width=0, stretch=tk.NO)
        self.tree.column("Index", width=40, anchor=tk.CENTER)
        self.tree.heading("Index", text="Index")
        self.tree.column("Item", width=800, anchor=tk.W)
        self.tree.heading("Item", text="Title")
        
        # Add items from the list to the Treeview widget
        for i, item in enumerate(self.my_list):
            self.tree.insert("", "end", values=(i+1, item))

        self.frame = ttk.Frame(self.master, padding="10")
        self.frame.grid(row=0, column=1, sticky=(tk.E, tk.N, tk.S, tk.W))

        self.chat_history = tk.Text(self.frame, wrap=tk.WORD, state="disabled", width=50, height=15)
        self.chat_history.grid(row=0, column=0, columnspan=2, sticky=(tk.W, tk.E, tk.N, tk.S))

        self.scrollbar = ttk.Scrollbar(self.frame, orient="vertical", command=self.chat_history.yview)
        self.scrollbar.grid(row=0, column=2, sticky=(tk.N, tk.S))

        self.chat_history["yscrollcommand"] = self.scrollbar.set

        self.user_text = tk.StringVar()
        self.entry_field = ttk.Entry(self.frame, textvariable=self.user_text, width=40)
        self.entry_field.grid(row=1, column=0, sticky=(tk.W, tk.E))

        self.send_button = ttk.Button(self.frame, text="Send", command=self.send_message)
        self.send_button.grid(row=1, column=1, sticky=(tk.W, tk.E))

        self.entry_field.bind("<Return>", self.send_message)
        self.entry_field.focus_set()

        self.frame.columnconfigure(0, weight=1)
        self.frame.columnconfigure(1, weight=1)
        self.frame.rowconfigure(0, weight=1)

    def send_message(self,event=None):
        user_input = self.user_text.get()
        if user_input:
            self.chat_history.configure(state="normal")
            self.chat_history.insert(tk.END, f"You: {user_input}\n")
            self.user_text.set("")
            self.chat_history.insert(tk.END, f"AI: {self.collect_messages(user_input)}\n")
            self.chat_history.configure(state="disabled")
            self.chat_history.yview(tk.END)

    def collect_messages(self, input):
        context.append({'role':'user', 'content':f"{input}"})
        response = get_completion_from_messages(context) 
        context.append({'role':'assistant', 'content':f"{response}"})
        return response


#读取scrapy获得的文章数据
with open("phys.org-with-chatgpt/data.json","r",encoding = "utf-8") as data:
    data_contents = json.load(data)

titles = []
for data_item in data_contents:
    titles.append(data_item["title"])

#for data_item in data_contents:
data_item = data_contents[0]
title = data_item["title"]  
abstract = data_item["brief"]
body = data_item["body"]

context = [ {'role':'system', 'content':f"""
You are an analyst of articles about physics. \
Here, we have an article with title, abstract and full text which are listed below. \
Title: '''{title}''' \
Abstract:'''{abstract}''' \
Text: '''{body}''' \
The user will chat with you about this article. \
Please provide information asked by the user.
"""} ]  # accumulate messages


# Create the Tkinter app and pass in the list
root = tk.Tk()
root.title("Chatbot")    # #窗口标题
root.geometry("1000x1000+200+20")   # #窗口位置后面是字母
app = ChatApp(root,titles)
root.mainloop()