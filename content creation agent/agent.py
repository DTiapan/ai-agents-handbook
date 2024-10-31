import streamlit as st
from swarm import Swarm, Agent
from duckduckgo_search import DDGS
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()
MODEL = "llama3.2"

# Initialize Swarm client
client = Swarm()

ddgs = DDGS()

# Web search function
def search_web(query):
    print(f"Searching the web for {query}...")
    current_date = datetime.now().strftime("%Y-%m")
    results = ddgs.text(f"{query} {current_date}", max_results=10)
    if results:
        content_results = ""
        for result in results:
            content_results += f"Title: {result['title']} 🔗\nURL: {result['href']}\nDescription: {result['body']}\n\n"
        return content_results.strip()
    else:
        return f"No relevant content found for {query}."

# Agent to generate a catchy hook with emojis
hook_agent = Agent(
    name="Hook Creator",
    instructions="""Create a catchy hook with emojis for the topic provided. 
    The hook should be engaging, relatable, and capture the reader's interest in one or two sentences.
    Use relevant emojis for better impact (e.g., 💡, 🚀, 🌍, 🔥).""",
    model=MODEL
)

# Agent to search for content topics
content_search_agent = Agent(
    name="Content Search Assistant",
    instructions="Your role is to find recent and relevant articles on the specified content topics using DuckDuckGo.",
    functions=[search_web],
    model=MODEL
)

# Agent to analyze search results for content themes
content_analysis_agent = Agent(
    name="Content Analysis Assistant",
    instructions="""Your role is to organize and refine raw content search results. Focus on:
    1. Removing duplicate and redundant content
    2. Synthesizing related topics
    3. Verifying content consistency across sources
    4. Highlighting key facts and primary sources
    5. Organizing findings by priority and relevance
    6. Flagging contradictory information and preserving attributions""",
    model=MODEL
)

# Agent to craft the final content with specific requirements and emojis
content_writer_agent = Agent(
    name="Content Writer",
    instructions="""Your role is to create a clear, engaging, and polished article based on research findings. You should:
    1. Start with the hook provided.
    2. Summarize key points in bullet format with emojis for easy reading (e.g., 🔹, ✔️).
    3. Ensure the post is no more than 300 words.
    4. Ensure Each point should be on new line.
    5. Add emojis where relevant for visual appeal (e.g., 💡 for ideas, 🔗 for links, 📌 for important points).
    6. End the post with this text: 'If this sounds useful, Like 👍 and share ♻️ with your network. And don’t forget to follow me, for more easy tips and tutorials on AI!'""",
    model=MODEL
)

# Workflow for generating the content
def run_content_workflow(query):
    print("Running content creation workflow...")
    
    # Step 1: Generate a catchy hook
    hook_response = client.run(
        agent=hook_agent,
        messages=[{"role": "user", "content": f"Generate a hook for {query}"}],
    )
    hook = hook_response.messages[-1]["content"]

    # Step 2: Search for content
    content_search_response = client.run(
        agent=content_search_agent,
        messages=[{"role": "user", "content": f"Find recent content on {query}"}],
    )
    raw_content = content_search_response.messages[-1]["content"]

    # Step 3: Analyze and synthesize the search results
    content_analysis_response = client.run(
        agent=content_analysis_agent,
        messages=[{"role": "user", "content": raw_content}],
    )
    synthesized_content = content_analysis_response.messages[-1]["content"]
    
    # Step 4: Write and publish the final content with streaming
    return client.run(
        agent=content_writer_agent,
        messages=[{"role": "user", "content": f"{hook}\n\n{synthesized_content}"}],
        stream=True,  # Enable streaming
    )

# Streamlit app
def main():
    st.set_page_config(page_title="Content Creation Assistant ✍️", page_icon="✍️")
    st.title("Content Creation Assistant ✍️")

    # Initialize session state for control and content
    if 'query' not in st.session_state:
        st.session_state.query = ""
    if 'content' not in st.session_state:
        st.session_state.content = ""
    if 'stop_process' not in st.session_state:
        st.session_state.stop_process = False

    # Input and control buttons
    col1, col2, col3 = st.columns([3, 1, 1])

    # Content query input
    with col1:
        query = st.text_input("Enter a topic for content creation:", value=st.session_state.query)

    # Clear button
    with col2:
        if st.button("Clear"):
            st.session_state.query = ""
            st.session_state.content = ""
            st.session_state.stop_process = False
            st.rerun()

    # Stop button
    with col3:
        if st.button("Stop Process"):
            st.session_state.stop_process = True

    # Generate content
    if st.button("Generate Content") and query and not st.session_state.stop_process:
        with st.spinner("Generating content..."):
            streaming_response = run_content_workflow(query)
            st.session_state.query = query

            # Placeholder for streaming text
            message_placeholder = st.empty()
            full_content = ""

            # Stream the response and check stop button status
            for chunk in streaming_response:
                if isinstance(chunk, dict) and 'content' in chunk:
                    content = chunk['content']
                    full_content += content
                    message_placeholder.markdown(full_content + "▌")

                # Stop the process if the stop button is clicked
                if st.session_state.stop_process:
                    message_placeholder.markdown("Process Stopped.")
                    break

            # Finalize and save content only if not stopped
            if not st.session_state.stop_process:
                st.session_state.content = full_content  # Save final content once
            else:
                st.session_state.stop_process = False  # Reset stop process flag

if __name__ == "__main__":
    main()