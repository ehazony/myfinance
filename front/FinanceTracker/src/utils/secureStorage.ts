import * as SecureStore from 'expo-secure-store';

const TOKEN_KEY = 'auth_token';
const TOKEN_EXPIRY_KEY = 'auth_token_expiry';
const REFRESH_TOKEN_KEY = 'refresh_token';

export const secureStorage = {
  async setToken(token: string, expiryHours: number = 24): Promise<void> {
    try {
      const expiryTime = new Date();
      expiryTime.setTime(expiryTime.getTime() + (expiryHours * 60 * 60 * 1000));
      
      await Promise.all([
        SecureStore.setItemAsync(TOKEN_KEY, token),
        SecureStore.setItemAsync(TOKEN_EXPIRY_KEY, expiryTime.toISOString())
      ]);
    } catch (error) {
      console.error('Error storing token:', error);
      throw error;
    }
  },

  async getToken(): Promise<string | null> {
    try {
      const [token, expiryString] = await Promise.all([
        SecureStore.getItemAsync(TOKEN_KEY),
        SecureStore.getItemAsync(TOKEN_EXPIRY_KEY)
      ]);

      if (!token || !expiryString) {
        return null;
      }

      // Check if token has expired
      const expiryTime = new Date(expiryString);
      const now = new Date();
      
      if (now > expiryTime) {
        console.log('Token has expired, removing...');
        await this.removeToken();
        return null;
      }

      return token;
    } catch (error) {
      console.error('Error retrieving token:', error);
      return null;
    }
  },

  async removeToken(): Promise<void> {
    try {
      await Promise.all([
        SecureStore.deleteItemAsync(TOKEN_KEY),
        SecureStore.deleteItemAsync(TOKEN_EXPIRY_KEY)
      ]);
    } catch (error) {
      console.error('Error removing token:', error);
      throw error;
    }
  },

  async setRefreshToken(refreshToken: string): Promise<void> {
    try {
      await SecureStore.setItemAsync(REFRESH_TOKEN_KEY, refreshToken);
    } catch (error) {
      console.error('Error storing refresh token:', error);
      throw error;
    }
  },

  async getRefreshToken(): Promise<string | null> {
    try {
      return await SecureStore.getItemAsync(REFRESH_TOKEN_KEY);
    } catch (error) {
      console.error('Error retrieving refresh token:', error);
      return null;
    }
  },

  async removeRefreshToken(): Promise<void> {
    try {
      await SecureStore.deleteItemAsync(REFRESH_TOKEN_KEY);
    } catch (error) {
      console.error('Error removing refresh token:', error);
      throw error;
    }
  },

  async clearAll(): Promise<void> {
    try {
      await Promise.all([
        this.removeToken(),
        this.removeRefreshToken(),
      ]);
    } catch (error) {
      console.error('Error clearing all tokens:', error);
      throw error;
    }
  },

  // Check if token exists and is valid (not expired)
  async isTokenValid(): Promise<boolean> {
    const token = await this.getToken();
    return token !== null;
  }
}; 