# RAG Chatbot Architecture Specification

## System Overview

**Purpose**: Provide an intelligent, context-aware chatbot embedded in the Physical AI and Humanoid Robotics textbook to enhance reader learning experience through conversational Q&A, code assistance, and concept clarification.

**Key Features**:
- Answer questions about book content
- Respond to queries on user-selected text
- Maintain conversation context
- Provide citations to source chapters/sections
- Assist with code debugging and explanations
- Quiz and assess understanding

## Architecture Components

### 1. Frontend (Docusaurus Widget)

#### Technology Stack
- React 18+ (included with Docusaurus)
- TypeScript for type safety
- Tailwind CSS for styling
- WebSocket or REST API for backend communication

#### Widget Features
- **Floating Chat Button**: Bottom-right corner, minimizable
- **Chat Interface**:
  - Message history display
  - Text input with auto-resize
  - Code block rendering with syntax highlighting
  - Markdown support for formatted responses
- **Text Selection Feature**:
  - Detect user text selection on page
  - Show "Ask about this" tooltip/button
  - Pre-populate chat with selected text context
- **Citation Links**: Clickable references to book sections
- **Conversation Management**:
  - New conversation button
  - Conversation history (session-based)
  - Export conversation option

#### Widget States
- Collapsed (only button visible)
- Expanded (full chat interface)
- Loading (waiting for response)
- Error (connection/API issues)

#### User Experience Flow
1. User reads book content
2. User selects text → "Ask about this" appears
3. User clicks → Chat opens with context
4. User types question or uses pre-filled prompt
5. Bot responds with answer + citations
6. User can continue conversation with context

### 2. Backend (FastAPI Application)

#### Technology Stack
- Python 3.11+
- FastAPI framework
- Uvicorn ASGI server
- Pydantic for data validation
- OpenAI Python SDK
- Qdrant Python client
- Psycopg3 for PostgreSQL

#### API Endpoints

**POST /api/chat/message**
```json
Request:
{
  "message": "Explain zero moment point",
  "conversation_id": "uuid-string",
  "selected_text": "optional-highlighted-text",
  "page_context": {
    "chapter": "5",
    "section": "Bipedal Locomotion",
    "url": "/docs/chapter-5/locomotion"
  }
}

Response:
{
  "response": "The Zero Moment Point (ZMP) is...",
  "citations": [
    {
      "chapter": "5",
      "section": "5.2 Walking Dynamics",
      "url": "/docs/chapter-5/locomotion#zmp"
    }
  ],
  "conversation_id": "uuid-string",
  "timestamp": "2026-01-03T10:30:00Z"
}
```

**POST /api/chat/new**
- Creates new conversation
- Returns conversation_id

**GET /api/chat/history/{conversation_id}**
- Retrieves conversation history
- Returns array of messages

**POST /api/embeddings/generate**
- Admin endpoint to generate book embeddings
- Processes all book content into vector store

**GET /api/health**
- Health check endpoint
- Returns service status

#### Core Services

**1. Query Service**
- Receives user query
- Retrieves conversation context from DB
- Generates embedding for query
- Searches vector database for relevant content
- Constructs RAG prompt with retrieved context
- Calls LLM API
- Parses response and extracts citations
- Stores conversation turn in DB

**2. Embedding Service**
- Generates embeddings for book content
- Uses OpenAI text-embedding-3-small model
- Chunks text optimally (512-1024 tokens)
- Stores in Qdrant with metadata

**3. Context Service**
- Manages conversation state
- Retrieves relevant history
- Handles selected text context
- Provides page context to LLM

**4. Citation Service**
- Identifies source content in retrieved chunks
- Formats citations with chapter/section/URL
- Validates citation links

#### LLM Integration

**Model**: OpenAI GPT-4 or GPT-3.5-turbo
**System Prompt Template**:
```
You are an expert assistant for the "Physical AI and Humanoid Robotics" textbook.
Your role is to help readers understand concepts, debug code, and explore topics in depth.

Context from the book:
{retrieved_chunks}

User's current page: {page_context}
Selected text (if any): {selected_text}

Conversation history:
{conversation_history}

Guidelines:
- Provide accurate, pedagogical explanations
- Reference specific chapters/sections when relevant
- Help debug code examples with specific suggestions
- Encourage hands-on learning
- If unsure, say so and suggest related topics
- Keep responses concise but comprehensive
- Use code blocks for code examples
- Format math equations clearly

User question: {user_query}
```

