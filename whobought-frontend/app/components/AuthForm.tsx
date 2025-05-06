'use client';

import { useState } from 'react';
import Link from 'next/link';
import { FormField, AuthFormProps } from '@/app/types/form/types';

export default function AuthForm({
    title,
    fields,
    submitButtonText,
    loadingText,
    altLink,
    onSubmit,
}: AuthFormProps) {
    const [formData, setFormData] = useState<Record<string, string>>(
        Object.fromEntries(fields.map(field => [field.id, '']))
    );
    const [error, setError] = useState('');
    const [isLoading, setIsLoading] = useState(false);

    const handleInputChange = (id: string, value: string) => {
        setFormData(prev => ({ ...prev, [id]: value }));
    };

    const handleSubmit = async (e: React.FormEvent) => {
        e.preventDefault();

        // Check if all required fields are filled
        const emptyRequiredField = fields
            .filter(field => field.required !== false)
            .find(field => !formData[field.id]);

        if (emptyRequiredField) {
            setError('Please fill in all required fields');
            return;
        }

        setIsLoading(true);
        setError('');

        try {
            await onSubmit(formData);
        } catch (err: any) {
            setError(err.message || 'An error occurred. Please try again.');
        } finally {
            setIsLoading(false);
        }
    };

    return (
        <>
            {title && altLink && (
                <div className="flex min-h-full flex-col justify-center py-12 px-4 sm:px-6 lg:px-8">
                    <div className="rounded-lg sm:mx-auto sm:w-full sm:max-w-md sm:rounded-lg">
                        <h2 className="mt-6 text-center text-3xl font-bold tracking-tight bg-gradient-to-r from-purple-600 to-pink-500 bg-clip-text text-transparent">
                            {title}
                        </h2>
                        <p className="mt-2 text-center text-sm text-gray-600">
                            Or{' '}
                            <Link href={altLink.href} className="font-medium text-purple-600 hover:text-purple-500">
                                {altLink.linkText}
                            </Link>
                        </p>
                    </div>
                </div>
            )}
            <div className="mt-8 sm:mx-auto sm:w-full sm:max-w-md ml-2 mr-2">
                <div className="bg-white py-6 px-4 shadow rounded-lg sm:rounded-lg sm:px-10">
                    {error && (
                        <div className="bg-red-50 border-l-4 border-red-500 p-4 mb-6">
                            <p className="text-red-700">{error}</p>
                        </div>
                    )}

                    <form className="space-y-6" onSubmit={handleSubmit}>
                        {fields.map((field) => (
                            <div key={field.id}>
                                <label htmlFor={field.id} className="block text-sm font-medium text-gray-700">
                                    {field.label}
                                </label>
                                <div className="mt-1">
                                    <input
                                        id={field.id}
                                        name={field.name}
                                        type={field.type}
                                        autoComplete={field.autoComplete}
                                        required={field.required !== false}
                                        value={formData[field.id]}
                                        onChange={(e) => handleInputChange(field.id, e.target.value)}
                                        className="block w-full appearance-none rounded-md border border-gray-300 px-3 py-2 placeholder-gray-400 shadow-sm focus:border-purple-500 focus:outline-none focus:ring-purple-500 sm:text-sm"
                                    />
                                </div>
                            </div>
                        ))}

                        <div>
                            <button
                                type="submit"
                                disabled={isLoading}
                                className={`flex w-full justify-center rounded-md border border-transparent px-4 py-2 text-sm font-medium text-white shadow-sm cursor-pointer ${isLoading ? 'bg-purple-400' : 'bg-purple-600 hover:bg-purple-700'
                                    } focus:outline-none focus:ring-2 focus:ring-purple-500 focus:ring-offset-2`}
                            >
                                {isLoading ? loadingText : submitButtonText}
                            </button>
                        </div>
                    </form>
                </div>
            </div>
        </>
    );
} 