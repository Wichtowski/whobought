'use client';

// Simple auth store for managing authentication state
export type User = {
    id: string;
    username: string;
};

// Local storage keys
const TOKEN_KEY = 'auth_token';
const USER_KEY = 'auth_user';

// .NET API Base URL - this should be set in your environment variables
const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'https://localhost:5001/api';

// Auth Store - Simple functions to manage auth state
const authStore = {
    // Get token from localStorage
    getToken: (): string | null => {
        if (typeof window !== 'undefined') {
            return localStorage.getItem(TOKEN_KEY);
        }
        return null;
    },

    // Get user from localStorage
    getUser: (): User | null => {
        if (typeof window !== 'undefined') {
            const userData = localStorage.getItem(USER_KEY);
            return userData ? JSON.parse(userData) : null;
        }
        return null;
    },

    // Check if user is authenticated
    isAuthenticated: (): boolean => {
        return !!authStore.getToken();
    },

    // Set auth data after login/register
    setAuth: (token: string, user: User): void => {
        if (typeof window !== 'undefined') {
            localStorage.setItem(TOKEN_KEY, token);
            localStorage.setItem(USER_KEY, JSON.stringify(user));
        }
    },

    // Clear auth data on logout
    clearAuth: (): void => {
        if (typeof window !== 'undefined') {
            localStorage.removeItem(TOKEN_KEY);
            localStorage.removeItem(USER_KEY);
        }
    },

    // Login user
    login: async (email: string, password: string): Promise<{ token: string; user: User }> => {
        try {
            const response = await fetch(`${API_BASE_URL}/Auth/login`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ email, password }),
            });

            if (!response.ok) {
                const error = await response.json();
                throw new Error(error.message || 'Login failed');
            }

            const data = await response.json();

            const user = {
                id: data.userId,
                username: data.username,
            };

            // Store token and user data
            authStore.setAuth(data.token, user);

            return { token: data.token, user };
        } catch (error) {
            console.error('Login failed:', error);
            throw error;
        }
    },

    // Register user
    register: async (username: string, email: string, password: string): Promise<{ token: string; user: User }> => {
        try {
            const response = await fetch(`${API_BASE_URL}/Auth/register`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ username, email, password }),
            });

            if (!response.ok) {
                const error = await response.json();
                throw new Error(error.message || 'Registration failed');
            }

            const data = await response.json();

            const user = {
                id: data.userId,
                username: data.username,
            };

            // Store token and user data
            authStore.setAuth(data.token, user);

            return { token: data.token, user };
        } catch (error) {
            console.error('Registration failed:', error);
            throw error;
        }
    },

    // Logout user
    logout: (): void => {
        authStore.clearAuth();
    },

    // Add auth header to fetch requests
    getAuthHeader: (): { Authorization: string } | Record<string, never> => {
        const token = authStore.getToken();
        return token ? { Authorization: `Bearer ${token}` } : {};
    }
};

export default authStore; 