from crewai import Agent, Task, Crew, LLM
from crewai_tools import FileReadTool
import os
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
import logging
logging.basicConfig(level=logging.DEBUG)

os.environ["OPENAI_API_KEY"] = "NA"

# Initialize App
app = FastAPI()

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Your Next.js frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Input Model for API
class ContentInput(BaseModel):
    transcript: str
    
llm = LLM(
    model="ollama/llama3.2",
    base_url="https://precious-finch-truly.ngrok-free.app"
)

file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'content.txt')

# Initialize the file read tool
file_read_tool = FileReadTool(file_path=file_path)

input_processing_agent = Agent(
    llm=llm,
    role="Input Formatter",
    goal="Clean and structure raw content (blog posts or transcriptions) for further processing.",
    backstory=(
        "You prepare the content for the crew. Your job is to clean up, organize, and break down "
        "input into a clear format so other agents can work efficiently."
    ),
    tools=[file_read_tool],
    allow_delegation=False,
    verbose=True
)

summarization_agent = Agent(
    llm=llm,
    role="Content Condenser",
    goal="Extract the most important ideas and package them into concise, impactful summaries.",
    backstory=(
        "You focus on finding the key points in the content. Your task is to condense everything "
        "into short and clear summaries that capture the main message."
    ),
    allow_delegation=False,
    verbose=True
)

tone_adaptation_agent = Agent(
    llm=llm,
    role="Voice Designer",
    goal="Adjust language and tone to suit LinkedIn's professional yet approachable style.",
    backstory=(
        "Your job is to make sure the content sounds just right for LinkedIn. You adjust the tone to be "
        "engaging, professional, and suitable for the audience."
    ),
    allow_delegation=False,
    verbose=True
)

seo_and_hashtag_agent = Agent(
    llm=llm,
    role="Discoverability Specialist",
    goal="Enhance content visibility by integrating relevant keywords and hashtags.",
    backstory=(
        "You make the content easy to find. By adding the right hashtags and keywords, you help it reach "
        "the right audience on LinkedIn."
    ),
    allow_delegation=False,
    verbose=True
)

validation_agent = Agent(
    llm=llm,
    role="Quality Inspector",
    goal="Review content for grammar, tone, and alignment with brand guidelines.",
    backstory=(
        "You check the content to make sure it’s polished and error-free. Your task is to ensure it follows "
        "all guidelines and is ready to share."
    ),
    allow_delegation=False,
    verbose=True
)


input_processing_task = Task(
    llm=llm,
    description=(
        "Take raw input content, such as a blog post or webinar transcription, and clean it up. "
        "Remove unnecessary elements like typos, redundant sections, and formatting issues. "
        "Segment the content into smaller, logically structured chunks for downstream processing.\n"
        "Ensure the content is properly formatted and error-free before passing it to other agents."
    ),
    expected_output=(
        "A cleaned and structured version of the input content, segmented into smaller, logical chunks. "
        "The output should be free of errors and unnecessary content, ready for further processing."
    ),
    agent=input_processing_agent,
)


summarization_task = Task(
    llm=llm,
    description=(
        "Analyze the processed content to identify the key points and main ideas. "
        "Create a concise summary that captures the essence of the content while retaining its core message.\n"
        "Focus on highlighting the most impactful ideas and avoiding unnecessary details."
    ),
    expected_output=(
        "A short, clear, and accurate summary of the content, focusing on the most important points. "
        "The summary should be ready to use as a foundation for LinkedIn posts."
    ),
    agent=summarization_agent,
)


tone_adaptation_task = Task(
    llm=llm,
    description=(
        "Take the summarized content and adjust its language and tone to fit LinkedIn's professional yet conversational style. "
        "Ensure the tone is engaging and aligns with the platform’s audience while maintaining the message's clarity.\n"
        "Adapt the content to be approachable, impactful, and well-suited for professional readers."
    ),
    expected_output=(
        "A revised version of the content, adjusted for tone and language. "
        "The output should be polished, engaging, and appropriate for LinkedIn."
    ),
    agent=tone_adaptation_agent,
)


seo_and_hashtag_task = Task(
    llm=llm,
    description=(
        "Enhance the LinkedIn-ready content by identifying and adding relevant keywords and hashtags. "
        "Use current trends, industry-specific terms, and popular hashtags to improve content visibility.\n"
        "Ensure the hashtags and keywords align with the content and help it reach the target audience effectively."
    ),
    expected_output=(
        "Content with a list of strategically chosen keywords and hashtags integrated seamlessly. "
        "The output should be optimized for LinkedIn visibility and audience reach."
    ),
    agent=seo_and_hashtag_agent,
)


validation_task = Task(
    llm=llm,
    description=(
        "Review the finalized content to ensure it is free of grammatical errors, maintains the desired tone, "
        "and aligns with brand guidelines. Perform a thorough quality check for coherence and professionalism.\n"
        "Ensure the content is ready for publishing with no errors or inconsistencies."
    ),
    expected_output=(
        "A fully reviewed and polished version of the content, error-free and ready for publishing. "
        "The output should meet all quality and brand standards."
    ),
    agent=validation_agent,
)




final_polisher_agent = Agent(
    llm=llm,
    role="Content Finisher",
    goal="Transform the draft content into a final polished version that is engaging, concise, and impactful, using a structured, point-wise style.",
    backstory=(
        "You are the final touchpoint in the content creation process. "
        "Your job is to take refined drafts and make them shine. "
        "Using a structured, point-wise approach, you ensure clarity, engagement, and alignment "
        "with the desired tone and purpose."
    ),
    allow_delegation=False,
    verbose=True
)

final_polishing_task = Task(
    llm=llm,
    description=(
        "Analyze the content provided and rewrite it in a point-wise and structured manner. "
        "Ensure each idea is expressed clearly, concisely, and with impact. "
        "Focus on creating an engaging and easy-to-follow format that is suitable for professional and social platforms."
    ),
    expected_output=(
        "A clean, structured version of the content with key ideas expressed in bullet points or short paragraphs. "
        "The output should be concise, engaging, and ready for publishing."
        "Use appropriate emojis to add visual appeal"
    ), 
    agent=final_polisher_agent,
)

crew = Crew(
    agents=[input_processing_agent, 
            summarization_agent,
            final_polisher_agent],
    
    tasks=[input_processing_task, 
           summarization_task,
           final_polishing_task],
	
    verbose=True,
	memory=True
)

# Store Results
results_cache = {}


@app.post("/process-content")
async def process_content(content_input: ContentInput):
    """Starts the content processing workflow."""
    global results_cache

    logging.debug("Received raw content: %s", content_input.transcript)
        # Validate that the content is not empty or only whitespace
    cleaned_content = content_input.transcript.strip()
    if not cleaned_content:
        raise HTTPException(status_code=422, detail="Content cannot be empty or just whitespace.")
  
    processed_content = cleaned_content.replace("'", "\\'")  # Escaping single quotes if needed

    # Update file content dynamically
    with open(file_path, 'w') as file:
        file.write(processed_content)

    try:
        result = crew.kickoff()
        # Cache results
        results_cache["latest"] = result
        # Return the result directly
        return {"status": "success", "message": "Content processed successfully!", "result": result}
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))




