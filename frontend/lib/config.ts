/**
 * Frontend configuration module for Todo App Chatbot Phase III.
 *
 * This module handles environment variable loading and validation for the frontend.
 * It ensures all required environment variables are present and provides helpful
 * error messages if they are missing.
 */

// Define the expected shape of our configuration
interface AppConfig {
  apiUrl: string;
  betterAuthUrl: string;
  appEnv: string;
  openaiDomain: string;
  enableAnalytics: boolean;
  maintenanceMode: boolean;
}

/**
 * Validates that a string value is present and not empty.
 * @param value The value to validate
 * @param name The name of the variable (for error messages)
 * @returns The validated value
 */
function validateRequired(value: string | undefined, name: string): string {
  if (!value || value.trim() === '') {
    throw new Error(
      `${name} environment variable is required. ` +
      `Please set NEXT_PUBLIC_${name.replace(' ', '_').toUpperCase()} in your .env.local file.`
    );
  }
  return value;
}

/**
 * Validates that a boolean environment variable is properly formatted.
 * @param value The value to validate
 * @param defaultValue The default value to use if the variable is not set
 * @returns The parsed boolean value
 */
function validateBoolean(value: string | undefined, defaultValue: boolean): boolean {
  if (value === undefined) {
    return defaultValue;
  }
  return value.toLowerCase() === 'true';
}

/**
 * Validates that a URL environment variable is properly formatted.
 * @param value The URL value to validate
 * @param name The name of the variable (for error messages)
 * @returns The validated URL value
 */
function validateUrl(value: string | undefined, name: string): string {
  const validatedValue = validateRequired(value, name);
  try {
    new URL(validatedValue);
    return validatedValue;
  } catch (error) {
    throw new Error(
      `${name} must be a valid URL. Got: ${validatedValue}`
    );
  }
}

/**
 * Loads and validates the application configuration from environment variables.
 * @returns The validated application configuration
 */
function loadConfig(): AppConfig {
  try {
    // Validate required string values
    const apiUrl = validateUrl(process.env.NEXT_PUBLIC_API_URL, 'API URL');
    const betterAuthUrl = validateUrl(process.env.NEXT_PUBLIC_BETTER_AUTH_URL, 'Better Auth URL');
    const appEnv = validateRequired(process.env.NEXT_PUBLIC_APP_ENV, 'App Environment');
    const openaiDomain = validateUrl(process.env.NEXT_PUBLIC_OPENAI_DOMAIN, 'OpenAI Domain');

    // Validate optional boolean values
    const enableAnalytics = validateBoolean(process.env.NEXT_PUBLIC_ENABLE_ANALYTICS, false);
    const maintenanceMode = validateBoolean(process.env.NEXT_PUBLIC_MAINTENANCE_MODE, false);

    // Additional validation for app environment
    const validEnvironments = ['development', 'production', 'staging', 'test'];
    if (!validEnvironments.includes(appEnv.toLowerCase())) {
      console.warn(
        `Warning: NEXT_PUBLIC_APP_ENV is set to "${appEnv}" which is not a standard environment. ` +
        `Expected one of: ${validEnvironments.join(', ')}`
      );
    }

    return {
      apiUrl,
      betterAuthUrl,
      appEnv,
      openaiDomain,
      enableAnalytics,
      maintenanceMode,
    };
  } catch (error) {
    console.error('Configuration validation failed:', error);
    throw new Error(
      'Failed to load application configuration. ' +
      'Please check your environment variables in .env.local file. ' +
      'Refer to .env.local.example for the required variables.'
    );
  }
}

/**
 * The application configuration object.
 * This is loaded once when the module is imported.
 */
const config: AppConfig = loadConfig();

/**
 * Validates the configuration and provides helpful error messages.
 * This can be called during app initialization to ensure all settings are valid.
 */
function validateConfig(): void {
  try {
    // Try to load the config again to trigger validation
    loadConfig();
    console.log('✓ Frontend configuration is valid and ready for use.');
  } catch (error) {
    console.error('❌ Frontend configuration validation failed:', error);
    throw error;
  }
}

/**
 * Gets the base API URL for backend requests.
 * @returns The API URL
 */
function getApiUrl(): string {
  return config.apiUrl;
}

/**
 * Gets the OpenAI API key.
 * @returns The OpenAI API key
 */
function getBetterAuthUrl(): string {
  return config.betterAuthUrl;
}

/**
 * Gets the OpenAI domain URL.
 * @returns The OpenAI domain URL
 */
function getOpenAiDomain(): string {
  return config.openaiDomain;
}

/**
 * Checks if the app is running in development mode.
 * @returns True if in development mode, false otherwise
 */
function isDevelopment(): boolean {
  return config.appEnv.toLowerCase() === 'development';
}

/**
 * Checks if the app is running in production mode.
 * @returns True if in production mode, false otherwise
 */
function isProduction(): boolean {
  return config.appEnv.toLowerCase() === 'production';
}

/**
 * Checks if analytics are enabled.
 * @returns True if analytics are enabled, false otherwise
 */
function areAnalyticsEnabled(): boolean {
  return config.enableAnalytics;
}

/**
 * Checks if maintenance mode is enabled.
 * @returns True if maintenance mode is enabled, false otherwise
 */
function isMaintenanceMode(): boolean {
  return config.maintenanceMode;
}

// Export the configuration and helper functions
export {
  config,
  validateConfig,
  getApiUrl,
  getBetterAuthUrl,
  getOpenAiDomain,
  isDevelopment,
  isProduction,
  areAnalyticsEnabled,
  isMaintenanceMode,
  type AppConfig,
};

// Validate the configuration when the module is loaded in development
if (typeof window !== 'undefined' && isDevelopment()) {
  validateConfig();
}