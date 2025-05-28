export interface User {
  id: number;
  username: string;
  email: string;
  first_name: string;
  last_name: string;
  is_staff: boolean;
  is_active: boolean;
  date_joined: string;
}

export interface LoginRequest {
  username?: string;
  email?: string;
  password: string;
  [key: string]: any; // Add index signature for API client compatibility
}

export interface LoginResponse {
  key: string;
}

export interface RegisterRequest {
  username: string;
  email: string;
  password1: string;
  password2: string;
  first_name?: string;
  last_name?: string;
  [key: string]: any; // Add index signature for API client compatibility
}

export interface AuthState {
  user: User | null;
  token: string | null;
  isAuthenticated: boolean;
  isLoading: boolean;
  error: string | null;
}

export interface AuthContextType extends AuthState {
  login: (email: string, password: string) => Promise<void>;
  register: (email: string, password: string, name: string) => Promise<void>;
  logout: () => Promise<void>;
  clearError: () => void;
}

export interface ApiError {
  message: string;
  status?: number;
  details?: Record<string, string[]>;
} 