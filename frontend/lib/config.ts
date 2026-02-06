/**
 * Frontend configuration for Todo App Chatbot Phase III.
 * All chat requests go to the Hugging Face backend - no API keys required.
 */

// Hugging Face backend URL (Phase-3)
const HF_BACKEND_URL = 'https://ubaid-ai-bot.hf.space';

interface AppConfig {
  apiUrl: string;
  enableAnalytics: boolean;
  maintenanceMode: boolean;
}

function validateBoolean(value: string | undefined, defaultValue: boolean): boolean {
  if (value === undefined) return defaultValue;
  return value.toLowerCase() === 'true';
}

function loadConfig(): AppConfig {
  // Use NEXT_PUBLIC_BACKEND_URL or fallback to HF backend - no API key needed
  const apiUrl =
    process.env.NEXT_PUBLIC_BACKEND_URL?.trim() ||
    process.env.NEXT_PUBLIC_API_BASE_URL?.trim() ||
    HF_BACKEND_URL;

  try {
    new URL(apiUrl);
  } catch {
    throw new Error(`Invalid API URL: ${apiUrl}`);
  }

  return {
    apiUrl: apiUrl.replace(/\/$/, ''), // strip trailing slash
    enableAnalytics: validateBoolean(process.env.NEXT_PUBLIC_ENABLE_ANALYTICS, false),
    maintenanceMode: validateBoolean(process.env.NEXT_PUBLIC_MAINTENANCE_MODE, false),
  };
}

const config: AppConfig = loadConfig();

function getApiUrl(): string {
  return config.apiUrl;
}

function isDevelopment(): boolean {
  return process.env.NODE_ENV === 'development';
}

function isProduction(): boolean {
  return process.env.NODE_ENV === 'production';
}

function areAnalyticsEnabled(): boolean {
  return config.enableAnalytics;
}

function isMaintenanceMode(): boolean {
  return config.maintenanceMode;
}

export {
  config,
  getApiUrl,
  isDevelopment,
  isProduction,
  areAnalyticsEnabled,
  isMaintenanceMode,
  type AppConfig,
};
