import React, { useState, useRef, useEffect } from 'react';
import './ChatWidget.css';

interface Message {
  role: 'user' | 'assistant';
  content: string;
  citations?: Citation[];
}

interface Citation {
  chapter: string;
  section: string;
  url: string;
  relevance_score: number;
}

interface ChatWidgetProps {
  apiUrl?: string;
}

const ChatWidget: React.FC<ChatWidgetProps> = ({
  apiUrl = process.env.NODE_ENV === 'production'
    ? 'https://physical-ai-and-humanoid-robotic.vercel.app'
    : 'http://localhost:8000'
}) => {
  const [isOpen, setIsOpen] = useState(false);
  const [messages, setMessages] = useState<Message[]>([]);
  const [input, setInput] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [sessionId, setSessionId] = useState<string | null>(null);
  const [selectedText, setSelectedText] = useState<string>('');
  const messagesEndRef = useRef<HTMLDivElement>(null);

  // Handle text selection on the page
  useEffect(() => {
    const handleSelection = () => {
      const selection = window.getSelection();
      const text = selection?.toString().trim();
      if (text && text.length > 10) {
        setSelectedText(text);
      }
    };

    document.addEventListener('mouseup', handleSelection);
    return () => document.removeEventListener('mouseup', handleSelection);
  }, []);

  // Auto-scroll to bottom
  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages]);

  const sendMessage = async (messageText?: string) => {
    const textToSend = messageText || input.trim();
    if (!textToSend) return;

    const userMessage: Message = {
      role: 'user',
      content: textToSend
    };

    setMessages(prev => [...prev, userMessage]);
    setInput('');
    setIsLoading(true);

    try {
      const response = await fetch(`${apiUrl}/api/chat/query`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          message: textToSend,
          context: selectedText || undefined,
          session_id: sessionId
        }),
      });

      if (!response.ok) {
        throw new Error('Failed to get response');
      }

      const data = await response.json();

      const assistantMessage: Message = {
        role: 'assistant',
        content: data.response,
        citations: data.citations
      };

      setMessages(prev => [...prev, assistantMessage]);
      setSessionId(data.session_id);
      setSelectedText(''); // Clear selected text after using it

    } catch (error) {
      console.error('Chat error:', error);
      const errorMessage: Message = {
        role: 'assistant',
        content: 'Sorry, I encountered an error. Please make sure the backend is running at http://localhost:8000'
      };
      setMessages(prev => [...prev, errorMessage]);
    } finally {
      setIsLoading(false);
    }
  };

  const handleKeyPress = (e: React.KeyboardEvent) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      sendMessage();
    }
  };

  const askAboutSelection = () => {
    if (!selectedText) return;
    sendMessage(`Explain this: "${selectedText.substring(0, 100)}..."`);
  };

  const clearChat = () => {
    setMessages([]);
    setSessionId(null);
    setSelectedText('');
  };

  return (
    <>
      {/* Floating chat button */}
      <button
        className={`chat-widget-button ${isOpen ? 'open' : ''}`}
        onClick={() => setIsOpen(!isOpen)}
        aria-label="Toggle chat"
      >
        {isOpen ? '✕' : '💬'}
      </button>

      {/* Selection popup */}
      {selectedText && !isOpen && (
        <div className="selection-popup">
          <button onClick={askAboutSelection} className="ask-ai-button">
            Ask AI about selection
          </button>
        </div>
      )}

      {/* Chat panel */}
      {isOpen && (
        <div className="chat-widget-panel">
          {/* Header */}
          <div className="chat-header">
            <h3>Physical AI Assistant</h3>
            <div className="chat-header-actions">
              {messages.length > 0 && (
                <button onClick={clearChat} className="clear-button" title="Clear chat">
                  🗑️
                </button>
              )}
              <button onClick={() => setIsOpen(false)} className="close-button">
                ✕
              </button>
            </div>
          </div>

          {/* Messages */}
          <div className="chat-messages">
            {messages.length === 0 && (
              <div className="welcome-message">
                <h4>👋 Welcome!</h4>
                <p>I'm your AI assistant for the Physical AI & Humanoid Robotics course.</p>
                <p>You can:</p>
                <ul>
                  <li>Ask questions about the course content</li>
                  <li>Select text on the page and ask me about it</li>
                  <li>Get help with ROS 2, Gazebo, NVIDIA Isaac, and more!</li>
                </ul>
                <p className="test-mode-note">
                  🧪 <strong>Test Mode:</strong> Currently using mock responses.
                  Connect API keys for full functionality.
                </p>
              </div>
            )}

            {messages.map((message, index) => (
              <div key={index} className={`message ${message.role}`}>
                <div className="message-content">
                  {message.content}
                </div>
                {message.citations && message.citations.length > 0 && (
                  <div className="citations">
                    <strong>📚 References:</strong>
                    <ul>
                      {message.citations.map((citation, idx) => (
                        <li key={idx}>
                          <a href={citation.url}>
                            {citation.chapter} - {citation.section}
                          </a>
                          <span className="relevance-score">
                            ({Math.round(citation.relevance_score * 100)}% relevant)
                          </span>
                        </li>
                      ))}
                    </ul>
                  </div>
                )}
              </div>
            ))}

            {isLoading && (
              <div className="message assistant loading">
                <div className="typing-indicator">
                  <span></span>
                  <span></span>
                  <span></span>
                </div>
              </div>
            )}

            <div ref={messagesEndRef} />
          </div>

          {/* Input area */}
          <div className="chat-input-area">
            {selectedText && (
              <div className="context-indicator">
                Context: "{selectedText.substring(0, 50)}..."
                <button onClick={() => setSelectedText('')}>✕</button>
              </div>
            )}
            <div className="chat-input-container">
              <textarea
                value={input}
                onChange={(e) => setInput(e.target.value)}
                onKeyPress={handleKeyPress}
                placeholder="Ask about the course content..."
                rows={2}
                disabled={isLoading}
              />
              <button
                onClick={() => sendMessage()}
                disabled={!input.trim() || isLoading}
                className="send-button"
              >
                {isLoading ? '⏳' : '📤'}
              </button>
            </div>
            <div className="quick-actions">
              <button onClick={() => sendMessage("What is ROS 2?")} className="quick-action">
                What is ROS 2?
              </button>
              <button onClick={() => sendMessage("Explain topics")} className="quick-action">
                Explain topics
              </button>
              <button onClick={() => sendMessage("Tell me about Gazebo")} className="quick-action">
                Tell me about Gazebo
              </button>
            </div>
          </div>
        </div>
      )}
    </>
  );
};

export default ChatWidget;
