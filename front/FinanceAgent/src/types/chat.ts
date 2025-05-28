export interface ChatMessage {
  id: number
  conversation: number
  sender: 'user' | 'agent'
  content_type: string
  payload: any
  timestamp: string
  status: string
}
