import { getApiUrl } from './config';
import { Conversation, Message as MessageInterface, ChatResponse, ChatRequest } from '@/types';

// API client for chat functionality
const API_BASE_URL = getApiUrl();

// Set up default headers (no authentication needed for Phase-3)
const getHeaders = (): HeadersInit => {
  return {
    'Content-Type': 'application/json',
  };
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
      let errorMessage = errorData.message || `HTTP error! status: ${response.status}`;

      // Sanitize error message to prevent displaying backend API key prompts
      if (errorMessage.toLowerCase().includes('api key')) {
        errorMessage = 'An unexpected error occurred. Please try again or contact support.';
      }

      throw new Error(errorMessage);
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
      let errorMessage = errorData.message || `HTTP error! status: ${response.status}`;

      // Sanitize error message to prevent displaying backend API key prompts
      if (errorMessage.toLowerCase().includes('api key')) {
        errorMessage = 'An unexpected error occurred. Please try again or contact support.';
      }

      throw new Error(errorMessage);
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
      let errorMessage = errorData.message || `HTTP error! status: ${response.status}`;

      // Sanitize error message to prevent displaying backend API key prompts
      if (errorMessage.toLowerCase().includes('api key')) {
        errorMessage = 'An unexpected error occurred. Please try again or contact support.';
      }

      throw new Error(errorMessage);
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
      let errorMessage = errorData.message || `HTTP error! status: ${response.status}`;

      // Sanitize error message to prevent displaying backend API key prompts
      if (errorMessage.toLowerCase().includes('api key')) {
        errorMessage = 'An unexpected error occurred. Please try again or contact support.';
      }

      throw new Error(errorMessage);
    }

    const data: MessageInterface[] = await response.json();
    return data;
  } catch (error) {
    console.error('Error fetching conversation messages:', error);
    throw error;
  }
};