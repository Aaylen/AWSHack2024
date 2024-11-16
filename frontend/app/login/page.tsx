// app/login/page.tsx
'use client';

import { useState, useEffect } from 'react';
import { useRouter } from 'next/navigation';
import { auth } from '../../lib/firebaseConfig';
import { GoogleAuthProvider, signInWithPopup, signInWithEmailAndPassword, onAuthStateChanged } from 'firebase/auth';
import './styles.css';

export default function Login() {
    const [email, setEmail] = useState('');
    const [password, setPassword] = useState('');
    const router = useRouter();

    useEffect(() => {
        const unsubscribe = onAuthStateChanged(auth, (user) => {
            if (user) {
                router.push('/dashboard');
            }
        });

        return () => unsubscribe();
    }, [router]);

    const handleLogin = async (e: React.FormEvent) => {
        e.preventDefault();
        try {
            await signInWithEmailAndPassword(auth, email, password);
        } catch (error) {
            console.error('Error logging in with email and password', error);
        }
    };

    const handleGoogleLogin = async () => {
        const provider = new GoogleAuthProvider();
        try {
            await signInWithPopup(auth, provider);
        } catch (error) {
            console.error('Error logging in with Google', error);
        }
    };

    return (
        <div className="flex flex-col items-center justify-center min-h-screen py-2 bg-gray-800">
            <h1 className="text-4xl mb-4 font-light text-white">Login</h1>

            <form onSubmit={handleLogin} className="flex flex-col gap-4 w-full max-w-sm">
                <input
                    type="email"
                    value={email}
                    onChange={(e) => setEmail(e.target.value)}
                    placeholder="Email"
                    className="p-2 border border-gray-300 rounded bg-white focus:outline-none focus:ring-2 focus:ring-blue-500"
                />
                <input
                    type="password"
                    value={password}
                    onChange={(e) => setPassword(e.target.value)}
                    placeholder="Password"
                    className="p-2 border border-gray-300 rounded bg-white focus:outline-none focus:ring-2 focus:ring-blue-500"
                />
                <button type="submit" className="p-2 border border-gray-300 text-gray-800 bg-white rounded focus:outline-none focus:ring-2 focus:ring-blue-500">
                    Login
                </button>
            </form>

            <button
                onClick={handleGoogleLogin}
                className="mt-4 p-2 border border-gray-300 text-gray-800 bg-white rounded focus:outline-none focus:ring-2 focus:ring-blue-500"
            >
                Sign in with Google
            </button>
        </div>
    );
}