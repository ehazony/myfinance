export type ChatContentType = 'text' | 'image' | 'buttons' | 'chart'

export type ChatPayload =
  | { text: string }
  | { url: string }
  | { buttons: string[] }
  | { labels: string[]; values: number[] }

export interface ChatMessage {
  id: number
  conversation: number
  sender: 'user' | 'agent'
  content_type: ChatContentType
  payload: ChatPayload
  timestamp: string
  status: string
}
