import { Conversation, Message as MessageInterface, ChatResponse, ChatRequest } from '@/types';

// API client for chat functionality
const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://127.0.0.1:8000';

// Get JWT token from wherever it's stored (e.g., localStorage, cookies)
const getAuthToken = (): string | null => {
  if (typeof window !== 'undefined') {
    // In browser environment
    return localStorage.getItem('auth_token');
  }
  return null;
};

// Set up default headers with authentication
const getHeaders = (): HeadersInit => {
  const headers: HeadersInit = {
    'Content-Type': 'application/json',
  };

  const token = getAuthToken();
  if (token) {
    headers['Authorization'] = `Bearer ${token}`;
  }

  return headers;
};

// Send a message to the chat API
export const sendMessage = async (
  conversation_id: number,
  message: string
): Promise<ChatResponse> => {
  // Validate that message is not empty or just whitespace
  if (!message || message.trim().length === 0) {
    throw new Error('Message content cannot be empty');
  }

  try {
    const response = await fetch(`${API_BASE_URL}/conversations/${conversation_id}/messages`, {
      method: 'POST',
      headers: getHeaders(),
      body: JSON.stringify({
        message: message.trim(), // Send only the message as expected by the backend
      }),
    });

    if (!response.ok) {
      const errorData = await response.json().catch(() => ({}));
      throw new Error(errorData.message || `HTTP error! status: ${response.status}`);
    }

    const data: ChatResponse = await response.json();
    return data;
  } catch (error) {
    console.error('Error sending message:', error);
    throw error;
  }
};

// Get user's conversations
export const getConversations = async (): Promise<Conversation[]> => {
  try {
    const response = await fetch(`${API_BASE_URL}/conversations`, {
      method: 'GET',
      headers: getHeaders(),
    });

    if (!response.ok) {
      const errorData = await response.json().catch(() => ({}));
      throw new Error(errorData.message || `HTTP error! status: ${response.status}`);
    }

    const data: Conversation[] = await response.json();
    return data;
  } catch (error) {
    console.error('Error fetching conversations:', error);
    throw error;
  }
};

// Create a new conversation
export const createConversation = async (): Promise<Conversation> => {
  try {
    const response = await fetch(`${API_BASE_URL}/conversations/`, {
      method: 'POST',
      headers: getHeaders(),
      body: JSON.stringify({}),
    });

    if (!response.ok) {
      const errorData = await response.json().catch(() => ({}));
      throw new Error(errorData.message || `HTTP error! status: ${response.status}`);
    }

    const data: Conversation = await response.json();
    return data;
  } catch (error) {
    console.error('Error creating conversation:', error);
    throw error;
  }
};

// Get messages for a specific conversation
export const getConversationMessages = async (conversation_id: number): Promise<MessageInterface[]> => {
  try {
    const response = await fetch(`${API_BASE_URL}/conversations/${conversation_id}/messages`, {
      method: 'GET',
      headers: getHeaders(),
    });

    if (!response.ok) {
      const errorData = await response.json().catch(() => ({}));
      throw new Error(errorData.message || `HTTP error! status: ${response.status}`);
    }

    const data: MessageInterface[] = await response.json();
    return data;
  } catch (error) {
    console.error('Error fetching conversation messages:', error);
    throw error;
  }
};