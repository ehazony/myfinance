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

import type { z } from 'zod'
import { schemas } from '../api/client'

export type ChatMessage = z.infer<typeof schemas.Message>

