from openai import OpenAI
import base64
from pathlib import Path
from window import ChatOverlay
import os

cwd = os.getcwd()
file_path = cwd+"/.secret/api_key.txt"
with open(file_path, "r") as file:
    key = file.read()

client = OpenAI(
    base_url="https://api.omnistack.sh/openai/v1",
    api_key=key
)

class ChatAPI():
    def messageQuery(self, chatHistory, ocrData):
        history = ""
        for i in chatHistory:
            history = history + "\n" + i
        completion = client.chat.completions.create(
            model="general_pansy_jettie",
            messages=[
                {
                    "role": "developer",
                    "content": [
                        {
                            "type": "text", 
                            "text": "You are a helpful assistant tool for users to use on their desktops."
                            "Be concise in all responses."
                            "You're name is ADAM, which stands for Automated Desktop Assistant Module. You can tell users this if they ask why you are called ADAM"
                            "You will receive an assistant prompt at every iteration of your completion with the entire chat history with the current user."
                            "The last entry in the prompt will be the user's most recent response or prompt to you."
                            "This is what you should respond to at any given iteration of this chat"
                            "You will also receive input under the 'user' role under EVERY iteration. This will ONLY come in the form of a dictionary converted to a string."
                            "Depending on the file extension, it will be OCR data on an image for you to analyse, or a file from the user's computer."
                            "Assume that the file has already been put in the directory by the user if they ask you to read it, and attempt to read it. If you really think its not there, let them know they have to put it in the 'files' folder in your default directory."
                            "Note that files will NOT be updated in your list of data unless you do it. You should, as such, call your function to update files before accessing them in case they've been edited."
                            "The OCR data input is also a string holding all previously interpreted screenshots, similar to the history of you and the user's chat."
                            "Each screenshot's data has a comma between it, so you can easily parse through the list to look at the first screenshot taken, 7th taken, etc if the user asks for it."
                            "Of course, you can also use the chat history to locate which image is of a specific topic if the user says something like 'What did the picture about trees say about leaves?'"
                            "Part of your functionality is a keybind to take a screenshot of the user's screen and send it to you."
                            "If the string of input is empty, either no text was identified in the image OR the user did not input an image on this prompt."
                            "Assume the latter UNLESS the most recent message in the history is from YOU stating that the OCR found no text."
                            "In this case, let the user know that no legible text was found on the desktop for you to work off of."
                            "Otherwise, the picture submitted to the OCR will be a screenshot of the user's desktop and whatever they are working on."
                            "Analyze the screenshot to determine what they are looking at and how you can help them with it."
                            "Check the Chat history given to you every time before you generate a response."
                            "Lines that you wrote will be labeled for you with 'ADAM: ' any other message is from the user."
                            "Do NOT start your messages with 'ADAM', we are appending this identifier for your and the user's ease."
                            "If you end your message in /read_files, a function will be called that imports a file to your OCR data list to view." 
                            "This is VERY IMPORTANT. Your file viewing functionality relies on the fact that you utilize ending your message in /read_files to call the function."
                            "Do not use unneccesary quotations, remember for /read_file it must be at the very end of your message with no punctuation following it."
                        },
                    ]
                },
                                {
                    "role": "assistant",
                    "content": [
                        {
                            "type": "text", 
                            "text": history
                        },
                    ]
                },
                                {
                    "role": "user",
                    "content": [
                        {
                            "type": "text", 
                            "text": ocrData
                        },
                    ]
                }
            ]
        )
        return completion.choices[0].message.content



'''TEMPLATE FOR CHAT RESPONSE GENERATION

Deprecated Image Upload Syntax: {"url": f"data:image/jpeg;base64,{encoded_image}"}

completion = client.chat.completions.create(
    model="general_pansy_jettie",
    messages=[
        {
            "role": "user",
            "content": [
                {
                    "type": "text", 
                    "text": "What's in the code in this image?"
                },
                {
                    "type": "text",
                    "text": test
                },
            ]
        }
    ]
)
'''