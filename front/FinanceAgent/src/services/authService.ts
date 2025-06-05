import { createApiClient } from '../api/client';
import { secureStorage } from '../utils/secureStorage';
import type { LoginRequest, RegisterRequest, User, ApiError } from '../types/auth';

// TODO: Replace with your actual backend URL
const API_BASE_URL = 'http://localhost:8000'; // or your backend URL

class AuthService {
  private apiClient;

  constructor() {
    this.apiClient = createApiClient(API_BASE_URL, {
      axiosConfig: {
        headers: {
          'Content-Type': 'application/json',
        },
      },
    });

    // Add response interceptor to suppress console errors for expected HTTP error status codes
    this.apiClient.axios.interceptors.response.use(
      (response) => response,
      (error) => {
        // Don't log expected client errors (4xx) to console
        // These are handled gracefully by our error handling logic
        if (error.response && error.response.status >= 400 && error.response.status < 500) {
          // Suppress console logging for client errors
          return Promise.reject(error);
        }
        
        // For server errors (5xx) or network errors, we still want to see them in console
        console.error('API Error:', error);
        return Promise.reject(error);
      }
    );
  }

  async setAuthToken(token: string) {
    console.log('AuthService: Setting auth token:', token.substring(0, 10) + '...')
    // Set the token for future requests
    this.apiClient.axios.defaults.headers.common['Authorization'] = `Token ${token}`;
    await secureStorage.setToken(token);
  }

  async removeAuthToken() {
    console.log('AuthService: Removing auth token')
    delete this.apiClient.axios.defaults.headers.common['Authorization'];
    await secureStorage.removeToken();
  }

  async restoreAuthToken(): Promise<string | null> {
    const token = await secureStorage.getToken();
    if (token) {
      console.log('AuthService: Restoring auth token:', token.substring(0, 10) + '...')
      this.apiClient.axios.defaults.headers.common['Authorization'] = `Token ${token}`;
    } else {
      console.log('AuthService: No token found to restore')
    }
    return token;
  }

  async login(email: string, password: string): Promise<{ token: string; user: User }> {
    try {
      const loginData: LoginRequest = {
        email,
        password,
      };

      const response = await this.apiClient.dj_rest_auth_login_create(loginData);
      const token = response.key;

      // Set the token for future requests
      await this.setAuthToken(token);

      // Get user details
      const userResponse = await this.apiClient.dj_rest_auth_user_retrieve();
      
      return {
        token,
        user: {
          id: userResponse.pk,
          username: userResponse.username,
          email: userResponse.email,
          first_name: userResponse.first_name || '',
          last_name: userResponse.last_name || '',
          is_staff: false, // UserDetails doesn't include this, would need full User endpoint
          is_active: true,
          date_joined: new Date().toISOString(),
        },
      };
    } catch (error: any) {
      // Only log unexpected errors, not authentication failures (400 status)
      if (!error.response || error.response.status !== 400) {
        console.error('Login error:', error);
      }
      throw this.handleApiError(error);
    }
  }

  async register(email: string, password: string, name: string): Promise<{ token: string; user: User }> {
    try {
      const [firstName, ...lastNameParts] = name.split(' ');
      const lastName = lastNameParts.join(' ');

      const registerData: RegisterRequest = {
        username: email, // Using email as username
        email,
        password1: password,
        password2: password,
        first_name: firstName,
        last_name: lastName,
      };

      const response = await this.apiClient.dj_rest_auth_registration_create(registerData);
      const token = response.key;

      // Set the token for future requests
      await this.setAuthToken(token);

      // Get user details
      const userResponse = await this.apiClient.dj_rest_auth_user_retrieve();
      
      return {
        token,
        user: {
          id: userResponse.pk,
          username: userResponse.username,
          email: userResponse.email,
          first_name: userResponse.first_name || '',
          last_name: userResponse.last_name || '',
          is_staff: false,
          is_active: true,
          date_joined: new Date().toISOString(),
        },
      };
    } catch (error: any) {
      // Only log unexpected errors, not registration failures (400 status)
      if (!error.response || error.response.status !== 400) {
        console.error('Registration error:', error);
      }
      throw this.handleApiError(error);
    }
  }

  async logout(): Promise<void> {
    try {
      // Call logout endpoint if token exists
      const token = await secureStorage.getToken();
      if (token) {
        await this.apiClient.dj_rest_auth_logout_create(undefined);
      }
    } catch (error) {
      console.error('Logout API error:', error);
      // Continue with local logout even if API call fails
    } finally {
      // Always clear local storage
      await this.removeAuthToken();
    }
  }

  async getCurrentUser(): Promise<User | null> {
    try {
      const token = await this.restoreAuthToken();
      if (!token) {
        return null;
      }

      const userResponse = await this.apiClient.dj_rest_auth_user_retrieve();
      
      return {
        id: userResponse.pk,
        username: userResponse.username,
        email: userResponse.email,
        first_name: userResponse.first_name || '',
        last_name: userResponse.last_name || '',
        is_staff: false,
        is_active: true,
        date_joined: new Date().toISOString(),
      };
    } catch (error: any) {
      // Only log unexpected errors, not authentication failures (401/403 status)
      if (!error.response || (error.response.status !== 401 && error.response.status !== 403)) {
        console.error('Get current user error:', error);
      }
      // If token is invalid, clear it
      await this.removeAuthToken();
      return null;
    }
  }

  private handleApiError(error: any): ApiError {
    if (error.response) {
      // Server responded with error status
      const status = error.response.status;
      const data = error.response.data;
      
      let message = 'An error occurred';
      let details: Record<string, string[]> | undefined;

      if (typeof data === 'object' && data !== null) {
        // Handle specific field errors (like the old dashboard app)
        if (data.password) {
          message = Array.isArray(data.password) ? data.password[0] : data.password;
        } else if (data.username) {
          message = Array.isArray(data.username) ? data.username[0] : data.username;
        } else if (data.email) {
          message = Array.isArray(data.email) ? data.email[0] : data.email;
        } else if (data.non_field_errors) {
          message = Array.isArray(data.non_field_errors) 
            ? data.non_field_errors[0] 
            : data.non_field_errors;
        } else if (data.detail) {
          message = data.detail;
        } else {
          // Handle any other field-specific errors
          details = data;
          const firstErrorKey = Object.keys(data)[0];
          if (firstErrorKey && data[firstErrorKey]) {
            const firstError = data[firstErrorKey];
            message = Array.isArray(firstError) && firstError.length > 0 
              ? firstError[0] 
              : firstError;
          }
        }
      }

      return {
        message,
        status,
        details,
      };
    } else if (error.request) {
      // Network error
      return {
        message: 'Network error. Please check your connection.',
      };
    } else {
      // Other error
      return {
        message: error.message || 'An unexpected error occurred',
      };
    }
  }
}

export const authService = new AuthService(); 