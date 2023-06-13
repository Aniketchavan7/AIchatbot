import React, { useState, useEffect, useRef } from 'react';
import { FaPaperPlane, FaCamera } from 'react-icons/fa';
import './App.css';
import cuteBotImage from './cute-bot.png';
import userImage from './user-image.png';
import chatImage from './chat-image.png'; // Import the chat image

const App = () => {
  const [messages, setMessages] = useState([]);
  const [userMessage, setUserMessage] = useState('');
  const messageContainerRef = useRef(null);

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  const scrollToBottom = () => {
    messageContainerRef.current.scrollTop = messageContainerRef.current.scrollHeight;
  };

  const handleInputChange = (event) => {
    setUserMessage(event.target.value);
  };

  const handleSendMessage = async (event) => {
    event.preventDefault();
    if (userMessage.trim() !== '') {
      const newMessage = {
        content: userMessage,
        isBot: false,
      };
      setMessages((prevMessages) => [...prevMessages, newMessage]);
      setUserMessage('');

      // Send user message to the Flask server
      try {
        const response = await fetch('http://localhost:5000/chat', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify({ message: userMessage }),
        });
        const data = await response.json();

        // Add bot response to the messages
        const botMessage = {
          content: data.message,
          isBot: true,
        };
        setTimeout(() => {
          setMessages((prevMessages) => [...prevMessages, botMessage]);
        }, 500); // Delay bot response for better UX
        console.log('Bot Response:', data.message);
      } catch (error) {
        console.error('Failed to send the request:', error);
      }
    }
  };

  return (
    <div className="App">
      <header className="header">
        <h1 className="chatbot-title">SerenityNow</h1>
        {/* <img className="cute-bot-image" src={cuteBotImage} alt="Cute Bot" /> */}
      </header>
      <div className="chat-window">
        <div className="chat-image-container">
          <img className="chat-image" src={chatImage} alt="Chat" />
        </div>

        <div className="message-container" ref={messageContainerRef}>
          {messages.map((message, index) => (
            <div
              key={index}
              className={`chat-message ${message.isBot ? 'bot' : 'user'}`}
            >
              {message.isBot ? (
                <>
                  <img className="bot-message-image" src={cuteBotImage} alt="Bot" />
                  <p style={{backgroundColor:"#3b9bd6"}} className="message-content">{message.content}</p>
                </>
              ) : (
                <>
                  <img className="user-message-image" src={userImage} alt="User" />
                  <p style={{backgroundColor:"#d217f8"}} className="message-content">{message.content}</p>
                </>
              )}
            </div>
          ))}
        </div>

        <form className="input-form" onSubmit={handleSendMessage}>
          <input
            type="text"
            placeholder="Type your message..."
            value={userMessage}
            onChange={handleInputChange}
          />
          <button type="submit" className="send-button">
            <FaPaperPlane />
          </button>
          <button type="button" className="camera-button">
            <FaCamera />
          </button>
        </form>
      </div>
    </div>
  );
};

export default App;
