export type ChatContentType = 'text' | 'image' | 'buttons' | 'chart'

/**
 * Payload sent with a chat message.
 * - `url` is used for regular images
 * - `chart_url` is returned by the reporting backend when a chart image is generated
 */
export type ChatPayload =
  | { text: string }
  | { url: string }
  | { chart_url: string }
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
