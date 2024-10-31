# Content Creation Assistant ✍️

A Streamlit-powered Content Creation Assistant that utilizes various agents to generate engaging, well-researched, and visually appealing content on specified topics. The app employs a Swarm client, DuckDuckGo for web search, and several AI agents to generate a catchy hook, search for relevant content, analyze findings, and synthesize it all into a final, shareable post.

## Features

- **Generate a catchy hook** using emojis and engaging language.
- **Search for relevant and recent content** on a specified topic.
- **Analyze and synthesize search results** to prioritize key information.
- **Craft a concise, visually appealing article** with emojis and bullet points.
- **Streamlit UI** to input queries, control the generation process, and view results in real-time.

## Project Setup

### Requirements

- **Python 3.7+**
- **Streamlit**: `pip install streamlit`
- **Swarm API**: `pip install swarm`
- **DuckDuckGo Search API**: `pip install duckduckgo-search`
- **dotenv**: `pip install python-dotenv`

### Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/DTiapan/ai-agents-handbook.git
   cd content-creation-assistant
   ```
2. Set up the .env file with necessary configurations:

```bash
OPENAI_BASE_URL=http://localhost:11434/v1
OPENAI_API_KEY=no-need-for-the-api-key
```

## Code Overview

### Main Workflow

1. **Initialize Swarm Client** and load environment variables.

2. **Define Agents**:

   - **Hook Agent**: Creates an engaging hook with relevant emojis.
   - **Content Search Agent**: Searches DuckDuckGo for content on the topic.
   - **Content Analysis Agent**: Refines and synthesizes the search results.
   - **Content Writer Agent**: Crafts a concise, polished post with bullet points and emojis.

3. **Define the `run_content_workflow` function** to orchestrate each agent:
   - **Step 1**: Generate a catchy hook for the specified query.
   - **Step 2**: Search for recent articles and content.
   - **Step 3**: Analyze search results to prioritize and organize information.
   - **Step 4**: Write a final, shareable post with emojis and bullet points.

### Streamlit Interface

- **Input Section**: Enter a topic for content generation.
- **Buttons**:
  - **Generate Content**: Starts the content creation process.
  - **Clear**: Resets the input field and clears content.
  - **Stop Process**: Interrupts the content generation.
- **Content Output**: Displays the generated content in real-time using streaming.

### Functions

- **`search_web(query)`**: Uses DuckDuckGo to fetch recent content on the topic.
- **`run_content_workflow(query)`**: Executes each step of the content generation pipeline.
- **`main()`**: Runs the Streamlit app and manages UI interactions.

## Usage

1. **Run the Streamlit App**:
   ```bash
   streamlit run agent.py
   ```

```

```
