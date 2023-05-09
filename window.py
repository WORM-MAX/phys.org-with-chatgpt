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
    def __init__(self, master, my_list, tips):
        self.master = master
        self.my_list = my_list
        self.tips = tips
        self.indexs = range(len(my_list))
        self.var1 = tk.StringVar()
        self.var1.set("Get the newest articles on phys.org/physics-news")
        self.createWidgets()

    def createWidgets(self):
        #self.frame0 = ttk.Frame(self.master, padding="10")
        #self.frame0.grid(row=1, column=0, columnspan=2, sticky=(tk.E, tk.N, tk.S, tk.W))
        
        # Create a label and button
        
        self.label1 = tk.Label(self.master, textvariable=self.var1, font=('Arial', 12),width=85,height=1)
        self.label1.grid(row=0,column=0,columnspan=2,sticky=(tk.E, tk.N, tk.S, tk.W), padx=1, pady=1)
        
        self.button1 = tk.Button(self.master, text="Scrape", command=None, font=('Arial', 12))
        self.button1.grid(row=0, column=2, sticky='nsew', padx=1, pady=1)

        style = ttk.Style()

        #self.master.columnconfigure(0,weight=7)
        #self.master.columnconfigure(1,weight=7)
        #self.master.columnconfigure(2,weight=1)
        #self.master.columnconfigure(3,weight=7)
        self.master.rowconfigure(0,weight=1)
        self.master.rowconfigure(1,weight=10)
        self.master.rowconfigure(2,weight=5)


        # Create a Tkinter Treeview widget
        self.tree = ttk.Treeview(self.master,height=17, columns=("Index", "Item"), show="headings")
        self.tree.grid(row=1, column=0, columnspan=3, sticky='nsew', padx=1, pady=1)

        # Set column widths and headings
        self.tree.column("#0", width=0, stretch=tk.NO)
        self.tree.column("Index", width=30, anchor=tk.CENTER)
        self.tree.heading("Index", text="Index")
        self.tree.column("Item", width=600,anchor=tk.W)
        self.tree.heading("Item", text="Title")
        
        # Add items from the list to the Treeview widget
        for i, item in enumerate(self.my_list):
            self.tree.insert("", "end", values=(i, item))

        #A Frame for tips on the bottom
        self.frame1 = ttk.Frame(self.master, padding="10")
        self.frame1.grid(row=2, column=0, columnspan=3, sticky=(tk.E, tk.N, tk.S, tk.W))

        self.message1 = tk.Message(self.frame1,text=self.tips,width=750, font=('Arial', 14))
        self.message1.grid(row=0, rowspan=2, column=0, columnspan=2, sticky=(tk.E, tk.N, tk.S, tk.W))

        #listbox for choosing
        var2 = tk.StringVar() 
        var2.set(tuple(self.indexs))
        self.listbox = tk.Listbox(self.frame1,listvariable=var2,
                                  font=('Arial', 12), width=10, height=10)
        self.listbox.grid(row=0, column=2,padx=1,pady=1)

        self.button2 = tk.Button(self.frame1, text="Start", command=self.startbot(),font=('Arial', 12), width=10, height=1)
        self.button2.grid(row=1,column=2,sticky=(tk.E, tk.N, tk.S),padx=1,pady=1)

        self.frame1.columnconfigure(0, weight=5)
        self.frame1.columnconfigure(1, weight=5)
        self.frame1.columnconfigure(2, weight=1)
        #self.frame1.rowconfigure(0, weight=10)
        #self.frame1.rowconfigure(1, weight=1)


        #A Frame for chatbot
        self.chat_frame = ttk.Frame(self.master, padding="10")
        self.chat_frame.grid(row=0, rowspan=3, column=3, sticky=(tk.E, tk.N, tk.S, tk.W))

        self.chat_history = tk.Text(self.chat_frame, wrap=tk.WORD, state="disabled", width=50, height=50)
        self.chat_history.grid(row=0, column=0, columnspan=2, sticky=(tk.W, tk.E, tk.N, tk.S))

        self.scrollbar = ttk.Scrollbar(self.chat_frame, orient="vertical", command=self.chat_history.yview)
        self.scrollbar.grid(row=0, rowspan = 2, column=2, sticky=(tk.N, tk.S))

        self.chat_history["yscrollcommand"] = self.scrollbar.set

        self.user_text = tk.StringVar()
        self.entry_field = ttk.Entry(self.chat_frame, textvariable=self.user_text, width=40)
        self.entry_field.grid(row=1, column=0, sticky=(tk.W, tk.E))

        self.send_button = ttk.Button(self.chat_frame, text="Send", command=self.send_message)
        self.send_button.grid(row=1, column=1, sticky=(tk.W, tk.E))

        self.entry_field.bind("<Return>", self.send_message)
        self.entry_field.focus_set()

        self.chat_frame.columnconfigure(0, weight=2)
        self.chat_frame.columnconfigure(1, weight=1)
        self.chat_frame.rowconfigure(0, weight=1)

    def startbot(self):
        #self.value = self.listbox.get(self.listbox.curselection())
        return 0

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

    def scrape(self):
        self.var1.set("Already load")



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

tips = """
Choose one of your favourite articles listed above in the listbox right. \
And chat with bot to get what your want.

Here are some prompt examples.
1. Tell me the structure and summarize key point.  \
Use the bullet point to separate different parts. \
For the body part, you should offer more detailed information with three sentences.
2. Extract five keywords from the article.
3.Summarize the background, research method and meaning with bullet point.
"""



# Create the Tkinter app and pass in the list
root = tk.Tk()
root.title("Chatbot")    # #窗口标题
root.geometry("1200x800+50+20")   # #窗口位置后面是字母
root.resizable(width=True, height=True)
app = ChatApp(root,titles,tips)
root.mainloop()