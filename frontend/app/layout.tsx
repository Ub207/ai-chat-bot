import './globals.css';
import { AuthProvider } from '@/lib/auth-context';

export const metadata = {
  title: 'Todo App Chatbot',
  description: 'AI-powered todo management system',
};

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="en">
      <AuthProvider>
        <body className="antialiased">{children}</body>
      </AuthProvider>
    </html>
  );
}