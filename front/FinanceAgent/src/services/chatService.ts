import { createApiClient, schemas } from '../api/client'
import { secureStorage } from '../utils/secureStorage'
import type { z } from 'zod'

export type ChatMessage = z.infer<typeof schemas.Message>

// TODO: replace with real backend url
const API_BASE_URL = 'http://localhost:8000'

class ChatService {
  private apiClient = createApiClient(API_BASE_URL)

  private async authHeaders() {
    const token = await secureStorage.getToken()
    return token ? { Authorization: `Token ${token}` } : {}
  }

  async sendMessage(text: string): Promise<ChatMessage> {
    const headers = await this.authHeaders()
    const res = await this.apiClient.api_chat_send_create({ body: { text } }, { headers })
    return res
  }

  async fetchHistory(): Promise<ChatMessage[]> {
    const headers = await this.authHeaders()
    const res = await this.apiClient.api_chat_history_retrieve(undefined, { headers })
    return res
  }
}

export const chatService = new ChatService()
