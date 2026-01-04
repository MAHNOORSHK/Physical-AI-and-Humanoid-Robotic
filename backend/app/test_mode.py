"""
Test mode services with mock responses
"""

from typing import List, Dict
import time


class MockOpenAIService:
    """Mock OpenAI service for testing"""

    async def generate_chat_response(
        self,
        user_message: str,
        context_documents: List[Dict[str, str]],
        conversation_history: List[Dict[str, str]] = None
    ) -> str:
        """Generate mock response"""

        # Simulate processing time
        time.sleep(0.5)

        # Simple keyword-based responses
        message_lower = user_message.lower()

        if "ros" in message_lower or "ros 2" in message_lower:
            return """ROS 2 (Robot Operating System 2) is a flexible framework for writing robot software. It's a collection of tools, libraries, and conventions designed to simplify the task of creating complex robot behavior.

Key features of ROS 2:
- **Distributed Architecture**: No single point of failure
- **Real-time Support**: For safety-critical applications
- **Multi-platform**: Linux, Windows, macOS
- **DDS Middleware**: Industry-standard communication

ROS 2 uses nodes (independent processes) that communicate via topics (streaming data), services (request-response), and actions (long-running tasks with feedback).

For installation and getting started, check out Chapter 1 of Module 1!"""

        elif "topic" in message_lower or "publish" in message_lower or "subscribe" in message_lower:
            return """Topics in ROS 2 enable asynchronous, many-to-many communication between nodes.

**How Topics Work:**
- Publishers send messages to a topic
- Subscribers receive messages from a topic
- Multiple publishers and subscribers can use the same topic
- Fire-and-forget pattern (publishers don't wait)

**When to Use Topics:**
- Streaming sensor data (camera, LiDAR, IMU)
- Robot state updates
- Continuous monitoring

Example use case: A camera node publishes images on `/camera/image_raw` topic, while multiple vision processing nodes can subscribe to process those images.

See Chapter 2 for detailed examples with code!"""

        elif "gazebo" in message_lower or "simulation" in message_lower:
            return """Gazebo is a powerful physics-based robot simulator. It allows you to test robots in realistic environments before deploying to hardware.

**Key Features:**
- Realistic physics engines (ODE, Bullet, Simbody)
- Sensor simulation (cameras, LiDAR, IMU)
- ROS 2 integration
- 3D visualization

**Why Use Gazebo:**
- Safe testing environment
- Iterate faster than hardware
- Test edge cases and failures
- Generate synthetic training data

Module 2 covers Gazebo in depth with hands-on labs!"""

        elif "isaac" in message_lower or "nvidia" in message_lower:
            return """NVIDIA Isaac is a comprehensive platform for AI-powered robotics development.

**Isaac Platform Components:**
- **Isaac Sim**: Photorealistic simulation with Omniverse
- **Isaac ROS**: Hardware-accelerated perception packages
- **Isaac Gym**: Massively parallel RL training

**Why Isaac?**
- RTX-powered ray tracing
- GPU-accelerated computer vision
- Synthetic data generation at scale
- Sim-to-real transfer capabilities

Module 3 explores the Isaac ecosystem with practical examples!"""

        elif "vla" in message_lower or "llm" in message_lower or "gpt" in message_lower:
            return """Vision-Language-Action (VLA) systems combine computer vision, natural language understanding, and robot control.

**VLA Pipeline:**
1. **Vision**: Perceive the environment (cameras, sensors)
2. **Language**: Understand natural language commands (GPT-4, Whisper)
3. **Action**: Execute robot actions (motion planning, control)

**Example Workflow:**
- User says: "Pick up the red cup"
- Whisper transcribes speech
- GPT-4 breaks down into steps
- Vision system locates red cup
- Robot executes pick-and-place

Module 4 covers VLA with the Autonomous Humanoid capstone project!"""

        else:
            # Generic response with context
            context_summary = ""
            if context_documents:
                chapters = [doc.get("chapter", "Unknown") for doc in context_documents[:2]]
                context_summary = f"\n\nBased on the course content (particularly {', '.join(chapters)}), "

            return f"""I'm here to help you learn about Physical AI and Humanoid Robotics!{context_summary}

This course covers:
- **Module 1**: ROS 2 (Robot Operating System)
- **Module 2**: Gazebo & Unity Simulation
- **Module 3**: NVIDIA Isaac Platform
- **Module 4**: Vision-Language-Action Systems

You asked: "{user_message}"

Could you be more specific? For example:
- "What is ROS 2?"
- "How do topics work?"
- "Tell me about Gazebo simulation"
- "What is NVIDIA Isaac?"

Feel free to select any text from the course and ask me about it!"""

    async def generate_embedding(self, text: str) -> List[float]:
        """Generate mock embedding"""
        # Return 1536-dimensional mock embedding (OpenAI size)
        import random
        random.seed(hash(text) % 2**32)
        return [random.random() for _ in range(1536)]


class MockQdrantService:
    """Mock Qdrant service for testing"""

    async def create_collection(self):
        """Mock collection creation"""
        print("✓ [Test Mode] Mock Qdrant collection created")
        return True

    async def search_similar(
        self,
        query_embedding: List[float],
        top_k: int = 5
    ) -> List[Dict]:
        """Return mock search results"""

        # Mock relevant documents
        mock_results = [
            {
                "id": "doc_1",
                "score": 0.95,
                "chapter": "Module 1: ROS 2",
                "section": "Introduction to ROS 2 Architecture",
                "url": "/module-01-ros2/chapter-01-ros2-architecture",
                "content": "ROS 2 is a flexible framework for writing robot software..."
            },
            {
                "id": "doc_2",
                "score": 0.88,
                "chapter": "Module 1: ROS 2",
                "section": "Topics, Services, and Actions",
                "url": "/module-01-ros2/chapter-02-topics-services-actions",
                "content": "Topics enable asynchronous communication between nodes..."
            },
            {
                "id": "doc_3",
                "score": 0.82,
                "chapter": "Module 1: ROS 2",
                "section": "Building with rclpy",
                "url": "/module-01-ros2/chapter-03-building-with-rclpy",
                "content": "rclpy is the Python client library for ROS 2..."
            },
            {
                "id": "doc_4",
                "score": 0.76,
                "chapter": "Module 2: Simulation",
                "section": "Gazebo Physics Simulation",
                "url": "/module-02-simulation/intro",
                "content": "Gazebo provides realistic physics simulation..."
            },
            {
                "id": "doc_5",
                "score": 0.70,
                "chapter": "Module 3: NVIDIA Isaac",
                "section": "Isaac Sim Overview",
                "url": "/module-03-isaac/intro",
                "content": "NVIDIA Isaac Sim offers photorealistic simulation..."
            }
        ]

        return mock_results[:top_k]

    async def get_collection_info(self) -> Dict:
        """Return mock collection info"""
        return {
            "name": "physical_ai_textbook",
            "vector_count": 150,
            "vector_size": 1536,
            "status": "test_mode"
        }

    async def insert_embedding(self, vector_id: str, embedding: List[float], metadata: Dict) -> bool:
        """Mock insert"""
        print(f"✓ [Test Mode] Mock insert: {vector_id}")
        return True

    async def insert_embeddings_batch(
        self,
        vector_ids: List[str],
        embeddings: List[List[float]],
        metadatas: List[Dict[str, str]]
    ) -> bool:
        """Mock batch insert"""
        print(f"✓ [Test Mode] Mock batch insert: {len(vector_ids)} embeddings")
        return True
