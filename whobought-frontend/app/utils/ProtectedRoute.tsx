'use client';

import { ReactNode, useEffect, useState } from 'react';
import { useRouter } from 'next/navigation';
import authStore from '../store/authStore';

interface ProtectedRouteProps {
    children: ReactNode;
    redirectTo?: string;
}

/**
 * A component that protects routes by checking authentication status
 * Redirects to login if user is not authenticated
 */
export default function ProtectedRoute({
    children,
    redirectTo = '/login'
}: ProtectedRouteProps) {
    const [isLoading, setIsLoading] = useState(true);
    const router = useRouter();

    useEffect(() => {
        // Check if user is authenticated
        const isAuthenticated = authStore.isAuthenticated();

        if (!isAuthenticated) {
            router.push(redirectTo);
        } else {
            setIsLoading(false);
        }
    }, [redirectTo, router]);

    // Show nothing while checking authentication or redirecting
    if (isLoading) {
        return (
            <div className="flex justify-center items-center min-h-[50vh]">
                <div className="animate-pulse text-purple-600 font-semibold">Loading...</div>
            </div>
        );
    }

    // If authenticated and done loading, render children
    return <>{children}</>;
} 