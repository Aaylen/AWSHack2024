// app/login/page.tsx
'use client';

import { useState } from 'react';
import { useRouter } from 'next/navigation';
import { auth } from '../../lib/firebaseConfig';
import { GoogleAuthProvider, signInWithPopup, signInWithEmailAndPassword } from 'firebase/auth';

export default function Login() {
    const [email, setEmail] = useState('');
    const [password, setPassword] = useState('');
    const router = useRouter();

    const handleLogin = async (e: React.FormEvent) => {
        e.preventDefault();
        try {
            await signInWithEmailAndPassword(auth, email, password);
            router.push('/');
        } catch (error) {
            console.error('Error logging in with email and password', error);
        }
    };

    const handleGoogleLogin = async () => {
        const provider = new GoogleAuthProvider();
        try {
            await signInWithPopup(auth, provider);
            router.push('/');
        } catch (error) {
            console.error('Error logging in with Google', error);
        }
    };

    return (
        <div className="flex flex-col items-center justify-center min-h-screen py-2">
            <h1 className="text-4xl mb-4">Login</h1>

            <form onSubmit={handleLogin} className="flex flex-col gap-4">
                <input
                    type="email"
                    value={email}
                    onChange={(e) => setEmail(e.target.value)}
                    placeholder="Email"
                    className="p-2 border border-gray-300 rounded"
                />
                <input
                    type="password"
                    value={password}
                    onChange={(e) => setPassword(e.target.value)}
                    placeholder="Password"
                    className="p-2 border border-gray-300 rounded"
                />
                <button
                    type="submit"
                    className="p-2 bg-blue-500 text-white rounded"
                >
                    Login
                </button>
            </form>

            <button
                onClick={handleGoogleLogin}
                className="mt-4 p-2 bg-red-500 text-white rounded"
            >
                Sign in with Google
            </button>
        </div>
    );
}