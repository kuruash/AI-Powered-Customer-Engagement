import openai
import os
from dotenv import load_dotenv
from twilio.rest import Client
import requests
from database import insert_user  # Import database function
from database import insert_conversation
from database import get_conversation_history
from database import get_user_by_email
from database import get_conversation_history


# Load the environment variables
load_dotenv()

# OpenAI API Key
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# Twilio Credentials
TWILIO_ACCOUNT_SID = os.getenv("TWILIO_ACCOUNT_SID")
TWILIO_AUTH_TOKEN = os.getenv("TWILIO_AUTH_TOKEN")
TWILIO_PHONE_NUMBER = os.getenv("TWILIO_PHONE_NUMBER")

# Zoho CRM Credentials
ZOHO_ACCESS_TOKEN = os.getenv("ZOHO_ACCESS_TOKEN")
ZOHO_CLIENT_ID = os.getenv("ZOHO_CLIENT_ID")
ZOHO_CLIENT_SECRET = os.getenv("ZOHO_CLIENT_SECRET")
ZOHO_REFRESH_TOKEN = os.getenv("ZOHO_REFRESH_TOKEN")


# Adding OpenAI API Response Generation
def generate_ai_response(user_input):
    """Generate a chatbot response using OpenAI."""
    try:
        openai.api_key = OPENAI_API_KEY
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": user_input}]
        )
        return response["choices"][0]["message"]["content"]
    except openai.error.RateLimitError:
        return "🚨 Error: OpenAI API quota exceeded. Please check your billing and usage."
# Test AI response (to avoid excessive calls)
# print("🧠 AI Test Response:", generate_ai_response("Tell me about marketing automation."))


def send_sms(to, message):
    client = Client(os.getenv("TWILIO_ACCOUNT_SID"), os.getenv("TWILIO_AUTH_TOKEN"))
    client.messages.create(
        body=message,
        from_=os.getenv("TWILIO_PHONE_NUMBER"),
        to=to
    )

# Test SMS
# send_sms("+12408894389", "Hello! This is your AI marketing assistant.")

'''
def create_zoho_lead(name, email, phone, company):
    url = "https://www.zohoapis.com/crm/v2/Leads"
    headers = {
        "Authorization": f"Bearer {os.getenv('ZOHO_ACCESS_TOKEN')}",
        "Content-Type": "application/json"
    }
    data = {
        "data": [
            {
                "Last_Name": name.split(" ")[-1],
                "First_Name": " ".join(name.split(" ")[:-1]),
                "Email": email,
                "Phone": phone,
                "Company": company
            }
        ]
    }
    response = requests.post(url, json=data, headers=headers)
    return response.json()
'''
# Test Zoho CRM Lead Creation
# print(create_zoho_lead("John Doe", "johndoe@example.com", "+1234567890", "OpenAI Inc."))


def chatbot_loop():
    """Runs an interactive chatbot loop."""
    print("🧠 AI Marketing Chatbot Started! Type 'exit' to quit, 'history' to view past messages.")

    user_exists = input("Are you an existing user? (yes or no): ").strip().lower()

    user_id = None  # Initialize user_id

    if user_exists == "yes":
        email = input("Enter your registered Email: ").strip()
        
        # Fetch user ID based on email
        user = get_user_by_email(email)  # Function to get user ID from DB
        
        if user:
            user_id, name, phone, company = user  # Unpack details
            print(f"✅ Welcome back, {name}!")
        else:
            print("❌ No user found with this email. Please register as a new user.")
            return  # Exit if user not found

    elif user_exists == "no":
        name = input("Enter Your Name: ")
        email = input("Enter Your Email: ")
        phone = input("Enter Your Phone: ")
        company = input("Enter Your Company: ")

        # Insert new user into DB and get user_id
        user_id = insert_user(name, email, phone, company)
        print(f"✅ New user {name} registered successfully!")

    else:
        print("❌ Invalid choice. Please enter 'yes' or 'no'.")
        return

    # Start chatbot interaction
    while True:
        user_input = input("You: ").strip()
        
        if user_input.lower() == "exit":
            print("👋 Exiting Chatbot. Have a great day!")
            break

        if user_input.lower() == "history":
            history = get_conversation_history(user_id)
            print("📜 Chat History:")
            for msg, res, timestamp in history:
                print(f"🕒 {timestamp} \n👤 You: {msg} \n🤖 Bot: {res}\n")
            continue

        # Generate AI response
        response = generate_ai_response(user_input)
        
        # Store conversation in DB
        insert_conversation(user_id, user_input, response)

        print("🤖 AI:", response)

if __name__ == "__main__":
    chatbot_loop()


# Database
def create_zoho_lead(name, email, phone, company):
    url = "https://www.zohoapis.com/crm/v2/Leads"
    headers = {
        "Authorization": f"Bearer {os.getenv('ZOHO_ACCESS_TOKEN')}",
        "Content-Type": "application/json"
    }
    data = {
        "data": [
            {
                "Last_Name": name.split(" ")[-1],
                "First_Name": " ".join(name.split(" ")[:-1]),
                "Email": email,
                "Phone": phone,
                "Company": company
            }
        ]
    }
    response = requests.post(url, json=data, headers=headers)
    
    # If successful, store the data in PostgreSQL
    if response.status_code == 200:
        insert_user(name, email, phone, company)
    
    return response.json()
    
# print(create_zoho_lead("John Doe", "johndoe@example.com", "+1234567890", "OpenAI Inc."))


def chatbot_interaction(name, email, phone, company, message):
    """Handles chatbot interaction and stores user data + conversation."""
    response = generate_ai_response(message)
    
    # Store user if they are new
    user_id = insert_user(name, email, phone, company)
    
    # Store conversation in DB
    insert_conversation(user_id, message, response)
    
    return f"🤖 Chatbot: {response} (User ID: {user_id})"

