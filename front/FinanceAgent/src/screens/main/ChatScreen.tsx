"use client"
import { useEffect, useState } from 'react'
import { View, StyleSheet, FlatList, TextInput, Image, Dimensions } from 'react-native'
import { Text, Button, useTheme } from 'react-native-paper'
import { LineChart } from 'react-native-chart-kit'
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

  const renderItem = ({ item }: { item: ChatMessage }) => {
    const containerStyle = [
      styles.message,
      item.sender === 'user' ? styles.user : styles.agent,
      {
        backgroundColor:
          item.sender === 'user' ? theme.colors.primary : theme.colors.surfaceVariant
      }
    ]

    let content
    if (item.content_type === 'text') {
      content = (
        <Text style={{ color: item.sender === 'user' ? '#fff' : theme.colors.onSurface }}>
          {(item.payload as any).text}
        </Text>
      )
    } else if (item.content_type === 'image') {
      content = (
        <Image source={{ uri: (item.payload as any).url }} style={styles.image} resizeMode="contain" />
      )
    } else if (item.content_type === 'buttons') {
      content = (
        <View style={styles.buttonRow}>
          {(item.payload as any).buttons.map((b: string) => (
            <Button key={b} mode="outlined" style={styles.button} onPress={() => setText(b)}>
              {b}
            </Button>
          ))}
        </View>
      )
    } else if (item.content_type === 'chart') {
      const { labels, values } = item.payload as any
      content = (
        <LineChart
          data={{ labels, datasets: [{ data: values }] }}
          width={Dimensions.get('window').width * 0.6}
          height={180}
          chartConfig={{
            backgroundGradientFrom: 'transparent',
            backgroundGradientTo: 'transparent',
            color: () => theme.colors.primary,
            labelColor: () => theme.colors.onSurface,
          }}
          style={{ marginVertical: 8 }}
        />
      )
    }

    return <View style={containerStyle}>{content}</View>
  }

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
  message: { padding: 12, borderRadius: 12, marginBottom: 12, maxWidth: '80%' },
  user: { alignSelf: 'flex-end' },
  agent: { alignSelf: 'flex-start' },
  inputRow: { flexDirection: 'row', padding: 8, alignItems: 'center' },
  input: { flex: 1, marginRight: 8 },
  image: { width: 200, height: 150, borderRadius: 8 },
  buttonRow: { flexDirection: 'row', flexWrap: 'wrap' },
  button: { margin: 4 }
})
