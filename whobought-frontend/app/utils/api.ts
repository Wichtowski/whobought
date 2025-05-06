// API utility for making authenticated requests

// .NET API Base URL - this should be set in your environment variables
const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'https://localhost:5001/api';

type RequestOptions = {
    method?: string;
    body?: any;
    headers?: Record<string, string>;
    requiresAuth?: boolean;
};

/**
 * Make an API request to our .NET backend
 * @param endpoint - The API endpoint path (e.g., '/Items')
 * @param options - Request options (method, body, headers, requiresAuth)
 * @returns Promise with the fetch response
 */
export async function apiRequest<T>(
    endpoint: string,
    options: RequestOptions = {}
): Promise<T> {
    const {
        method = 'GET',
        body,
        headers = {},
        requiresAuth = true,
    } = options;

    // Ensure endpoint doesn't start with a slash when combining with base URL
    const normalizedEndpoint = endpoint.startsWith('/') ? endpoint.slice(1) : endpoint;
    const url = `${API_BASE_URL}/${normalizedEndpoint}`;

    // Base headers
    const requestHeaders: Record<string, string> = {
        'Content-Type': 'application/json',
        ...headers,
    };

    // Add auth token if required and available
    if (requiresAuth) {
        const token = localStorage.getItem('auth_token');
        if (token) {
            requestHeaders['Authorization'] = `Bearer ${token}`;
        }
    }

    // Prepare request options
    const requestOptions: RequestInit = {
        method,
        headers: requestHeaders,
    };

    // Add body for non-GET requests
    if (body && method !== 'GET') {
        requestOptions.body = JSON.stringify(body);
    }

    try {
        const response = await fetch(url, requestOptions);

        // Check if the response is ok (status in the range 200-299)
        if (!response.ok) {
            const errorData = await response.json();
            throw new Error(errorData.message || 'API request failed');
        }

        // Parse JSON response
        const data = await response.json();
        return data as T;
    } catch (error) {
        console.error(`API request to ${url} failed:`, error);
        throw error;
    }
}

/**
 * Check if the current user is authenticated
 * @returns boolean indicating if user is authenticated
 */
export function isAuthenticated(): boolean {
    return !!localStorage.getItem('auth_token');
}

/**
 * Get the current authentication token
 * @returns The current token or null if not authenticated
 */
export function getAuthToken(): string | null {
    return localStorage.getItem('auth_token');
}

/**
 * Handle API errors in a standardized way
 * @param error - The error object
 * @returns A human-readable error message
 */
export function handleApiError(error: any): string {
    if (error instanceof Error) {
        return error.message;
    }
    return 'An unknown error occurred';
} 