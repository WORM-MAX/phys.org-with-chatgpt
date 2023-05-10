from utils import *
import openai

openai.api_key  = 

#Text display in GUI
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



# Create the Tkinter app
root = tk.Tk()
root.title("Chatbot") 
root.geometry("1400x800+50+20")
root.resizable(width=True, height=True)
app = ChatApp(root,tips)
root.mainloop()