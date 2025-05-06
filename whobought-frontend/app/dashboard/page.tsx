'use client';

import { useState, useEffect } from 'react';
import ProtectedRoute from '../utils/ProtectedRoute';
import authStore from '../store/authStore';

export default function Dashboard() {
    const [username, setUsername] = useState<string>('');

    useEffect(() => {
        const user = authStore.getUser();
        if (user) {
            setUsername(user.username);
        }
    }, []);

    return (
        <ProtectedRoute>
            <div className="py-10">
                <header>
                    <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
                        <h1 className="text-3xl font-bold leading-tight text-gray-900">Dashboard</h1>
                    </div>
                </header>
                <main>
                    <div className="max-w-7xl mx-auto sm:px-6 lg:px-8">
                        <div className="px-4 py-8 sm:px-0">
                            <div className="border-4 border-dashed border-gray-200 rounded-lg p-6">
                                <h2 className="text-xl font-semibold mb-4">Welcome, {username}!</h2>

                                <p className="text-gray-600 mb-6">
                                    This is your dashboard where you can manage your account and track items.
                                </p>

                                <div className="bg-white shadow overflow-hidden sm:rounded-md">
                                    <ul className="divide-y divide-gray-200">
                                        <li>
                                            <a href="#" className="block hover:bg-gray-50">
                                                <div className="px-4 py-4 sm:px-6">
                                                    <div className="flex items-center justify-between">
                                                        <p className="text-sm font-medium text-purple-600 truncate">
                                                            Recent Purchases
                                                        </p>
                                                        <div className="ml-2 flex-shrink-0 flex">
                                                            <p className="px-2 inline-flex text-xs leading-5 font-semibold rounded-full bg-green-100 text-green-800">
                                                                3 New
                                                            </p>
                                                        </div>
                                                    </div>
                                                </div>
                                            </a>
                                        </li>
                                        <li>
                                            <a href="#" className="block hover:bg-gray-50">
                                                <div className="px-4 py-4 sm:px-6">
                                                    <div className="flex items-center justify-between">
                                                        <p className="text-sm font-medium text-purple-600 truncate">
                                                            Your Groups
                                                        </p>
                                                        <div className="ml-2 flex-shrink-0 flex">
                                                            <p className="px-2 inline-flex text-xs leading-5 font-semibold rounded-full bg-purple-100 text-purple-800">
                                                                2 Active
                                                            </p>
                                                        </div>
                                                    </div>
                                                </div>
                                            </a>
                                        </li>
                                        <li>
                                            <a href="#" className="block hover:bg-gray-50">
                                                <div className="px-4 py-4 sm:px-6">
                                                    <div className="flex items-center justify-between">
                                                        <p className="text-sm font-medium text-purple-600 truncate">
                                                            Account Settings
                                                        </p>
                                                    </div>
                                                </div>
                                            </a>
                                        </li>
                                    </ul>
                                </div>
                            </div>
                        </div>
                    </div>
                </main>
            </div>
        </ProtectedRoute>
    );
} 