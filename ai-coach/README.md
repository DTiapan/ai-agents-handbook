# AI Coach


## Setup
1. Clone the repo and navigate to the folder
    ```
    git clone https://github.com/DTiapan/ai-agents-handbook.git
    cd ai-coach
    ```

2. Make sure you have `uv` installed,
    - If not installed, here is the website [link](https://docs.astral.sh/uv/getting-started/installation/)

3. Install the necessary packages, it also creats the virtual environment for you.
    ```
    uv sync
    ```

4. Provide environment variables from [openai](https://platform.openai.com/settings/organization/api-keys). If you use Qdrant cloud, then here is the link -> [Qdrant Cloud](https://cloud.qdrant.io/) in the `.env` file.
    - Rename `.env.example` to `.env`
    - Provide your env variables inside it as shown below.
    ```
    OPENAI_API_KEY="xxxxx"
    ```

    QDRANT local setup, INSTALL [DOCKER](https://www.docker.com/get-started/) FIRST, HERE IS THE [LINK](https://qdrant.tech/documentation/quickstart/)
    ```
    docker pull qdrant/qdrant
    docker run -p 6333:6333 -p 6334:6334 \
    -v $(pwd)/qdrant_storage:/qdrant/storage:z \
    qdrant/qdrant
    
    ```

## Execute the script

```
python3 agentic_rag.py
```


