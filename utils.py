import tkinter as tk
from tkinter import ttk
import openai
import json
import subprocess  


#get response from opanai api
def get_completion_from_messages(messages, model="gpt-3.5-turbo", temperature=0):
    response = openai.ChatCompletion.create(
        model=model,
        messages=messages,
        temperature=temperature, # this is the degree of randomness of the model's output
    )
    return response.choices[0].message["content"]

#GUI
class ChatApp:
    def __init__(self, master, tips):
        self.master = master
        self.titles = []
        self.tips = tips
        self.indexs = [0]
        self.var1 = tk.StringVar()#Label teext on the top
        self.var1.set("Get the newest articles on phys.org/physics-news")
        self.createWidgets()
        
    def createWidgets(self):
        # Create a label and button
        self.label1 = tk.Label(self.master, textvariable=self.var1, font=('Arial', 12),width=85,height=1)
        self.label1.grid(row=0,column=0,columnspan=2,sticky=(tk.E, tk.N, tk.S, tk.W), padx=1, pady=1)
        
        self.button1 = tk.Button(self.master, text="Scrape", command=self.scrape, font=('Arial', 12))
        self.button1.grid(row=0, column=2, sticky='nsew', padx=1, pady=1)

        # Create a Tkinter Treeview widget for titles
        self.tree = ttk.Treeview(self.master,height=17, columns=("Index", "Item"), show="headings")
        self.tree.grid(row=1, column=0, columnspan=3, sticky='nsew', padx=1, pady=1)

        # Set column widths and headings
        self.tree.column("#0", width=0, stretch=tk.NO)
        self.tree.column("Index", width=30, anchor=tk.CENTER)
        self.tree.heading("Index", text="Index")
        self.tree.column("Item", width=600,anchor=tk.W)
        self.tree.heading("Item", text="Title")

        #A Frame for tips on the bottom
        self.frame1 = ttk.Frame(self.master, padding="10")
        self.frame1.grid(row=2, column=0, columnspan=3, sticky=(tk.E, tk.N, tk.S, tk.W))

        self.message1 = tk.Message(self.frame1,text=self.tips,width=750, font=('Arial', 14))
        self.message1.grid(row=0, rowspan=2, column=0, columnspan=2, sticky=(tk.E, tk.N, tk.S, tk.W))

        #listbox for choosing
        self.var2 = tk.StringVar() 
        self.listbox = tk.Listbox(self.frame1,listvariable=self.var2,selectmode="single",
                                  font=('Arial', 12), width=10, height=10)
        self.listbox.grid(row=0, column=2,padx=1,pady=1)

        #Button for starting bot
        self.button2 = tk.Button(self.frame1, text="Start", command=self.startbot,font=('Arial', 12), width=10, height=1)
        self.button2.grid(row=1,column=2,sticky=(tk.E, tk.N, tk.S),padx=1,pady=1)

        self.frame1.columnconfigure(0, weight=5)
        self.frame1.columnconfigure(1, weight=5)
        self.frame1.columnconfigure(2, weight=1)
        #self.frame1.rowconfigure(0, weight=10)
        #self.frame1.rowconfigure(1, weight=1)


        #A Frame for chatbot
        self.chat_frame = ttk.Frame(self.master, padding="10")
        self.chat_frame.grid(row=0, rowspan=3, column=3, sticky=(tk.E, tk.N, tk.S, tk.W))

        self.chat_history = tk.Text(self.chat_frame, wrap=tk.WORD, state="disabled", font=('Arial', 12), width=50, height=50)
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
        
        #size configure
        self.chat_frame.columnconfigure(0, weight=2)
        self.chat_frame.columnconfigure(1, weight=1)
        self.chat_frame.rowconfigure(0, weight=1)

        self.master.columnconfigure(0,weight=7)
        self.master.columnconfigure(1,weight=7)
        self.master.columnconfigure(2,weight=1)
        self.master.columnconfigure(3,weight=7)
        self.master.rowconfigure(0,weight=1)
        self.master.rowconfigure(1,weight=10)
        self.master.rowconfigure(2,weight=5)

    def scrape(self):
        #use cmd to run requests
        cmd='request.exe'
        p=subprocess.Popen(cmd,shell=True)
        return_code=p.wait()  #wait for the end of subprocess

        #read json to get data from the website
        with open("data.json","r",encoding = "utf-8") as data:
            self.datacontents = json.load(data)
        for data_item in self.datacontents:
            self.titles.append(data_item["title"])
        self.indexs = range(len(self.titles))
        self.var2.set(tuple(self.indexs))

        # Add items from the list to the Treeview widget
        for i, item in enumerate(self.titles):
            self.tree.insert("", "end", values=(i, item))

        #change the label
        self.var1.set("Already load")

    def startbot(self):
        #get listbox value
        value = self.listbox.curselection()
        print(value)
        if value:
            self.value = self.listbox.get(value[0]) #get value from listbox

            #initiate the chatbot
            data_item = self.datacontents[self.value]
            self.title = data_item["title"]  
            self.abstract = data_item["brief"]
            self.body = data_item["body"]
            self.pdf = data_item["pdf"]
            self.context = [ {'role':'system', 'content':f"""
                You are an analyst of articles about physics. \
                Here, we have an article with title, abstract and full text which are listed below. \
                Title: '''{self.title}''' \
                Abstract:'''{self.abstract}''' \
                Text: '''{self.body}''' \
                The user will chat with you about this article. \
                Please provide information asked by the user.
                """} ]
            self.chat_history.configure(state="normal")
            self.chat_history.insert(tk.END, f"If you want to download the article\nHere is the url:{self.pdf} \n")
            self.chat_history.insert(tk.END, "Please enter your requirements.\n")
            self.chat_history.configure(state="disabled")
            self.chat_history.yview(tk.END)

    #get input and send response
    def send_message(self,event=None):
        user_input = self.user_text.get()
        if user_input:
            self.chat_history.configure(state="normal")
            self.chat_history.insert(tk.END, f"You: {user_input}\n")
            self.user_text.set("")
            self.chat_history.insert(tk.END, f"AI: {self.collect_messages(user_input)}\n")
            self.chat_history.configure(state="disabled")
            self.chat_history.yview(tk.END)

    #collect chat history in one dict
    def collect_messages(self, input): 
        self.context.append({'role':'user', 'content':f"{input}"})
        response = get_completion_from_messages(self.context) 
        self.context.append({'role':'assistant', 'content':f"{response}"})
        return response