**Response Format**:
```json
{
  "answer": "Main response text with markdown",
  "citations": ["chapter:section", "chapter:section"],
  "suggested_followups": ["Related question 1", "Related question 2"]
}
```

### 3. Vector Database (Qdrant Cloud)

#### Configuration
- **Collection Name**: `physical_ai_book`
- **Vector Size**: 1536 (OpenAI text-embedding-3-small)
- **Distance Metric**: Cosine similarity
- **Index**: HNSW for fast approximate search

#### Document Structure
```json
{
  "id": "chapter-5-section-2-chunk-3",
  "vector": [0.123, -0.456, ...],
  "payload": {
    "chapter": "5",
    "chapter_title": "Bipedal Locomotion",
    "section": "5.2",
    "section_title": "Walking Dynamics",
    "text": "The Zero Moment Point (ZMP) is a concept...",
    "page_url": "/docs/chapter-5/locomotion#walking-dynamics",
    "chunk_index": 3,
    "tokens": 512,
    "code_included": false,
    "keywords": ["ZMP", "stability", "walking"]
  }
}
```

#### Indexing Strategy
- Chunk each chapter into 512-1024 token segments
- Overlap chunks by 128 tokens for context continuity
- Separate code blocks and explanatory text
- Include metadata for filtering and citation

#### Query Strategy
- Convert user query to embedding
- Search top-k (k=5) similar chunks
- Filter by chapter if page_context provided
- Boost relevance if selected_text matches
- Return chunks with metadata for citation

### 4. Relational Database (Neon Postgres)

#### Schema

**conversations table**
```sql
CREATE TABLE conversations (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    created_at TIMESTAMP DEFAULT NOW(),
    last_activity TIMESTAMP DEFAULT NOW(),
    user_session_id VARCHAR(255),
    page_context JSONB,
    message_count INTEGER DEFAULT 0
);
```

**messages table**
```sql
CREATE TABLE messages (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    conversation_id UUID REFERENCES conversations(id),
    role VARCHAR(50) NOT NULL, -- 'user' or 'assistant'
    content TEXT NOT NULL,
    selected_text TEXT,
    citations JSONB,
    created_at TIMESTAMP DEFAULT NOW(),
    tokens_used INTEGER,
    response_time_ms INTEGER
);
```

**analytics table**
```sql
CREATE TABLE analytics (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    event_type VARCHAR(100), -- 'query', 'selection', 'citation_click'
    event_data JSONB,
    created_at TIMESTAMP DEFAULT NOW()
);
```

#### Data Management
- Conversations expire after 30 days of inactivity
- Implement cleanup job for old data
- Export important conversations before deletion
- Anonymize user_session_id for privacy

## Security & Performance

### Security Measures

**1. API Security**
- Rate limiting: 20 requests/minute per IP
- API key authentication for admin endpoints
- CORS configuration for Docusaurus domain only
- Input sanitization for all user queries
- SQL injection prevention (parameterized queries)
- XSS prevention (sanitize outputs)

**2. Data Privacy**
- No PII collection
- Anonymous session IDs (no login required)
- Conversation data retention policy
- Optional conversation deletion

**3. API Key Management**
- Environment variables for all keys
- Separate keys for dev/prod
- Key rotation policy
- Monitor usage and costs

### Performance Optimization

**1. Response Time Targets**
- Vector search: <100ms
- LLM response: <2s
- Total query time: <3s
- Widget load time: <500ms

**2. Caching Strategy**
- Cache common queries (Redis optional)
- Cache embeddings (no regeneration needed)
- Browser cache for widget assets

**3. Scalability**
- Connection pooling for databases
- Async request handling in FastAPI
- CDN for frontend assets
- Horizontal scaling via container orchestration

**4. Monitoring**
- Log all API requests
- Track response times
- Monitor token usage
- Alert on error rates >5%

## Deployment Architecture

### Frontend Deployment (GitHub Pages)
```
GitHub Repository
├── /docs (Docusaurus source)
├── /chatbot-widget (React component)
└── /.github/workflows (CI/CD)
    └── deploy.yml
```

