# Physical AI & Humanoid Robotics Textbook with RAG Chatbot - Project Constitution

## Project Overview

**Project Name:** Physical AI & Humanoid Robotics: An Interactive Learning Experience

**Goal:** Create a comprehensive, production-ready educational textbook on Physical AI and humanoid robotics, delivered as a Docusaurus website with an integrated RAG-powered chatbot that provides intelligent, context-aware assistance to learners.

**Target Audience:** Students and practitioners learning about embodied AI, ROS 2, robot simulation, NVIDIA Isaac, and vision-language-action systems.

---

## Core Principles

### I. AI-Native Development First
Leverage Claude Code and Spec-Kit Plus as primary development tools, embracing specification-driven architecture from inception. All development must prioritize AI-assisted workflows and specification-first approaches.

### II. Educational Excellence
Content must be pedagogically sound, technically accurate, and progressively structured. Each module builds upon previous knowledge, with clear learning outcomes, practical examples, and hands-on guidance.

### III. Documentation as Code
Treat book content as executable documentation using Docusaurus, ensuring maintainability, version control, and automated deployment. All content must be reviewable, testable, and deployable through CI/CD pipelines.

### IV. User-Centric Intelligence
Build RAG chatbot to enhance learning by:
- Answering questions about course content
- Responding to queries based on user-selected text snippets
- Providing contextual explanations with citations
- Supporting natural conversation flow

### V. Production-Ready Standards
Deliver fully functional, deployed systems (GitHub Pages + chatbot backend) not prototypes. Every component must meet production quality standards with proper error handling, security, and performance optimization.

### VI. Specification-First Approach (NON-NEGOTIABLE)
Write comprehensive specifications before implementation. No code is written without an approved specification. This ensures clarity, reduces rework, and maintains architectural integrity.

### VII. Incremental Development
Build in phases: specification → book → backend → integration → testing → deployment. Each phase must be completed and validated before proceeding to the next.

---

## Technical Standards

### Book Development Standards

#### Platform & Deployment
- **Framework:** Docusaurus 3.x (latest stable version)
- **Deployment:** GitHub Pages with automated CI/CD pipeline
- **Version Control:** Git-based workflow with meaningful commit messages
- **Accessibility:** WCAG 2.1 AA compliance minimum

#### Content Structure
- **Minimum Chapters:** 10-15 chapters organized into 4 modules
- **Module 1:** The Robotic Nervous System (ROS 2) - 3 chapters
- **Module 2:** The Digital Twin (Gazebo & Unity) - 3 chapters
- **Module 3:** The AI-Robot Brain (NVIDIA Isaac) - 3 chapters
- **Module 4:** Vision-Language-Action (VLA) - 3-4 chapters
- **Supporting Content:** Hardware requirements, lab setup, assessments

#### Content Quality Standards
- Clear learning outcomes for each chapter
- Progressive difficulty with scaffolded learning
- Code examples must be:
  - Syntax-highlighted
  - Fully functional and tested
  - Accompanied by explanations
- Diagrams and images optimized for web (WebP/SVG preferred)
- Responsive design for mobile, tablet, and desktop viewing
- Internal links for cross-references between chapters

#### Navigation & UX
- Hierarchical sidebar navigation
- Breadcrumbs for location awareness
- Search functionality (Docusaurus built-in)
- Previous/Next chapter navigation
- Table of contents for each page
- Dark/light theme support

---

### RAG Chatbot Standards

#### Architecture Components

**Frontend:**
- Embedded React/TypeScript widget within Docusaurus pages
- Persistent chat interface (floating button + expandable panel)
- Text selection handler for context queries
- Message history within session
- Citation rendering with clickable links to book sections

**Backend:**
- **Framework:** FastAPI (Python 3.11+)
- **Deployment:** Vercel, Railway, or Render free tier
- **API Design:** RESTful endpoints with OpenAPI documentation

**LLM Integration:**
- **Provider:** OpenAI API (GPT-4 or GPT-4-turbo)
- **Embedding Model:** text-embedding-3-small or text-embedding-3-large
- **Prompt Engineering:** System prompts optimized for educational context

**Vector Database:**
- **Service:** Qdrant Cloud Free Tier
- **Storage Limit:** 1GB
- **Collections:** Book content embeddings with metadata (chapter, section, URL)

**Relational Database:**
- **Service:** Neon Serverless Postgres
- **Free Tier Limits:** 0.5GB storage, 100 hours compute/month
- **Schema:** Conversation history, user sessions, query logs, analytics

#### Functionality Requirements

**Core Features:**
1. Answer questions about entire book content
2. Respond to queries based on user-selected text snippets
3. Maintain conversation context within sessions
4. Provide source citations (chapter/section references with links)
5. Handle multi-turn conversations with memory
6. Gracefully handle out-of-scope queries

