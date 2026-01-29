# Todo Frontend

A modern Next.js frontend for the Todo application with full CRUD functionality.

## Features

- Create, read, update, and delete todos
- Real-time statistics
- Responsive design
- Error handling and API connection status
- Clean, accessible UI

## Tech Stack

- Next.js 14
- React 18
- TypeScript
- Tailwind CSS (via imports)
- Zustand (state management)

## Getting Started

### Prerequisites

- Node.js 18+
- npm or yarn

### Installation

1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd frontend
   ```

2. Install dependencies:
   ```bash
   npm install
   ```

3. Set up environment variables:
   ```bash
   cp .env.local.example .env.local
   ```

   Update the `NEXT_PUBLIC_API_URL` variable to point to your backend API:
   ```env
   NEXT_PUBLIC_API_URL=http://localhost:8000/api  # For local development
   # Or for production:
   # NEXT_PUBLIC_API_URL=https://your-backend-domain.com/api
   ```

4. Run the development server:
   ```bash
   npm run dev
   ```

   The app will be available at http://localhost:3000

## Environment Variables

- `NEXT_PUBLIC_API_URL`: The URL of the backend API (required)

## Building for Production

```bash
npm run build
```

## Deployment

### Deploy to Vercel

The easiest way to deploy this Next.js application is to use [Vercel](https://vercel.com), the creators of Next.js.

[![Deploy with Vercel](https://vercel.com/button)](https://vercel.com/new/clone?repository-url=https://github.com/your-username/your-repo/tree/main/frontend&env=NEXT_PUBLIC_API_URL&envDescription=Backend%20API%20URL%20for%20the%20Todo%20application)

#### Prerequisites

Before deploying, make sure you have:

1. A deployed backend API (either self-hosted or on a platform like Vercel, Heroku, etc.)
2. The URL of your backend API ready to configure

#### Manual Vercel Deployment

1. Install the Vercel CLI:
   ```bash
   npm i -g vercel
   ```

2. Login to your Vercel account:
   ```bash
   vercel login
   ```

3. Navigate to the frontend directory:
   ```bash
   cd frontend
   ```

4. Deploy the project with your backend API URL:
   ```bash
   vercel --env NEXT_PUBLIC_API_URL='https://your-backend-api.com/api'
   ```

   Or deploy without environment variables and set them in the Vercel dashboard:
   ```bash
   vercel
   ```

#### Git Integration (Recommended)

The recommended approach is to link your GitHub/GitLab/Bitbucket repository to Vercel:

1. Push your code to a Git repository
2. Go to [Vercel Dashboard](https://vercel.com/dashboard)
3. Click "New Project" and import your repository
4. Select the `frontend` directory as your project root
5. Set the `NEXT_PUBLIC_API_URL` environment variable in the project settings
6. Vercel will automatically deploy on pushes to your repository

### Environment Configuration for Vercel

When deploying to Vercel, make sure to set the following environment variable:

- `NEXT_PUBLIC_API_URL`: URL of your deployed backend API (e.g., `https://your-backend-app.vercel.app/api` or `https://yourdomain.com/api`)

## API Integration

This frontend connects to a backend API that provides the following endpoints:
- `GET /api/todos` - Get all todos
- `POST /api/todos` - Create a new todo
- `PATCH /api/todos/:id/status` - Update todo status
- `DELETE /api/todos/:id` - Delete a todo

## Scripts

- `npm run dev` - Start development server
- `npm run build` - Build for production
- `npm run start` - Start production server
- `npm run lint` - Run linter
- `npm run test` - Run tests
- `npm run test:watch` - Run tests in watch mode
- `npm run test:coverage` - Run tests with coverage

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request