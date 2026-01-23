'use client';

import { useState, useEffect } from 'react';
import { useSearchParams, useRouter } from 'next/navigation';
import ChatInterface from '@/components/ChatInterface';
import ConversationList from '@/components/ConversationList';
import { getConversations, createConversation } from '@/lib/chat-api';

export default function ChatPage() {
  const router = useRouter();
  const searchParams = useSearchParams();
  const [conversations, setConversations] = useState<any[]>([]);
  const [selectedConversationId, setSelectedConversationId] = useState<number | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  // Check if there's a user_id in the URL and remove it for Phase-3 compatibility
  useEffect(() => {
    const urlUserId = searchParams.get('user_id');
    if (urlUserId) {
      // Redirect to clean URL without user_id for Phase-3 compatibility
      router.replace('/chat');
    }
  }, [searchParams, router]);

  useEffect(() => {
    const fetchConversations = async () => {
      try {
        setLoading(true);
        const userConversations = await getConversations(); // Updated for Hackathon-2 Phase-3
        setConversations(userConversations);

        // Set the first conversation as selected if none is selected
        if (userConversations.length > 0 && !selectedConversationId) {
          setSelectedConversationId(userConversations[0].id);
        }
      } catch (err) {
        setError('Failed to load conversations');
        console.error(err);
      } finally {
        setLoading(false);
      }
    };

    fetchConversations();
  }, [selectedConversationId]); // Removed dependency on userId since we don't use it anymore

  const handleNewConversation = async () => {
    try {
      const newConversation = await createConversation(); // Updated for Hackathon-2 Phase-3
      setConversations([newConversation, ...conversations]);
      setSelectedConversationId(newConversation.id);
      // No need to change URL since we're removing user_id routing
    } catch (err) {
      setError('Failed to create new conversation');
      console.error(err);
    }
  };

  const handleConversationSelect = (conversationId: number) => {
    setSelectedConversationId(conversationId);
    // No need to change URL since we're removing user_id routing
  };

  if (error) {
    return (
      <div className="flex items-center justify-center min-h-screen bg-gray-50">
        <div className="text-center">
          <h2 className="text-xl font-semibold text-red-600">Error</h2>
          <p className="text-gray-600 mt-2">{error}</p>
          <button
            onClick={() => window.location.reload()}
            className="mt-4 px-4 py-2 bg-blue-600 text-white rounded-md hover:bg-blue-700"
          >
            Retry
          </button>
        </div>
      </div>
    );
  }

  if (loading) {
    return (
      <div className="flex items-center justify-center min-h-screen bg-gray-50">
        <div className="animate-spin rounded-full h-12 w-12 border-t-2 border-b-2 border-blue-600"></div>
      </div>
    );
  }

  return (
    <div className="flex flex-col md:flex-row h-screen bg-gray-50">
      {/* Sidebar for conversations */}
      <div className="w-full md:w-64 lg:w-80 flex-shrink-0 border-r border-gray-200 bg-white">
        <ConversationList
          conversations={conversations}
          currentConversationId={selectedConversationId}
          onSelectConversation={handleConversationSelect}
          onNewConversation={handleNewConversation}
          loading={loading}
        />
      </div>

      {/* Main chat area */}
      <div className="flex-grow flex flex-col">
        {selectedConversationId ? (
          <ChatInterface
            userId="demo_user" // Use demo user for Hackathon-2 Phase-3
            conversationId={selectedConversationId}
          />
        ) : (
          <div className="flex-grow flex items-center justify-center">
            <div className="text-center p-8">
              <h2 className="text-2xl font-semibold text-gray-800 mb-2">No conversation selected</h2>
              <p className="text-gray-600 mb-6">Select a conversation from the sidebar or start a new one</p>
              <button
                onClick={handleNewConversation}
                className="px-6 py-3 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors shadow-sm"
              >
                Start New Conversation
              </button>
            </div>
          </div>
        )}
      </div>
    </div>
  );
}