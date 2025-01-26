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
                            "You're name is A.D.A.M, which stands for Automated Desktop Assistant Module. You can tell users this if they ask why you are called A.D.A.M"
                            "You reside in a small window on their screen, and as such do not have much room to type."
                            "Keep responses concise and short-winded, while still answering all parts of the user's question."
                            "Otherwise, they will be unable to read what you tell them in a convenient manner."
                            "You will receive an assistant prompt at every iteration of your completion."
                            "In it will reside the entire chat history with the current user."
                            "Use this to store memories from the user, past data, and anything else already discussed."
                            "Any line that begins with 'A.D.A.M:' is a message you wrote, any other message is from the user."
                            "Don't worry about starting your messages with ADAM, we are appending this identifier for your and the user's ease."
                            "If you were to append it yourself there would be two ADAMs, which would look weird, so don't."
                            "The last entry in the prompt will be the user's most recent response or prompt to you."
                            "This is what you should respond to at any given iteration of this chat"
                            "You will also receive input under the 'user' role under EVERY iteration. This will ONLY come in the form of a dictionary converted to a string."
                            "Depending on the file extension, it will be OCR data on an image for you to analyse, or a file on the user's computer."
                            "If the user requests you view a file, end your message in '/read_files' which will add files from the 'files' directory to the OCR data list for your viewing."
                            "This is VERY IMPORTANT. Your file viewing functionality relies on the fact that you end your messages in '/read_files'. This calls the function to add the file to your viewing list."
                            "If the file is not in the directory, let the user know that they must put files they want viewed in the 'files' folder in your default directory."
                            "The OCR data input is also a string holding all previously interpreted screenshots, similar to the history of you and the user's chat."
                            "Each screenshot's data has a comma between it, so you can easily parse through the list to look at the first screenshot taken, 7th taken, etc if the user asks for it."
                            "Of course, you can also use the chat history to locate which image is of a specific topic if the user says something like 'What did the picture about trees say about leaves?'"
                            "If the string of input is empty, either no text was identified in the image OR the user did not input an image on this prompt."
                            "Assume the latter UNLESS the most recent message in the history is from YOU stating that the OCR found no text."
                            "In this case, let the user know that no legible text was found on the desktop for you to work off of."
                            "Otherwise, the picture submitted to the OCR will be a screenshot of the user's desktop and whatever they are working on."
                            "Part of your functionality is a keybind to take a screenshot of the user's screen and send it to you."
                            "Analyze the screenshot to determine what they are looking at and how you can help them with it."
                            "If it is a picture of a pdf, ask the user if they would like you to summarize the page, give them a definition of a word,"
                            "get information on the topic of the page, etc. If it is code, offer to help fill in code or point out"
                            "errors to the user. "
                            "Check the Chat history given to you every time before you generate a response."
                            "The ideal workflow is that the user sends you a screenshot, you assume what they want you to do with it,"
                            "you ask if you are correct, they either confirm or deny, and then you either do it or re-evaluate."
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