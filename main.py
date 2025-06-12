# import os
# import csv
# from dotenv import load_dotenv
# import chainlit as cl
# from typing import cast
# from agents import Agent, Runner, AsyncOpenAI, OpenAIChatCompletionsModel
# from agents.run import RunConfig

# # Load environment variables
# load_dotenv()

# gemini_api_key = os.getenv("GEMINI_API_KEY")
# if not gemini_api_key:
#     raise ValueError("GEMINI_API_KEY environment variable is not set.")

# # Helper: Load NGI prices from CSV and return markdown table
# def load_ngi_prices_from_csv(csv_path="data/NGI_Prices.csv") -> str:
#     try:
#         with open(csv_path, mode="r", encoding="utf-8") as file:
#             reader = csv.reader(file)
#             rows = list(reader)
#             if not rows:
#                 return "⚠️ NGI price list is empty."
#             header = rows[0]
#             data = rows[1:]
#             markdown = "| " + " | ".join(header) + " |\n"
#             markdown += "| " + " | ".join(["---"] * len(header)) + " |\n"
#             for row in data:
#                 markdown += "| " + " | ".join(row) + " |\n"
#             return markdown
#     except Exception as e:
#         return f"⚠️ Unable to load NGI price list: {e}"


# # Helper: Load Methaq prices from CSV and return markdown table
# def load_methaq_prices_from_csv(csv_path="data/Methaq_Prices.csv") -> str:
#     try:
#         with open(csv_path, mode="r", encoding="utf-8") as file:
#             reader = csv.reader(file)
#             rows = list(reader)
#             if not rows:
#                 return "⚠️ Methaq price list is empty."
#             header = rows[0]
#             data = rows[1:]
#             markdown = "| " + " | ".join(header) + " |\n"
#             markdown += "| " + " | ".join(["---"] * len(header)) + " |\n"
#             for row in data:
#                 markdown += "| " + " | ".join(row) + " |\n"
#             return markdown
#     except Exception as e:
#         return f"⚠️ Unable to load Methaq price list: {e}"



# @cl.on_chat_start
# async def start():
#     external_client = AsyncOpenAI(
#         api_key=gemini_api_key,
#         base_url="https://generativelanguage.googleapis.com/v1beta/openai/",
#     )

#     model = OpenAIChatCompletionsModel(
#         model="gemini-2.0-flash",
#         openai_client=external_client,
#     )

#     config = RunConfig(
#         model=model,
#         model_provider=external_client,
#         tracing_disabled=True
#     )

#     cl.user_session.set("chat_history", [])
#     cl.user_session.set("config", config)

#     agent: Agent = Agent(
#         name="Assistant",
#         instructions="""
# You are a sales assistant for **Methaq Motor Insurance Company**. You help users with **motor insurance inquiries**, especially related to **Methaq and NGI motor insurance**.

# ✅ You can assist with both **Methaq** and **NGI** motor insurance pricing and policies.

# 📄 If the user asks about **NGI prices**, load the NGI motor insurance price list and display it.

# 💡 NGI and Methaq are both available through our portal — you're here to help the user choose the right one based on their vehicle and needs.

# ⏳ Methaq policies are issued within 5 to 10 minutes.
# ⏳ NGI policies are issued within 1 to 2 hours.


# ❌ If the user asks anything unrelated to motor insurance (e.g., health, travel, life, etc.), reply:
# "Sorry, I can only assist with motor insurance policies. For other help, please contact our support team on WhatsApp: https://wa.me/971543984710?text=Hello%2C%20I%20need%20help%20with%20motor%20insurance.


# "
#         """,
#         model=model,
#     )

#     cl.user_session.set("agent", agent)

#     await cl.Message(content="Welcome to the Methaq Motor Insurance Chatbot! We offer both Methaq and NGI motor insurance. How can I assist you today?").send()

# @cl.on_message
# async def main(message: cl.Message):
#     history = cl.user_session.get("chat_history") or []
#     agent = cast(Agent, cl.user_session.get("agent"))
#     config = cast(RunConfig, cl.user_session.get("config"))

#     history.append({"role": "user", "content": message.content})

#     msg = cl.Message(content="")
#     await msg.send()

#     # Check if NGI price info requested
#     if "ngi" in message.content.lower() and "price" in message.content.lower():
#         ngi_prices = load_ngi_prices_from_csv()
#         await cl.Message(
#             content=(
#                 "Here is the NGI motor insurance price list:\n\n" + ngi_prices
#             )
#         ).send()
#          # Check if Methaq price info requested
#     if "methaq" in message.content.lower() and "price" in message.content.lower():
#         methaq_prices = load_methaq_prices_from_csv()
#         await cl.Message(
#             content=(
#                 "Here is the Methaq motor insurance price list:\n\n" + methaq_prices
#             )
#         ).send()


#         await cl.Message(content="Want to speak with a Support Team? [Click to chat on WhatsApp](https://wa.me/971543984710?text=Hello%2C%20I%20need%20help%20with%20motor%20insurance.)").send()


#     try:
#         result = Runner.run_streamed(agent, history, run_config=config)
#         async for event in result.stream_events():
#             if event.type == "raw_response_event" and hasattr(event.data, 'delta'):
#                 token = event.data.delta
#                 await msg.stream_token(token)

#         history.append({"role": "assistant", "content": msg.content})
#         cl.user_session.set("chat_history", history)

#     except Exception as e:
#         await msg.update(f"Error: {str(e)}")


import os
import csv
from dotenv import load_dotenv
import chainlit as cl
from typing import cast
from agents import Agent, Runner, AsyncOpenAI, OpenAIChatCompletionsModel
from agents.run import RunConfig

# Load environment variables
load_dotenv()


