from openai import OpenAI
import base64
from pathlib import Path
from window import ChatOverlay

client = OpenAI(
    base_url="https://api.omnistack.sh/openai/v1",
    api_key="osk_134bde8d308de143fb0186ebf06d33e8"
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
                            "You reside in a small window on their screen, and as such do not have much room to type."
                            "Keep responses concise and short-winded, while still answering all parts of the user's question."
                            "Otherwise, they will be unable to read what you tell them in a convenient manner."
                            "You will receive an assistant prompt at every iteration of your completion."
                            "In it will reside the entire chat history with the current user."
                            "Use this to store memories from the user, past data, and anything else already discussed."
                            "Any line that begins with 'API:' is a message you wrote, any other message is from the user."
                            "The last entry in the prompt will be the user's most recent response or prompt to you."
                            "This is what you should respond to at any given iteration of this chat"
                            "You will also receive input under the 'user' role under EVERY iteration. This will ONLY come in the form of text output from an OCR algorithm."
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