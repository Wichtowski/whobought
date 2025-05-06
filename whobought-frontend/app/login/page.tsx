'use client';

import { useRouter } from 'next/navigation';
import authStore from '../store/authStore';
import AuthForm, { FormField } from '../components/AuthForm';

export default function Login() {
  const router = useRouter();

  const fields: FormField[] = [
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
      autoComplete: 'current-password',
      required: true
    }
  ];

  const handleLogin = async (formData: Record<string, string>) => {
    await authStore.login(formData.email, formData.password);
    router.push('/dashboard');
  };

  return (
    <AuthForm
      title="Sign in to your account"
      fields={fields}
      submitButtonText="Sign in"
      loadingText="Signing in..."
      altLink={{
        text: 'Or',
        linkText: 'create a new account',
        href: '/register'
      }}
      onSubmit={handleLogin}
    />
  );
} 