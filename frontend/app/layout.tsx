import './globals.css';

export const metadata = {
  title: 'Todo App Chatbot',
  description: 'AI-powered todo management system',
};

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="en">
      <body className="antialiased">{children}</body>
    </html>
  );
}