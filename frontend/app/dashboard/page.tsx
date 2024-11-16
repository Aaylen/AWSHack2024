// app/dashboard/page.tsx
'use client';

import { useState, useEffect } from 'react';
import { useRouter } from 'next/navigation';
import { auth } from '../../lib/firebaseConfig';
import { User, signOut, onAuthStateChanged } from 'firebase/auth';

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
            // Handle AI response here if needed
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
        <div className="flex flex-col min-h-screen">
            <div className="flex justify-between items-center py-4 px-8 bg-gray-800 text-white">
                <h1 className="text-2xl">Dashboard</h1>
                {user && (
                    <div className="relative">
                        <button className="relative z-10 block text-white focus:outline-none">
                            {user.email}
                        </button>
                        <div className="absolute right-0 mt-2 w-48 bg-white rounded-md overflow-hidden shadow-xl z-20">
                            <button
                                className="block px-4 py-2 text-gray-800 hover:bg-gray-200 w-full text-left"
                                onClick={handleLogout}
                            >
                                Logout
                            </button>
                        </div>
                    </div>
                )}
            </div>
            <div className="flex flex-grow items-center justify-center">
                <div className="flex flex-col items-center w-full max-w-md p-4 border rounded shadow-md bg-white">
                    <div className="flex flex-col items-center w-full space-y-4 overflow-y-auto">
                        {messages.map((message, index) => (
                            <div key={index} className="p-2 bg-gray-200 rounded-md">
                                {message}
                            </div>
                        ))}
                    </div>
                    <div className="w-full pt-4">
                        <input
                            type="text"
                            value={input}
                            onChange={(e) => setInput(e.target.value)}
                            placeholder="Type your message here..."
                            className="p-2 border border-gray-300 rounded w-full"
                        />
                        <button
                            onClick={handleSendMessage}
                            className="p-2 bg-blue-500 text-white rounded mt-2 w-full"
                        >
                            Send
                        </button>
                    </div>
                </div>
            </div>
        </div>
    );
}