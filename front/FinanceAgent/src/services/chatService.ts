import { schemas } from '../api/client'
import { authService } from './authService'
import type { z } from 'zod'

export type ChatMessage = z.infer<typeof schemas.Message>

class ChatService {
  // Use the authenticated API client from authService
  private get apiClient() {
    return (authService as any).apiClient
  }

  async sendMessage(text: string): Promise<ChatMessage> {
    const res = await this.apiClient.api_chat_send_create({ text })
    return res
  }

  async fetchHistory(): Promise<ChatMessage[]> {
    const res = await this.apiClient.api_chat_history_retrieve()
    return res
  }
}

export const chatService = new ChatService()
