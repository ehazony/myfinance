"use client"
import { useEffect, useState } from 'react'
import { View, StyleSheet, FlatList, TextInput } from 'react-native'
import { Text, Button, useTheme } from 'react-native-paper'
import { SafeAreaView } from 'react-native-safe-area-context'
import { chatService } from '../../services/chatService'
import type { ChatMessage } from '../../types/chat'

export default function ChatScreen() {
  const [messages, setMessages] = useState<ChatMessage[]>([])
  const [text, setText] = useState('')
  const theme = useTheme()

  useEffect(() => {
    loadHistory()
  }, [])

  const loadHistory = async () => {
    try {
      const history = await chatService.fetchHistory()
      setMessages(history)
    } catch (err) {
      console.error('Failed to load history', err)
    }
  }

  const send = async () => {
    if (!text.trim()) return
    try {
      const reply = await chatService.sendMessage(text)
      const userMessage: ChatMessage = {
        id: Date.now(),
        conversation: reply.conversation,
        sender: 'user',
        content_type: 'text',
        payload: { text },
        timestamp: new Date().toISOString(),
        status: 'sent'
      }
      setMessages(prev => [...prev, userMessage, reply])
      setText('')
    } catch (err) {
      console.error('Send failed', err)
    }
  }

  const renderItem = ({ item }: { item: ChatMessage }) => (
    <View
      style={[
        styles.message,
        item.sender === 'user' ? styles.user : styles.agent,
        {
          backgroundColor:
            item.sender === 'user' ? theme.colors.primary : theme.colors.surfaceVariant
        }
      ]}
    >
      <Text style={{ color: item.sender === 'user' ? '#fff' : theme.colors.onSurface }}>
        {item.payload.text}
      </Text>
    </View>
  )

  return (
    <SafeAreaView style={styles.container}>
      <FlatList data={messages} renderItem={renderItem} keyExtractor={m => m.id.toString()} contentContainerStyle={styles.list} />
      <View style={styles.inputRow}>
        <TextInput style={styles.input} value={text} onChangeText={setText} placeholder="Message" />
        <Button mode="contained" onPress={send}>
          Send
        </Button>
      </View>
    </SafeAreaView>
  )
}

const styles = StyleSheet.create({
  container: { flex: 1 },
  list: { padding: 16 },
  message: { padding: 8, borderRadius: 8, marginBottom: 8, maxWidth: '80%' },
  user: { alignSelf: 'flex-end' },
  agent: { alignSelf: 'flex-start' },
  inputRow: { flexDirection: 'row', padding: 8, alignItems: 'center' },
  input: { flex: 1, marginRight: 8 }
})
