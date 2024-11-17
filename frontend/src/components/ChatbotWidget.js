import React, { useState } from 'react';
import ChatMessage from './ChatMessage';
import ChatInput from './ChatInput';
import './ChatbotWidget.css';

const ChatbotWidget = () => {
    const [messages, setMessages] = useState([]);

    const handleSendMessage = (message) => {
        setMessages([...messages, { text: message, user: 'You' }, { text: 'The first place we visit in our journey is Europe in the 1800s. A new and popular piece of tableware, the willow plate, has started production. This might seem insignificant, but this is an important part about western and eastern cultures mixing. The willow plate gets its name from the content depicted on these plates, which is an influence from a Chinese love story. It was a very popular design at the time, with the production of these plates even continuing today. There are even different variations made adapting to pop culture. The story goes that a daughter and his father’s accountant fall in love, run away together, pass away, and reincarnate as willow birds. The plate illustrates the entire story, although it is a little hard to decipher without context. The fact that Chinese influence spread this far west is quite intriguing, based on China’s history of isolationism. The west did not have much access to China until “In 1760, the Chinese Emperor Qianlong, desiring to control the empire’s intellectual and commercial intercourse with the outside world, confined all Westerners to the southern port of Canton (Guangzhou)”. Despite China being open to the west, parts of Chinese culture only trickled into the west due to the limited amount of ports available. China was not yet fully comfortable trading with the west yet, and had more of an isolationist view. China’s isolationism created mystery around itself, and the west considered any article from China as “exotic”. At this point, the west did not fully understand Chinese culture or customs. China was nothing more than this far away land that was yet to be explored and understood. This exociticism led to the production of Cathay, or Chinese-influenced style. \n', user: 'AI' }]);
    };

    return (
        <div className="chatbot-widget">
            <div className="chat-messages">
                {messages.map((message, index) => (
                    <ChatMessage key={index} message={message} />
                ))}
            </div>
            <ChatInput onSendMessage={handleSendMessage} />
        </div>
    );
};

export default ChatbotWidget;