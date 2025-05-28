import axios from 'axios'
import { secureStorage } from '../utils/secureStorage'
import type { ChatMessage } from '../types/chat'

// TODO: replace with real backend url
const API_BASE_URL = 'http://localhost:8000'

class ChatService {
  private axiosInstance = axios.create({ baseURL: API_BASE_URL })

  private async authHeaders() {
    const token = await secureStorage.getToken()
    return token ? { Authorization: `Token ${token}` } : {}
  }

  async sendMessage(text: string): Promise<ChatMessage> {
    const headers = await this.authHeaders()
    const res = await this.axiosInstance.post('/api/chat/send/', { text }, { headers })
    return res.data
  }

  async fetchHistory(): Promise<ChatMessage[]> {
    const headers = await this.authHeaders()
    const res = await this.axiosInstance.get('/api/chat/history/', { headers })
    return res.data
  }
}

export const chatService = new ChatService()
