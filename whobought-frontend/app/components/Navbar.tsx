'use client';

import { useState, useRef, useEffect } from 'react';
import Link from 'next/link';
import { useRouter } from 'next/navigation';
import authStore from '../store/authStore';

const Navbar = () => {
    const [isMobileMenuOpen, setIsMobileMenuOpen] = useState(false);
    const [isAuthenticated, setIsAuthenticated] = useState(false);
    const [user, setUser] = useState<{ id: string; username: string } | null>(null);
    const mobileMenuRef = useRef<HTMLDivElement>(null);
    const buttonRef = useRef<HTMLButtonElement>(null);
    const router = useRouter();

    // Check authentication status on client-side
    useEffect(() => {
        setIsAuthenticated(authStore.isAuthenticated());
        setUser(authStore.getUser());
    }, []);

    const handleLogout = () => {
        authStore.logout();
        setIsAuthenticated(false);
        setUser(null);
        router.push('/login');
    };

    // Close mobile menu when clicking outside
    useEffect(() => {
        const handleClickOutside = (event: MouseEvent) => {
            if (
                mobileMenuRef.current &&
                !mobileMenuRef.current.contains(event.target as Node) &&
                buttonRef.current &&
                !buttonRef.current.contains(event.target as Node)
            ) {
                setIsMobileMenuOpen(false);
            }
        };

        document.addEventListener('mousedown', handleClickOutside);
        return () => {
            document.removeEventListener('mousedown', handleClickOutside);
        };
    }, []);

    return (
        <>
            {/* Desktop navbar */}
            <nav className="bg-gradient-to-r from-purple-600 via-pink-500 to-orange-400 shadow hidden sm:block sticky top-0 z-40">
                <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
                    <div className="flex justify-between h-16">
                        <div className="flex">
                            <div className="ml-6 flex items-center">
                                <Link href="/" className="text-white font-bold text-xl">
                                    WhoBought
                                </Link>
                            </div>
                            <div className="ml-6 flex space-x-8 items-center">
                                <Link href="/"
                                    className="text-white hover:text-yellow-200 px-3 py-2 rounded-md text-sm font-medium transition-colors duration-200 cursor-pointer">
                                    Home
                                </Link>
                                <Link href="/items"
                                    className="text-white hover:text-yellow-200 px-3 py-2 rounded-md text-sm font-medium transition-colors duration-200 cursor-pointer">
                                    Items
                                </Link>
                                {isAuthenticated && (
                                    <Link href="/dashboard"
                                        className="text-white hover:text-yellow-200 px-3 py-2 rounded-md text-sm font-medium transition-colors duration-200 cursor-pointer">
                                        Dashboard
                                    </Link>
                                )}
                            </div>
                        </div>
                        <div className="ml-6 flex items-center">
                            {isAuthenticated ? (
                                <div className="flex items-center space-x-4">
                                    <span className="text-white text-sm">Hi, {user?.username}</span>
                                    <Link href="/profile"
                                        className="text-white hover:text-yellow-200 px-3 py-2 rounded-md text-sm font-medium transition-colors duration-200 cursor-pointer">
                                        Profile
                                    </Link>
                                    <button
                                        onClick={handleLogout}
                                        className="bg-red-600 hover:bg-red-500 text-white px-4 py-2 rounded-md text-sm font-medium transition-colors duration-200 cursor-pointer">
                                        Logout
                                    </button>
                                </div>
                            ) : (
                                <div className="flex items-center space-x-4">
                                    <Link href="/login"
                                        className="text-white hover:text-yellow-200 px-3 py-2 rounded-md text-sm font-medium transition-colors duration-200 cursor-pointer">
                                        Login
                                    </Link>
                                    <Link href="/register"
                                        className="text-white hover:text-yellow-200 px-3 py-2 rounded-md text-sm font-medium transition-colors duration-200 cursor-pointer">
                                        Register
                                    </Link>
                                </div>
                            )}
                        </div>
                    </div>
                </div>
            </nav>

            {/* Mobile bubble menu button - fixed to the bottom right */}
            <div className="fixed bottom-6 right-6 sm:hidden z-50">
                <button
                    ref={buttonRef}
                    onClick={() => setIsMobileMenuOpen(!isMobileMenuOpen)}
                    className={`flex items-center justify-center w-14 h-14 rounded-full shadow-lg cursor-pointer ${isMobileMenuOpen ? 'bg-red-600' : 'bg-gradient-to-r from-purple-600 to-pink-500'} text-white transition-all duration-300 transform ${isMobileMenuOpen ? 'rotate-90' : ''}`}
                    aria-expanded={isMobileMenuOpen}
                >
                    {isMobileMenuOpen ? (
                        <svg
                            className="w-6 h-6"
                            xmlns="http://www.w3.org/2000/svg"
                            fill="none"
                            viewBox="0 0 24 24"
                            stroke="currentColor"
                        >
                            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M6 18L18 6M6 6l12 12" />
                        </svg>
                    ) : (
                        <svg
                            className="w-6 h-6"
                            xmlns="http://www.w3.org/2000/svg"
                            fill="none"
                            viewBox="0 0 24 24"
                            stroke="currentColor"
                        >
                            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M4 6h16M4 12h16M4 18h16" />
                        </svg>
                    )}
                </button>
            </div>

            {/* Mobile menu - speech bubble style, positioned above the button */}
            {isMobileMenuOpen && (
                <div
                    ref={mobileMenuRef}
                    className="fixed bottom-24 right-6 sm:hidden z-40 bg-white rounded-lg shadow-xl w-64 overflow-hidden transform transition-all duration-300 ease-in-out"
                    style={{
                        boxShadow: '0 10px 25px -5px rgba(0, 0, 0, 0.1), 0 10px 10px -5px rgba(0, 0, 0, 0.04)'
                    }}
                >
                    {/* Mobile menu content */}
                    <div className="relative rounded-lg overflow-hidden">
                        <div className="bg-gradient-to-r from-purple-600 to-pink-500 px-4 py-1.5">
                            {isAuthenticated && user && (
                                <div className="text-white text-sm mt-1">Hi, {user.username}</div>
                            )}
                        </div>

                        <div className="p-1">
                            <Link href="/"
                                className="block px-4 py-3 rounded-md text-base font-medium text-purple-700 hover:bg-purple-50 hover:text-pink-600 transition-colors duration-200 cursor-pointer"
                                onClick={() => setIsMobileMenuOpen(false)}
                            >
                                Home
                            </Link>
                            <Link href="/items"
                                className="block px-4 py-3 rounded-md text-base font-medium text-purple-700 hover:bg-purple-50 hover:text-pink-600 transition-colors duration-200 cursor-pointer"
                                onClick={() => setIsMobileMenuOpen(false)}
                            >
                                Items
                            </Link>
                            {isAuthenticated && (
                                <Link href="/dashboard"
                                    className="block px-4 py-3 rounded-md text-base font-medium text-purple-700 hover:bg-purple-50 hover:text-pink-600 transition-colors duration-200 cursor-pointer"
                                    onClick={() => setIsMobileMenuOpen(false)}
                                >
                                    Dashboard
                                </Link>
                            )}
                        </div>

                        <div className="border-t border-gray-200 p-1">
                            {isAuthenticated ? (
                                <>
                                    <Link href="/profile"
                                        className="block px-4 py-3 rounded-md text-base font-medium text-purple-700 hover:bg-purple-50 hover:text-pink-600 transition-colors duration-200 cursor-pointer"
                                        onClick={() => setIsMobileMenuOpen(false)}
                                    >
                                        Profile
                                    </Link>
                                    <button
                                        onClick={() => {
                                            handleLogout();
                                            setIsMobileMenuOpen(false);
                                        }}
                                        className="w-full text-left block px-4 py-3 rounded-md text-base font-medium text-red-600 hover:bg-red-50 transition-colors duration-200 cursor-pointer"
                                    >
                                        Logout
                                    </button>
                                </>
                            ) : (
                                <>
                                    <Link href="/login"
                                        className="block px-4 py-3 rounded-md text-base font-medium text-purple-700 hover:bg-purple-50 hover:text-pink-600 transition-colors duration-200 cursor-pointer"
                                        onClick={() => setIsMobileMenuOpen(false)}
                                    >
                                        Login
                                    </Link>
                                    <Link href="/register"
                                        className="block px-4 py-3 rounded-md text-base font-medium text-purple-700 hover:bg-purple-50 hover:text-pink-600 transition-colors duration-200 cursor-pointer"
                                        onClick={() => setIsMobileMenuOpen(false)}
                                    >
                                        Register
                                    </Link>
                                </>
                            )}
                        </div>
                    </div>

                    {/* Bubble pointer at the bottom */}
                    <div
                        className="absolute bottom-0 right-5 w-4 h-4 bg-white transform rotate-45"
                        style={{
                            marginBottom: '-0.5rem'
                        }}
                    ></div>
                </div>
            )}

            {/* Small app title in the top left corner for mobile users */}
            <div className="sm:hidden bg-white/90 px-2 py-1 rounded-lg shadow-sm absolute top-4 left-4 bg-gradient-to-r from-purple-600 to-pink-500 bg-clip-text text-transparent font-bold text-xl z-30">
                <Link href="/" className="cursor-pointer">
                    WhoBought
                </Link>
            </div>
        </>
    );
};

export default Navbar; 