gemini_api_key = os.getenv("GEMINI_API_KEY")
if not gemini_api_key:
    raise ValueError("GEMINI_API_KEY environment variable is not set.")

# Load NGI Prices from CSV
def load_ngi_prices_from_csv(csv_path="data/NGI_Prices.csv") -> str:
    try:
        with open(csv_path, mode="r", encoding="utf-8") as file:
            reader = csv.reader(file)
            rows = list(reader)
            if not rows:
                return "⚠️ NGI price list is empty."
            header = rows[0]
            data = rows[1:]
            markdown = "| " + " | ".join(header) + " |\n"
            markdown += "| " + " | ".join(["---"] * len(header)) + " |\n"
            for row in data:
                markdown += "| " + " | ".join(row) + " |\n"
            return markdown
    except Exception as e:
        return f"⚠️ Unable to load NGI price list: {e}"

# Load Methaq Prices from CSV
def load_methaq_prices_from_csv(csv_path="data/Methaq_Prices.csv") -> str:
    try:
        with open(csv_path, mode="r", encoding="utf-8") as file:
            reader = csv.reader(file)
            rows = list(reader)
            if not rows:
                return "⚠️ Methaq price list is empty."
            header = rows[0]
            data = rows[1:]
            markdown = "| " + " | ".join(header) + " |\n"
            markdown += "| " + " | ".join(["---"] * len(header)) + " |\n"
            for row in data:
                markdown += "| " + " | ".join(row) + " |\n"
            return markdown
    except Exception as e:
        return f"⚠️ Unable to load Methaq price list: {e}"

# Chat starts
@cl.on_chat_start
async def start():
    external_client = AsyncOpenAI(
        api_key=gemini_api_key,
        base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
    )

    model = OpenAIChatCompletionsModel(
        model="gemini-2.0-flash",
        openai_client=external_client
    )

    config = RunConfig(
        model=model,
        model_provider=external_client,
        tracing_disabled=True
    )

    cl.user_session.set("chat_history", [])
    cl.user_session.set("config", config)

    agent: Agent = Agent(
        name="Assistant",
        instructions="""
You are a sales assistant for **Methaq Motor Insurance Company**. You help users with **motor insurance inquiries**, especially related to **Methaq and NGI motor insurance**.

✅ You can assist with both **Methaq** and **NGI** motor insurance pricing and policies.

📄 If the user asks about **NGI prices**, load the NGI motor insurance price list and display it.

💡 NGI and Methaq are both available through our portal — you're here to help the user choose the right one based on their vehicle and needs.

⏳ Methaq policies are issued within 5 to 10 minutes.
⏳ NGI policies are issued within 1 to 2 hours.

❌ If the user asks anything unrelated to motor insurance (e.g., health, travel, life, etc.), reply:
"Sorry, I can only assist with motor insurance policies. For other help, please contact our support team on WhatsApp: https://wa.me/971543984710?text=Hello%2C%20I%20need%20help%20with%20motor%20insurance."
        """,
        model=model
    )

    cl.user_session.set("agent", agent)

    await cl.Message(
        content="🚗 Welcome to the Methaq Motor Insurance Chatbot!\nWe offer both **Methaq** and **NGI** motor insurance.\n\nHow can I assist you today?"
    ).send()

# On message
@cl.on_message
async def main(message: cl.Message):
    history = cl.user_session.get("chat_history") or []
    agent = cast(Agent, cl.user_session.get("agent"))
    config = cast(RunConfig, cl.user_session.get("config"))

    user_input = message.content.lower()
    history.append({"role": "user", "content": message.content})

    msg = cl.Message(content="")
    await msg.send()

    # Handle unrelated topics
    unrelated_keywords = ["health", "life", "travel", "medical", "home"]
    if any(keyword in user_input for keyword in unrelated_keywords):
        await cl.Message(
            content="""❌ Sorry, I can only assist with **motor insurance** policies.
📱 For other insurance types, please contact our support team on WhatsApp:
👉 [Click here](https://wa.me/971543984710?text=Hello%2C%20I%20need%20help%20with%20motor%20insurance.)
"""
        ).send()
        return

    # Show Methaq prices
    if "methaq" in user_input and "price" in user_input:
        methaq_prices = load_methaq_prices_from_csv()
        await cl.Message(
            content=f"📋 **Methaq Motor Insurance Price List:**\n\n{methaq_prices}"
        ).send()

        await cl.Message(
            content="💬 Want to speak with support?\n👉 [Chat on WhatsApp](https://wa.me/971543984710?text=Hello%2C%20I%20need%20help%20with%20motor%20insurance.)"
        ).send()
        return

    # Show NGI prices
    if "ngi" in user_input and "price" in user_input:
        ngi_prices = load_ngi_prices_from_csv()
        await cl.Message(
            content=f"📋 **NGI Motor Insurance Price List:**\n\n{ngi_prices}"
        ).send()
        return

    # General quote inquiry
    if "quote" in user_input or "insurance" in user_input:
        await cl.Message(
            content="""
📝 To get a quote, please share:
- 🚘 Vehicle make & model
- 📅 Year of manufacture
- 👤 Your age
- 🚦 Driving experience
- 📊 Any accident history?
"""
        ).send()
        return

    # General AI response via LLM
    try:
        result = Runner.run_streamed(agent, history, run_config=config)
        async for event in result.stream_events():
            if event.type == "raw_response_event" and hasattr(event.data, 'delta'):
                token = event.data.delta
                await msg.stream_token(token)

        history.append({"role": "assistant", "content": msg.content})
        cl.user_session.set("chat_history", history)

    except Exception as e:
        await msg.update(f"❌ Error: {str(e)}")
