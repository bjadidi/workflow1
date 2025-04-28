import boto3
import os
import json
from dotenv import load_dotenv
from openai import OpenAI
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# load prompt engineering context
def load_prompt_context():
    """
    Loads prompt engineering context or guidelines from a text file.
    """
    try:
        with open("prompt_context.txt", "r") as file:
            return file.read()
    except FileNotFoundError:
        return ""


def get_material_details(material_type):
    """
    Fetches material details using AWS Bedrock's Claude-3 Sonnet model via the Messages API.

    Parameters:
        material_type (str): The type of material to query.

    Returns:
        str: Generated text response from the model.
    """
    try:
        # Initialize the Bedrock runtime client
        client = boto3.client(
            'bedrock-runtime',
            region_name=os.getenv('AWS_REGION'),  # Ensure the region is set
            aws_access_key_id=os.getenv('AWS_ACCESS_KEY_ID'),
            aws_secret_access_key=os.getenv('AWS_SECRET_ACCESS_KEY')
        )

        # Define the conversation as a list of messages (Claude-3 requires Messages API)
        messages = [
            {"role": "user", "content": f"Tell me about the material: {material_type}. Provide a brief description including its properties, uses, and sustainability aspects. Give me only 1 sentence for response!"}
        ]

        # messages = [
        #     {"role": "user", "content": f"{material_type}. Give me only 1 sentence for response!"}
        # ]
        # Prepare request payload for Messages API
        payload = json.dumps({
            "anthropic_version": "bedrock-2023-05-31",  # Required for Claude in Bedrock
            "messages": messages,  # Use messages instead of prompt
            "max_tokens": 500,  # Controls response length
            "temperature": 0.5,  # Adjust randomness
        })

        # Invoke the model (Claude-3 requires Messages API)
        response = client.invoke_model(
            modelId="anthropic.claude-3-sonnet-20240229-v1:0",
            body=payload,
            accept="application/json",
            contentType="application/json"
        )

        # Parse the response
        response_body = json.loads(response['body'].read().decode("utf-8"))

        # Extract the generated text (Claude-3 responses are under 'content')
        details = response_body["content"][0]["text"] if "content" in response_body else "No details found."
        return details

    except Exception as e:
        return f"Error retrieving material details: {str(e)}"
    

# Function to get answer from ZYAssistant
def get_answer_from_zya(user_input):
    """
    Fetches answer from ZYAssistant using AWS Bedrock's Claude-3 Sonnet model via the Messages API.

    Parameters:
        user_input (str): The user's input question.

    Returns:
        str: Generated text response from the model.
    """
    try:
        # Initialize the Bedrock runtime client
        client = boto3.client(
            'bedrock-runtime',
            region_name=os.getenv('AWS_REGION'),  # Ensure the region is set
            aws_access_key_id=os.getenv('AWS_ACCESS_KEY_ID'),
            aws_secret_access_key=os.getenv('AWS_SECRET_ACCESS_KEY')
        )

        # Load prompt context
        context = load_prompt_context()
        messages = [
            {"role": "user", "content": f"{context}\n{user_input}. Provide a 1-sentence description of its properties, uses, and sustainability aspects."}
        ]

        payload = json.dumps({
            "anthropic_version": "bedrock-2023-05-31",
            "messages": messages,
            "max_tokens": 500,
            "temperature": 0.5,
        })
        
        # Invoke the model
        response = client.invoke_model(
            modelId="anthropic.claude-3-sonnet-20240229-v1:0",
            body=payload,
            accept="application/json",
            contentType="application/json"
        )
        
        response_body = json.loads(response['body'].read().decode("utf-8"))
        details = response_body["content"][0]["text"] if "content" in response_body else "No details found."
        return details
    
    except Exception as e:
        return f"Error retrieving material details: {str(e)}"

def call_llm(user_input, prompt, llm_model_name):
    """
    Calls a specified LLM model using AWS Bedrock's Messages API.

    Parameters:
        user_input (str): The user's input question.
        prompt (str): The prompt to provide context for the LLM.
        llm_model_name (str): The name of the LLM model to invoke.

    Returns:
        str: Generated text response from the model.
    """
    try:
        if "gpt" in llm_model_name.lower():
            # Create OpenAI client
            client = OpenAI()
            
        else:
            # Initialize the Bedrock runtime client
            client = boto3.client(
                'bedrock-runtime',
                region_name=os.getenv('AWS_REGION'),  # Ensure the region is set
                aws_access_key_id=os.getenv('AWS_ACCESS_KEY_ID'),
                aws_secret_access_key=os.getenv('AWS_SECRET_ACCESS_KEY')
            )

        # Define the conversation as a list of messages
        messages = [
            {"role": "user", "content": f"Based on this: \n{prompt}\n{user_input}"}
        ]

        # Prepare request payload based on the model
        if "claude" in llm_model_name.lower():
            payload = json.dumps({
                "anthropic_version": "bedrock-2023-05-31",
                "messages": messages,
                "max_tokens": 2048,  # Adjust as needed
                "temperature": 0,
            })
            # Invoke the model
            response = client.invoke_model(
            modelId=llm_model_name,
            body=payload,
            accept="application/json",
            contentType="application/json")

            # Parse the response
            response_body = json.loads(response['body'].read().decode("utf-8"))

            result = response_body["content"][0]["text"] if "content" in response_body else "No details found."

        elif "titan" in llm_model_name.lower():
            # Prepare the payload for Titan model
            input_text = f"{prompt}\n{user_input}"
            payload = json.dumps({
                "inputText": input_text,
                "textGenerationConfig": {
                    "maxTokenCount": 3072,  # Set to the desired max token count
                    "stopSequences": [],  # Add any stop sequences if needed
                    "temperature": 0,  # Adjust temperature as needed
                    "topP": 0.9  # Adjust topP as needed
                }
            })
            
            # Invoke the model
            response = client.invoke_model(
            modelId=llm_model_name,
            body=payload,
            accept="application/json",
            contentType="application/json")

            # Parse the response
            response_body = json.loads(response['body'].read().decode("utf-8"))
            result = response_body.get("results", [{}])[0].get("outputText", "No output text found.")

        elif "gpt" in llm_model_name.lower():

            response = client.chat.completions.create(
            model=llm_model_name,
            messages=[
                {"role": "system", "content": f"{prompt}"},
                {"role": "user", "content": f"{user_input}"}
            ],
            temperature=0)

            result = response.choices[0].message.content.strip()

        else:
            raise ValueError("Unsupported model specified.")

       
        return result

    except Exception as e:
        return f"Error retrieving LLM response: {str(e)}"

# Example usage
if __name__ == "__main__":
    material_info = get_material_details("PLA")
    print(material_info)
