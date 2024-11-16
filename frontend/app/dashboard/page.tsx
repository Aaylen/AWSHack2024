'use client'; // Mark this component as a Client Component

import { useState, useEffect } from 'react';
import { useRouter } from 'next/navigation';
import { auth } from '@/lib/firebaseConfig';
import { User, signOut, onAuthStateChanged } from 'firebase/auth';
import './styles.css';

export default function Dashboard() {
    const [messages, setMessages] = useState<string[]>([]);
    const [input, setInput] = useState('');
    const [user, setUser] = useState<User | null>(null);
    const router = useRouter();

    useEffect(() => {
        const unsubscribe = onAuthStateChanged(auth, (user) => {
            if (user) {
                setUser(user);
            } else {
                router.push('/login');
            }
        });
        return () => unsubscribe();
    }, [router]);

    const handleSendMessage = () => {
        if (input) {
            setMessages((prevMessages) => [...prevMessages, input]);
            setInput('');
        }
    };

    const handleLogout = async () => {
        try {
            await signOut(auth);
            router.push('/login');
        } catch (error) {
            console.error('Error logging out', error);
        }
    };

    return (
        <div className="dashboard-container">
            {/* Header */}
            <div className="header">
                <h1>Dashboard</h1>
                {user && (
                    <div className="header-user">
                        <span>{user.email}</span>
                        <button onClick={handleLogout} className="header-logout">
                            Logout
                        </button>
                    </div>
                )}
            </div>

            {/* Main Content */}
            <div className="main">
                {/* Left Column */}
                <div className="column"></div>

                {/* Center Column */}
                <div className="column column-center">
                    <div className="chat-box">
                        {/* Messages */}
                        <div className="chat-messages">
                            {messages.map((message, index) => (
                                <div key={index}>{message}</div>
                            ))}
                        </div>
                        {/* Input */}
                        <div className="chat-input-container">
                            <input
                                type="text"
                                value={input}
                                onChange={(e) => setInput(e.target.value)}
                                placeholder="Type your message here..."
                                className="chat-input"
                            />
                            <button onClick={handleSendMessage} className="chat-send-button">
                                Send
                            </button>
                        </div>
                    </div>
                </div>

                {/* Right Column */}
                <div className="column"></div>
            </div>
        </div>
    );
}
