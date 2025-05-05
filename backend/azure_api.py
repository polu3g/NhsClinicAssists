import os
import time
from openai import AzureOpenAI
from dotenv import load_dotenv

load_dotenv()
# Ensure you have the required environment variables set
client = AzureOpenAI(
    azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"),
    api_key=os.getenv("AZURE_OPENAI_API_KEY"),
    api_version="2024-05-01-preview"
)

# Assistant instance is created once for performance
assistant = client.beta.assistants.create(
    model="gpt-4o-mini",  # Replace with your deployment name
    instructions=(
        "You are a clinically safe, empathetic, and professional AI assistant developed to support NHS GP clinics in non-urgent "
        "triage and structured patient follow-up. You provide accurate, evidence-based guidance aligned with NICE clinical guidelines "
        "and use SNOMED CT terminology when relevant. Your role is to assist with initial patient symptom triage, automate follow-up steps, "
        "and generate clear clinical summaries to reduce administrative burden and improve care continuity. "
        "Be polite, grounded in clinical standards, and transparent about when to escalate to a human clinician. "
        "Engage patients with compassion and clarity, using plain language where possible, while maintaining professional tone suitable "
        "for NHS care environments. If unsure or outside your scope, advise the patient to contact their GP directly. "
        "Format all responses in HTML suitable for safe embedding in a web-based chat interface. Use <strong>, <ul>, <p>, and other standard tags "
        "for readability, but avoid inline styles or scripts."
    ),
    tools=[{"type": "file_search"}],
    tool_resources={"file_search": {"vector_store_ids": ["vs_2wCXgSABvPuHtCoknfus0Ikj"]}},
    temperature=0.7,
    top_p=1
)

def query_azure_api(query: str) -> str:
    try:
        # Create a new thread
        thread = client.beta.threads.create()

        # Add the user's message
        client.beta.threads.messages.create(
            thread_id=thread.id,
            role="user",
            content=query
        )

        # Run the assistant
        run = client.beta.threads.runs.create(
            thread_id=thread.id,
            assistant_id=assistant.id
        )

        # Wait for completion
        while run.status in ['queued', 'in_progress', 'cancelling']:
            time.sleep(1)
            run = client.beta.threads.runs.retrieve(
                thread_id=thread.id,
                run_id=run.id
            )

        if run.status == 'completed':
            messages = client.beta.threads.messages.list(thread_id=thread.id)

            # Find the assistant's response
            for message in reversed(messages.data):
                if message.role == "assistant":
                    for content in message.content:
                        if content.type == "text":
                            return content.text.value
        elif run.status == 'requires_action':
            return "Assistant requires additional input or function call."
        else:
            return f"Assistant failed with status: {run.status}"
    except Exception as e:
        return f"Error during Azure API query: {str(e)}"
