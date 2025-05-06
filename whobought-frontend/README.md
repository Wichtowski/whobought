# WhoBought Frontend

A Next.js frontend application for the WhoBought project that connects to a .NET backend API.

## Getting Started

### Prerequisites

- Node.js 18+ installed
- .NET 8.0+ installed and running the WhoBought backend API

### Setup

1. Clone the repository
   ```bash
   git clone https://github.com/yourusername/whobought.git
   cd whobought/whobought-frontend
   ```

2. Install dependencies
   ```bash
   npm install
   ```

3. Configure environment variables
   ```bash
   cp .env.example .env.local
   ```
   
   Then edit `.env.local` to match your backend API URL:
   ```
   NEXT_PUBLIC_API_URL=https://localhost:5001/api
   JWT_SECRET=your-secret-key-here  # Make sure this matches your backend
   ```

4. Start the development server
   ```bash
   npm run dev
   ```

5. Open [http://localhost:3000](http://localhost:3000) in your browser

## Project Structure

- `/app` - Next.js App Router based structure
  - `/components` - Reusable UI components
  - `/dashboard` - Dashboard pages (protected)
  - `/login` - Login page
  - `/register` - Registration page
  - `/store` - State management (authStore)
  - `/utils` - Utility functions including API calls

## Authentication

This application uses JWT-based authentication. The authentication flow:

1. User logs in/registers through the frontend
2. Backend validates credentials and returns a JWT token
3. Frontend stores the token in localStorage
4. Protected routes check for valid token before rendering

## API Requests

All API requests to the backend use the utility function in `/app/utils/api.ts`. This function:

- Automatically adds authentication headers
- Handles errors consistently
- Provides type safety for requests and responses

## Backend Integration

This frontend is designed to work with a .NET backend that provides:

- `/Auth/login` - POST endpoint for user login
- `/Auth/register` - POST endpoint for user registration
- Other API endpoints for application functionality

Make sure your .NET backend is correctly configured with CORS to allow requests from this frontend.
