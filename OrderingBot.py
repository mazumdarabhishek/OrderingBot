import time
import openai
def initialize_chatbot(api_key):
    openai.api_key = api_key

def get_completion_from_messages(messages, model="gpt-3.5-turbo", temperature=0):
    response = openai.ChatCompletion.create(
        model=model,
        messages=messages,
        temperature=temperature, # this is the degree of randomness of the model's output
    )
#     print(str(response.choices[0].message))
    return response.choices[0].message["content"]

def chat(api_key):
    # Initialize chatbot
    initialize_chatbot(api_key)
    print("Chatbot initialized. Start chatting!\n")
    
    collect_conversation = [
        {
            'role': 'system',
            'content': """
            You are OrderBot, an automated service to collect orders for a Indian burger restaurant.\
            You first greet the customer, then collects the order, \
            and then asks if it's a dine-in or parcel. \
            You wait to collect the entire order, then summarize it and check for a final \
            time if the customer wants to add anything else. \
            If it's a parcel, you add packaging cost of 10 to the total cost. \
            calculate the total by displaying the break-up and then display the total amount.\
            Finally you display the total amount with breakdown of cost and ask the customer to make UPI payment.\
            Make sure to clarify all options, extras and sizes to uniquely \
            At the end utter the words "Order Complete!"\
            identify the item from the menu.\
            You respond in a short, very conversational friendly style. \ 
            The menu includes: \
            veggie burger  60.0, 80.0, 100.0 \
            veggie cheese burger   80.0, 100.0, 120.0 \
            chicken burger   120.0, 140.0, 180.0 \
            fries 80.0, 100.0 \
            greek salad 80.00 \
            Add-ons: \
            extra cheese 25.00, \
            mushrooms 30.0 \
            sausage 50.00 \
            hot sauce 15.0 \
            Drinks: \
            coke 50.00, 57.00, 100.00 \
            sprite 50.00, 57.00, 100.00 \
            bottled water 20.00 \
            """
        }
    ]
    # Loop through conversation until chatbot outputs "Order Complete"
    # bot_response = get_completion_from_messages(messages= collect_conversation)
    # print("OrderBot: ", bot_response)
    while True:
        # Get user input
        user_input = input("User: ")
        collect_conversation.append({'role':'user', 'content': user_input})
        # Pass user input to chatbot and get response
        bot_response = get_completion_from_messages(messages= collect_conversation)
        collect_conversation.append({'role':'assistant', 'content': bot_response})
        print(f"\nChatbot: {bot_response}\n")

        # Check if chatbot output "Order Complete"
        if "complete" in bot_response.lower():
            recept_prompt = """
            create a JSON summary of previous food order with the following information:
            - burger, include size
            - list of add-ons
            - list of drinks, include size
            - list of sides, include size
            - total price
            - type of order, dine-in or parcel
            """
            collect_conversation.append({'role':'system', 'content': recept_prompt})
            bot_response = get_completion_from_messages(messages= collect_conversation)
            print(f"Order Receipt::\n{bot_response}")
            break

        # Wait for a short period of time before continuing conversation
        time.sleep(1)

if __name__ == "__main__":
    # Ask user to input API key
    api_key = input("Please enter your API key: ")

    # Start chat with user-provided API key
    chat(api_key)
