# Pydantic AI Documentation Assistant

An AI-powered documentation assistant that crawls, indexes, and provides intelligent responses about Pydantic AI using RAG (Retrieval Augmented Generation).

## Methodology

### Documentation Crawling Process

This project uses a sophisticated web crawling approach to build its knowledge base:

1. **Sitemap-Based Discovery**
   - The crawler first locates the Pydantic AI documentation sitemap
   - Systematically extracts URLs from the sitemap structure
   - Filters for relevant documentation pages only

2. **Content Processing**
   - Each documentation page is processed into clean, structured markdown
   - Content is intelligently split into semantic chunks
   - Maintains context and relationships between sections

3. **Vector Database Integration**
   - Generates embeddings for each content chunk using OpenAI's embedding model
   - Stores both content and embeddings in PostgreSQL with pgvector
   - Enables efficient semantic search capabilities

4. **Compliance and Rate Limiting**
   - Respects robots.txt directives
   - Implements appropriate crawl delays
   - Follows website's terms of service

### RAG Implementation

The assistant uses Retrieval Augmented Generation (RAG) to provide accurate responses:

1. When a question is asked, the system:
   - Converts the question into an embedding
   - Performs similarity search against the documentation chunks
   - Retrieves the most relevant context

2. The retrieved context is then:
   - Formatted into a prompt for the LLM
   - Used to generate accurate, documentation-based responses
   - Citations are included to reference source material

## Setup Process

### 1. Environment Setup

This step creates an isolated Python environment for the project to avoid conflicts with other Python packages on your system.

1. Create a virtual environment:

   ```bash
   python -m venv venv
   ```

2. Activate the virtual environment:

   ```bash
   # Windows
   venv\Scripts\activate
   
   # macOS/Linux
   source venv/bin/activate
   ```

3. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

### 2. Database Setup

This step sets up the vector database that will store the documentation chunks and their embeddings for semantic search.

1. Set up a PostgreSQL database (or use Supabase)
   - Supabase is recommended as it provides a managed PostgreSQL service with the required pgvector extension
   - The database will store documentation chunks and their vector embeddings for semantic search

2. Enable the pgvector extension and create necessary tables by running the SQL commands in `site_pages.sql`
   - This creates the required table structure
   - Sets up vector similarity search functionality
   - Configures proper indexing for efficient queries

### 3. Environment Variables

These variables are required for the application to connect to various services and APIs.

#### Getting API Keys

1. **OpenAI API Key**:
   - Go to <https://platform.openai.com/api-keys>
   - Sign in or create an account
   - Click "Create new secret key"
   - Copy the key (you won't be able to see it again)
   - This key is used for generating embeddings and powering the AI responses

2. **Supabase Setup**:
   - Go to <https://supabase.com/>
   - Sign in or create an account
   - Create a new project
   - Under Project Settings > API, you'll find:
     - Project URL (use as `SUPABASE_URL`)
     - Project API keys (use `service_role` secret as `SUPABASE_SERVICE_KEY`)
   - These credentials allow the application to interact with your database

Create a `.env` file with the following variables:

```env
OPENAI_API_KEY=your_openai_api_key
SUPABASE_URL=your_supabase_url
SUPABASE_SERVICE_KEY=your_supabase_service_key
LLM_MODEL=gpt-4o-mini  # or your preferred OpenAI model
```

### 4. Crawl Documentation

This step fetches and processes the Pydantic AI documentation.

1. Run the crawler to index Pydantic AI documentation:

   ```bash
   python crawl_pydantic_ai_docs.py
   ```

   This script will:
   - Fetch all pages from the Pydantic AI documentation
   - Split the content into manageable chunks
   - Generate embeddings for each chunk
   - Store the processed content in your database
   - Create a searchable knowledge base for the AI assistant

### 5. Launch the UI

Start the interactive chat interface where you can ask questions about Pydantic AI.

1. Start the Streamlit interface:

   ```bash
   streamlit run streamlit_ui.py
   ```

   This will:
   - Launch a web interface in your default browser
   - Connect to your database and OpenAI
   - Allow you to ask questions about Pydantic AI
   - Provide AI-powered responses based on the documentation