**Build Process**:
1. Commit to main branch
2. GitHub Actions triggers
3. Build Docusaurus site
4. Build chatbot widget
5. Deploy to gh-pages branch
6. Available at username.github.io/repo-name

### Backend Deployment (Railway/Render/Vercel)

**Option 1: Railway** (Recommended)
- Docker container deployment
- Automatic scaling
- Built-in PostgreSQL (if needed)
- Environment variable management
- Free tier: 500 hours/month

**Option 2: Render**
- Native Python support
- Background workers for async tasks
- Free tier: Available with limitations

**Option 3: Vercel**
- Serverless functions
- Edge deployment
- Free tier: Generous limits

**Deployment Configuration**:
```dockerfile
# Dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

```yaml
# railway.toml
[build]
builder = "DOCKERFILE"

[deploy]
startCommand = "uvicorn main:app --host 0.0.0.0 --port $PORT"
healthcheckPath = "/api/health"
```

### Database Deployment

**Qdrant Cloud**
- Sign up for free tier
- Create cluster
- Get API key and endpoint
- 1GB storage limit

**Neon Postgres**
- Sign up for free tier
- Create database
- Get connection string
- 0.5GB storage, 100 hours compute/month

## Development Workflow

### Phase 1: Backend Development
1. Set up FastAPI project structure
2. Implement database models and migrations
3. Build embedding service and populate Qdrant
4. Implement query service with RAG
5. Create API endpoints
6. Write unit tests (70% coverage target)
7. Test locally with sample queries

### Phase 2: Frontend Development
1. Create React widget component
2. Implement chat UI with state management
3. Add text selection detection
4. Integrate with backend API
5. Style with Tailwind CSS
6. Test responsiveness
7. Add loading states and error handling

### Phase 3: Integration
1. Embed widget in Docusaurus theme
2. Configure API endpoints
3. Test end-to-end flows
4. Optimize performance
5. Fix bugs

### Phase 4: Deployment
1. Set up CI/CD pipeline
2. Deploy backend to Railway/Render
3. Configure environment variables
4. Deploy frontend to GitHub Pages
5. Test production environment
6. Monitor and optimize

## Testing Strategy

### Backend Tests
- Unit tests for each service
- Integration tests for API endpoints
- Mock external APIs (OpenAI, Qdrant)
- Test rate limiting and security
- Load testing for concurrent users

### Frontend Tests
- Component unit tests (React Testing Library)
- Integration tests for user flows
- Cross-browser testing
- Mobile responsiveness testing
- Accessibility testing (WCAG 2.1 AA)

### End-to-End Tests
- User reads page → asks question → receives answer
- User selects text → asks about it → gets contextualized response
- User continues conversation → context maintained
- Citation links work correctly
- Error handling works gracefully

## Cost Estimation (Monthly)

### OpenAI API
- Embeddings: ~$0.50 (one-time for book)
- GPT-4 queries: ~$5-20 (depends on usage)
- Total: ~$25/month for moderate usage

### Qdrant Cloud
- Free tier: $0

### Neon Postgres
- Free tier: $0

### Backend Hosting (Railway)
- Free tier: $0 (with limits)
- Paid tier: $5/month (if needed)

### Total Estimated Cost: $0-30/month

## Success Metrics

### Technical Metrics
- API uptime: >99%
- Average response time: <3s
- Error rate: <2%
- Test coverage: >70%

### User Metrics
- Chat widget engagement: >70% of visitors
- Average messages per conversation: >3
- Citation click rate: >30%
- User satisfaction: Qualitative feedback

### Cost Metrics
- Stay within free tiers initially
- Monitor OpenAI token usage
- Optimize queries to reduce costs

## Future Enhancements (Post-MVP)

1. **Voice Input**: Speech-to-text for questions
2. **Multilingual Support**: Translate book and responses
3. **Code Execution**: Run code examples in browser
4. **Personalization**: Track user progress and adapt responses
5. **Community Features**: Share conversations, upvote answers
6. **Analytics Dashboard**: Track usage patterns and popular topics
7. **Offline Mode**: Cached responses for common queries
8. **Mobile App**: Native apps for iOS/Android

---

**Specification Version**: 1.0.0
**Created**: 2026-01-03
**Status**: APPROVED FOR IMPLEMENTATION
**Dependencies**: Book specification must be implemented first
