import asyncio

from task.clients.client import DialClient
from task.clients.custom_client import CustomDialClient
from task.constants import DEFAULT_SYSTEM_PROMPT
from task.models.conversation import Conversation
from task.models.message import Message
from task.models.role import Role


async def start(stream: bool) -> None:
    #TODO:
    # 1.1. Create DialClient
    # (you can get available deployment_name via https://ai-proxy.lab.epam.com/openai/models
    #  you can import Postman collection to make a request, file in the project root `dial-basics.postman_collection.json`
    #  don't forget to add your API_KEY)
    # 1.2. Create CustomDialClient
    # 2. Create Conversation object
    # 3. Get System prompt from console or use default -> constants.DEFAULT_SYSTEM_PROMPT and add to conversation
    #    messages.
    # 4. Use infinite cycle (while True) and get yser message from console
    # 5. If user message is `exit` then stop the loop
    # 6. Add user message to conversation history (role 'user')
    # 7. If `stream` param is true -> call DialClient#stream_completion()
    #    else -> call DialClient#get_completion()
    # 8. Add generated message to history
    # 9. Test it with DialClient and CustomDialClient
    # 10. In CustomDialClient add print of whole request and response to see what you send and what you get in response
    
    # 1.1 and 1.2: Create clients (using gpt-4o as the default model)
    client = DialClient(deployment_name="gpt-4o")
    # Uncomment the line below to test CustomDialClient
    # client = CustomDialClient(deployment_name="gpt-4o")
    
    # 2. Create Conversation object
    conversation = Conversation()
    
    # 3. Get System prompt from console or use default
    print("Provide System prompt or press 'enter' to continue.")
    system_prompt = input("> ").strip()
    if not system_prompt:
        system_prompt = DEFAULT_SYSTEM_PROMPT
    
    # Add system message to conversation
    system_message = Message(role=Role.SYSTEM, content=system_prompt)
    conversation.add_message(system_message)
    
    print("\nType your question or 'exit' to quit.")
    
    # 4. Infinite cycle
    while True:
        # Get user input
        user_input = input("> ").strip()
        
        # 5. If user message is 'exit', stop the loop
        if user_input.lower() == 'exit':
            print("Exiting the chat. Goodbye!")
            break
        
        if not user_input:
            continue
        
        # 6. Add user message to conversation history
        user_message = Message(role=Role.USER, content=user_input)
        conversation.add_message(user_message)
        
        # 7. Call appropriate completion method based on stream parameter
        try:
            if stream:
                ai_message = await client.stream_completion(conversation.get_messages())
            else:
                ai_message = client.get_completion(conversation.get_messages())
            
            # 8. Add generated message to history
            conversation.add_message(ai_message)
            print()
        except Exception as e:
            print(f"Error: {e}")
            # Remove the user message if there was an error
            conversation.messages.pop()


asyncio.run(
    start(True)
)