**Advanced Features:**
- Semantic search across all chapters
- Query understanding and intent classification
- Context-aware responses based on current page
- Code explanation and debugging assistance (when applicable)

#### Performance Targets
- **Response Time:** <3 seconds for typical queries (95th percentile)
- **Uptime:** 99%+ for backend services
- **Concurrent Users:** Support minimum 50 simultaneous sessions
- **Embedding Generation:** Complete book indexing in <30 minutes
- **Search Quality:** Top-3 retrieval accuracy >80%

---

### Code Quality Standards

#### Testing Requirements
- **Backend:** Minimum 70% code coverage
- **Unit Tests:** All service functions and API endpoints
- **Integration Tests:** End-to-end chat flow
- **Load Tests:** Concurrent user simulation

#### Documentation Requirements
1. **README.md** with:
   - Project overview and features
   - Prerequisites and dependencies
   - Installation instructions (step-by-step)
   - Environment variable configuration
   - Deployment guide
   - Usage examples
   - Troubleshooting common issues

2. **API Documentation:**
   - FastAPI auto-generated OpenAPI docs
   - Endpoint descriptions and examples
   - Request/response schemas

3. **Architecture Documentation:**
   - System architecture diagram
   - Data flow diagrams
   - Database schemas
   - Component interaction diagrams

#### Security Standards
- **API Keys:** Stored in environment variables (never committed)
- **Rate Limiting:** 100 requests per minute per IP
- **Input Sanitization:** All user queries sanitized before processing
- **CORS Configuration:** Whitelist only GitHub Pages domain
- **Authentication:** Optional user sessions (not required for MVP)
- **Data Privacy:** No PII storage; conversation logs anonymized

#### Error Handling
- Graceful degradation when services unavailable
- User-friendly error messages (no stack traces exposed)
- Retry logic with exponential backoff
- Fallback responses when LLM unavailable
- Comprehensive logging for debugging

---

## Constraints

### Technical Constraints

#### Required Tools
- **Claude Code:** Primary development assistant
- **Spec-Kit Plus:** Specification management
- **Git/GitHub:** Version control and collaboration

#### Free Tier Services (MANDATORY)
- **Qdrant Cloud:** 1GB vector storage limit
- **Neon Postgres:** 0.5GB storage, 100 hours compute/month
- **GitHub Pages:** Static hosting for Docusaurus site
- **Vercel/Railway/Render:** Backend hosting on free tier

#### API Cost Management
- **OpenAI API:** Monitor token usage; implement query throttling
- **Budget Limit:** Set monthly spending cap
- **Optimization:** Cache common queries, optimize prompt length

### Development Constraints

#### Specification-First Workflow
1. Write detailed specification in `.specify/specs/`
2. Review and approve specification
3. Implement according to specification
4. Validate implementation against specification

#### Incremental Development with Validation Gates
- Each phase must pass validation before next phase begins
- No phase skipping or parallel execution of dependent phases
- Code reviews and testing at each gate

#### Token Budget Awareness
- Optimize prompts for Claude Code interactions
- Minimize redundant file reads
- Use targeted searches and queries

### Content Constraints

#### Book Scope
- **Topic:** Physical AI & Humanoid Robotics (clearly defined)
- **Depth:** Comprehensive coverage from fundamentals to advanced topics
- **Length:** 10-15 substantive chapters (not just placeholders)
- **Originality:** Original content with proper attribution for external sources

#### Code Examples
- All code must be tested and functional
- Provide setup instructions for dependencies
- Include expected outputs and explanations

#### Hardware & Lab Setup
- Document realistic hardware requirements
- Provide cloud-based alternatives where possible
- Cost transparency for all recommended equipment

---

## Development Workflow

### Phase 0: Specification & Planning
**Duration:** 3-5 days

**Activities:**
- Define book outline and learning objectives
- Design chatbot architecture and data flow
- Create technical specifications for all components
- Set up project structure and Git repository

**Deliverables:**
- `.specify/specs/book-specification.md`
- `.specify/specs/chatbot-architecture.md`
- `.specify/specs/integration-specification.md`
- Architecture diagrams

**Validation Gate:** Specifications reviewed and approved

---

### Phase 1: Book Development
**Duration:** 1-2 weeks

**Activities:**
- Initialize Docusaurus project
- Configure theme, navigation, and plugins
- Write Module 1 content (ROS 2)
- Write Module 2 content (Simulation)
- Write Module 3 content (NVIDIA Isaac)
- Write Module 4 content (VLA)
- Add supporting content (hardware, lab setup, assessments)
- Add images, diagrams, and code examples
- Configure GitHub Pages deployment
- Test responsive design and accessibility

**Deliverables:**
- Docusaurus site with 10+ chapters
- All code examples tested
- Images and diagrams optimized
- GitHub Actions workflow for deployment

