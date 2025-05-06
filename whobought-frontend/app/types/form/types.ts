export type FormField = {
    id: string;
    name: string;
    type: string;
    label: string;
    autoComplete?: string;
    required?: boolean;
};

export type AuthFormProps = {
    title?: string;
    fields: FormField[];
    submitButtonText: string;
    loadingText: string;
    altLink?: {
        text: string;
        linkText: string;
        href: string;
    };
    onSubmit: (formData: Record<string, string>) => Promise<void>;
};