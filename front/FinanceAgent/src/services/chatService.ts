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
    console.log('ChatService: Sending message:', text)
    try {
      const res = await this.apiClient.api_chat_send_create({ text })
      console.log('ChatService: Received response:', res)
      return res
    } catch (error) {
      console.error('ChatService: Error sending message:', error)
      throw error
    }
  }

  async fetchHistory(): Promise<ChatMessage[]> {
    console.log('ChatService: Fetching history')
    try {
      const res = await this.apiClient.api_chat_history_retrieve()
      console.log('ChatService: Received history:', res)
      return res
    } catch (error) {
      console.error('ChatService: Error fetching history:', error)
      throw error
    }
  }
}

export const chatService = new ChatService()