**Validation Gate:** Functional Docusaurus site deployed to GitHub Pages with complete content

---

### Phase 2: Backend Development
**Duration:** 1-2 weeks

**Activities:**
- Set up FastAPI project structure
- Implement Postgres database schema and connection
- Implement Qdrant vector database integration
- Implement OpenAI API integration
- Build chat API endpoints
- Build embedding generation endpoints
- Add authentication and rate limiting
- Write comprehensive tests (70%+ coverage)
- Deploy to Vercel/Railway/Render
- Generate API documentation

**Deliverables:**
- FastAPI backend with REST API
- Deployed backend service (public URL)
- API documentation accessible
- Test suite with 70%+ coverage

**Validation Gate:** Backend deployed and accessible; all tests passing; API documentation complete

---

### Phase 3: Content Embeddings
**Duration:** 3-5 days

**Activities:**
- Write embedding generation script
- Parse Docusaurus markdown files
- Chunk content into semantic units (paragraph/section level)
- Generate embeddings via OpenAI API
- Store embeddings in Qdrant with metadata
- Create citation mapping (embedding → chapter/section URL)
- Test retrieval quality with sample queries
- Optimize chunk size and overlap parameters

**Deliverables:**
- Embedding generation script in `backend/scripts/`
- Qdrant collection populated with book embeddings
- Citation metadata complete
- Retrieval quality report

**Validation Gate:** Qdrant populated; test queries return relevant results with >80% accuracy

---

### Phase 4: Frontend Integration
**Duration:** 1 week

**Activities:**
- Create React ChatWidget component
- Implement chat UI with message history
- Add text selection handler for context queries
- Connect widget to backend API
- Implement citation display with clickable links to book sections
- Add loading states and error handling
- Style widget to match Docusaurus theme
- Embed widget in all book pages via Docusaurus plugin/component
- Test on mobile, tablet, and desktop
- Add keyboard shortcuts and accessibility features (ARIA labels)

**Deliverables:**
- ChatWidget component (`src/components/ChatWidget/`)
- Embedded chat in all Docusaurus pages
- Mobile-responsive design
- Accessibility compliance (WCAG 2.1 AA)

**Validation Gate:** Chat widget functioning in Docusaurus; text selection queries working; citations linking correctly

---

### Phase 5: Testing & Refinement
**Duration:** 3-5 days

**Activities:**
- End-to-end user flow testing (read → select text → ask → receive answer with citation)
- Performance testing (response times under load)
- Load testing (50+ concurrent users)
- Security testing (rate limits, input sanitization, API key protection)
- Cross-browser testing (Chrome, Firefox, Safari, Edge)
- Mobile responsiveness testing (iOS/Android)
- Bug fixes and UX improvements
- API cost monitoring and optimization
- Documentation review and updates
- Accessibility audit (WCAG 2.1 AA)

**Deliverables:**
- Test reports (performance, load, security, accessibility)
- Bug fixes committed
- Optimizations implemented
- Updated documentation

**Validation Gate:** All success criteria met; no critical bugs; performance targets achieved

---

### Phase 6: Documentation & Deployment
**Duration:** 2-3 days

**Activities:**
- Write comprehensive README with setup instructions
- Create system architecture diagram
- Document all API endpoints with examples
- Write deployment guide for reproducing setup
- Document environment variables and configuration
- Add troubleshooting guide
- Create demo screenshots/video
- Final production deployment
- Project retrospective and lessons learned

**Deliverables:**
- Complete README.md
- Architecture diagrams
- Deployment guide
- Troubleshooting documentation
- Demo materials
- Retrospective notes

**Validation Gate:** Complete project with full documentation; ready for submission/presentation

---

## Success Criteria

### Book Deliverables ✓
- [ ] Docusaurus site successfully deployed to GitHub Pages
- [ ] Minimum 10 chapters with cohesive narrative across 4 modules
- [ ] All code examples tested and functional
- [ ] Navigation, search, and responsive design working
- [ ] Accessibility compliance (WCAG 2.1 AA)
- [ ] GitHub repository with clean commit history
- [ ] Images and diagrams optimized for web

### RAG Chatbot Deliverables ✓
- [ ] FastAPI backend deployed and accessible
- [ ] Qdrant vector database populated with book embeddings
- [ ] Neon Postgres storing conversation history/metadata
- [ ] OpenAI integration functioning correctly
- [ ] Chatbot widget embedded in all book pages
- [ ] User-selected text query feature operational
- [ ] Citations linking back to book sections with clickable URLs
- [ ] Response time <3 seconds for 95% of queries
- [ ] Support for 50+ concurrent users

