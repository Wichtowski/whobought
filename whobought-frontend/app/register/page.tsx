'use client'

import { useRouter } from 'next/navigation';
import authStore from '../store/authStore';
import AuthForm from '../components/AuthForm';
import { FormField } from '../types/form/types';

export default function Register() {
  const router = useRouter();

  const fields: FormField[] = [
    {
      id: 'username',
      name: 'username',
      type: 'text',
      label: 'Username',
      autoComplete: 'username',
      required: true
    },
    {
      id: 'email',
      name: 'email',
      type: 'email',
      label: 'Email address',
      autoComplete: 'email',
      required: true
    },
    {
      id: 'password',
      name: 'password',
      type: 'password',
      label: 'Password',
      autoComplete: 'new-password',
      required: true
    },
    {
      id: 'confirmPassword',
      name: 'confirmPassword',
      type: 'password',
      label: 'Confirm Password',
      autoComplete: 'new-password',
      required: true
    }
  ];

  const handleRegister = async (formData: Record<string, string>) => {
    if (formData.password !== formData.confirmPassword) {
      throw new Error('Passwords do not match');
    }

    if (formData.password.length < 6) {
      throw new Error('Password must be at least 6 characters long');
    }

    await authStore.register(formData.username, formData.email, formData.password);
    router.push('/dashboard');
  };

  return (
    <AuthForm
      title="Create a new account"
      fields={fields}
      submitButtonText="Create account"
      loadingText="Creating account..."
      altLink={{
        text: 'Or',
        linkText: 'sign in to your account',
        href: '/login'
      }}
      onSubmit={handleRegister}
    />
  );
} 