### Integration & Quality ✓
- [ ] End-to-end user flow tested (read → select text → ask question → receive answer with citation)
- [ ] API documentation accessible and complete
- [ ] Setup instructions validated by fresh install
- [ ] No critical bugs or broken functionality
- [ ] Performance targets met (response time, uptime, concurrent users)
- [ ] Security measures implemented (rate limiting, input sanitization, API key protection)
- [ ] 70%+ test coverage for backend code

### Documentation ✓
- [ ] System architecture diagram showing all components
- [ ] README with:
  - Project overview and features
  - Prerequisites and dependencies
  - Installation steps (detailed)
  - Configuration instructions (environment variables)
  - Deployment instructions (reproducible)
  - Usage examples
  - Troubleshooting guide
- [ ] API documentation accessible (FastAPI auto-generated)
- [ ] Lessons learned or development notes

---

## Risk Management

### API Cost Overruns
**Risk:** OpenAI API costs exceed budget
**Mitigation:**
- Set monthly spending cap in OpenAI dashboard
- Implement query throttling (rate limiting)
- Cache common queries
- Monitor token usage daily
- Use smaller models where possible (gpt-3.5-turbo for simple queries)

### Free Tier Limitations
**Risk:** Exceeding Qdrant (1GB) or Neon (0.5GB, 100hrs) limits
**Mitigation:**
- Optimize embedding storage (compress metadata)
- Implement data retention policies (delete old conversations)
- Monitor usage proactively
- Plan migration strategy if limits approached

### Deployment Issues
**Risk:** CI/CD pipeline failures or deployment errors
**Mitigation:**
- Test deployment pipeline early (Phase 1)
- Have rollback strategy (git revert + redeploy)
- Use staging environment for testing
- Document deployment steps for manual fallback

### Scope Creep
**Risk:** Adding features beyond MVP requirements
**Mitigation:**
- Stick rigidly to success criteria
- Document "future enhancements" separately
- Use validation gates to enforce phase completion
- Regular reviews against constitution

### Performance Degradation
**Risk:** Chatbot response times exceed 3 seconds
**Mitigation:**
- Load testing in Phase 5
- Optimize vector search (reduce embedding dimensions if needed)
- Implement caching for common queries
- Use async/await in FastAPI for concurrent requests

### Security Vulnerabilities
**Risk:** API key exposure, injection attacks, or DDoS
**Mitigation:**
- Never commit API keys (use .env files)
- Input sanitization on all user queries
- Rate limiting (100 req/min per IP)
- CORS whitelist (only GitHub Pages domain)
- Regular security audits

---

## Governance

### Constitution Authority
This constitution supersedes all other development practices and decisions. All implementation work must comply with the principles, standards, and constraints defined herein.

### Compliance Requirements
- All development must verify compliance with constitution requirements before proceeding
- Deviations require documented justification and explicit approval
- Constitution updates require version increment and ratification
- Weekly reviews to ensure alignment with success criteria

### Decision-Making Framework
1. **Specification-First:** No code without approved spec
2. **Validation Gates:** No phase skipping without passing validation
3. **Quality Over Speed:** Meet standards even if it takes longer
4. **User-Centric:** Prioritize learner experience in all decisions
5. **Production-Ready:** No "good enough" prototypes; build for deployment

### Change Management
- Minor updates (typos, clarifications): Direct edit with commit message
- Major changes (new phases, altered standards): Version increment + documented rationale
- Emergency changes (critical bugs): Immediate fix + retrospective documentation

---

## Metadata

**Version:** 2.0.0
**Project:** Physical AI & Humanoid Robotics Textbook with RAG Chatbot
**Ratified:** 2026-01-03
**Last Amended:** 2026-01-03
**Next Review:** Upon completion of Phase 0 (Specification)

---

## Appendix: Key Technologies

### Frontend Stack
- Docusaurus 3.x (React-based static site generator)
- React 18+ (UI framework)
- TypeScript (type-safe JavaScript)
- CSS Modules (component styling)

### Backend Stack
- FastAPI (Python web framework)
- Python 3.11+ (programming language)
- Pydantic (data validation)
- SQLAlchemy (ORM for Postgres)
- Uvicorn (ASGI server)

### AI & Database Services
- OpenAI API (GPT-4, text-embedding-3-small)
- Qdrant Cloud (vector database)
- Neon Serverless Postgres (relational database)

### DevOps & Deployment
- GitHub Actions (CI/CD)
- GitHub Pages (frontend hosting)
- Vercel/Railway/Render (backend hosting)
- Git (version control)

### Development Tools
- Claude Code (AI development assistant)
- Spec-Kit Plus (specification management)
- VS Code / Cursor (code editor)
- pytest (testing framework)
- Black/Ruff (Python formatting/linting)
- ESLint/Prettier (JavaScript/TypeScript linting/formatting)

---

**End of Constitution**
