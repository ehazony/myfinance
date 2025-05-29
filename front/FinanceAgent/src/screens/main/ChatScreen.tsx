"use client"
import { useEffect, useState, useRef, useCallback } from 'react'
import { View, StyleSheet, FlatList, TextInput, Image, Dimensions, KeyboardAvoidingView, Platform, TouchableOpacity, Animated } from 'react-native'
import { Text, Button, useTheme, IconButton, ActivityIndicator } from 'react-native-paper'
import { LineChart } from 'react-native-chart-kit'
import { SafeAreaView } from 'react-native-safe-area-context'
import { LinearGradient } from 'expo-linear-gradient'
import { chatService } from '../../services/chatService'
import { audioService } from '../../services/audioService'
import type { ChatMessage } from '../../types/chat'

const { width: screenWidth } = Dimensions.get('window')

type MessageStatus = 'sending' | 'sent' | 'delivered' | 'failed'

interface EnhancedChatMessage extends ChatMessage {
  status: MessageStatus
}

export default function ChatScreen() {
  const [messages, setMessages] = useState<EnhancedChatMessage[]>([])
  const [text, setText] = useState('')
  const [isTyping, setIsTyping] = useState(false)
  const [isSending, setIsSending] = useState(false)
  const theme = useTheme()
  const flatListRef = useRef<FlatList>(null)
  const typingTimeoutRef = useRef<NodeJS.Timeout>()
  const fadeAnim = useRef(new Animated.Value(0)).current
  const scaleAnim = useRef(new Animated.Value(1)).current

  useEffect(() => {
    initializeAudio()
    loadHistory()
    
    // Fade in animation on mount
    Animated.timing(fadeAnim, {
      toValue: 1,
      duration: 300,
      useNativeDriver: true,
    }).start()

    return () => {
      audioService.cleanup()
      if (typingTimeoutRef.current) {
        clearTimeout(typingTimeoutRef.current)
      }
    }
  }, [])

  const initializeAudio = async () => {
    try {
      await audioService.initialize()
    } catch (error) {
      console.warn('Audio initialization failed:', error)
    }
  }

  const loadHistory = async () => {
    try {
      const history = await chatService.fetchHistory()
      const enhancedHistory = history.map(msg => ({
        ...msg,
        status: 'delivered' as MessageStatus
      }))
      setMessages(enhancedHistory)
      scrollToBottom()
    } catch (err) {
      console.error('Failed to load history', err)
      audioService.playError()
    }
  }

  const scrollToBottom = useCallback(() => {
    setTimeout(() => {
      flatListRef.current?.scrollToEnd({ animated: true })
    }, 100)
  }, [])

  const handleTextChange = useCallback((newText: string) => {
    setText(newText)
    
    // Play typing sound with throttling
    if (typingTimeoutRef.current) {
      clearTimeout(typingTimeoutRef.current)
    }
    
    if (newText.length > text.length) {
      audioService.playTyping()
    }
    
    typingTimeoutRef.current = setTimeout(() => {
      // Stop typing sound after user stops typing
    }, 500)
  }, [text])

  const animateSendButton = () => {
    Animated.sequence([
      Animated.timing(scaleAnim, {
        toValue: 0.9,
        duration: 100,
        useNativeDriver: true,
      }),
      Animated.timing(scaleAnim, {
        toValue: 1,
        duration: 100,
        useNativeDriver: true,
      }),
    ]).start()
  }

  const send = async () => {
    if (!text.trim() || isSending) return
    
    const messageText = text.trim()
    setText('')
    setIsSending(true)
    setIsTyping(true)
    
    // Play send sound and haptic feedback
    audioService.playSend()
    animateSendButton()
    
    try {
      const userMessage: EnhancedChatMessage = {
        id: Date.now(),
        conversation: 1,
        sender: 'user',
        content_type: 'text',
        payload: { text: messageText },
        timestamp: new Date().toISOString(),
        status: 'sending'
      }
      
      setMessages(prev => [...prev, userMessage])
      scrollToBottom()
      
      // Update message status to sent
      setTimeout(() => {
        setMessages(prev => prev.map(msg => 
          msg.id === userMessage.id ? { ...msg, status: 'sent' } : msg
        ))
      }, 500)
      
      const reply = await chatService.sendMessage(messageText)
      const enhancedReply: EnhancedChatMessage = {
        ...reply,
        status: 'delivered'
      }
      
      // Update user message to delivered
      setMessages(prev => prev.map(msg => 
        msg.id === userMessage.id ? { ...msg, status: 'delivered' } : msg
      ))
      
      // Add AI reply with animation
      setTimeout(() => {
        setMessages(prev => [...prev, enhancedReply])
        audioService.playReceive()
        scrollToBottom()
      }, 300)
      
      audioService.playSuccess()
      
    } catch (err) {
      console.error('Send failed', err)
      audioService.playError()
      
      // Update message status to failed
      setMessages(prev => prev.map(msg => 
        msg.id === Date.now() ? { ...msg, status: 'failed' } : msg
      ))
    } finally {
      setIsSending(false)
      setIsTyping(false)
    }
  }

  const renderMessageStatus = (status: MessageStatus) => {
    switch (status) {
      case 'sending':
        return <ActivityIndicator size="small" color="#9CA3AF" style={styles.statusIndicator} />
      case 'sent':
        return <Text style={styles.statusText}>✓</Text>
      case 'delivered':
        return <Text style={styles.statusText}>✓✓</Text>
      case 'failed':
        return <Text style={[styles.statusText, { color: '#EF4444' }]}>!</Text>
      default:
        return null
    }
  }

  const renderItem = ({ item, index }: { item: EnhancedChatMessage; index: number }) => {
    const isUser = item.sender === 'user'
    const isLastMessage = index === messages.length - 1
    
    const bubbleStyle = [
      styles.messageBubble,
      isUser ? styles.userBubble : styles.agentBubble,
      isLastMessage && styles.lastMessage
    ]

    let content
    if (item.content_type === 'text') {
      content = (
        <Text style={[
          styles.messageText,
          { color: isUser ? '#FFFFFF' : theme.colors.onSurface }
        ]}>
          {(item.payload as any).text}
        </Text>
      )
    } else if (item.content_type === 'image') {
      content = (
        <View style={styles.imageContainer}>
          <Image 
            source={{ uri: (item.payload as any).url }} 
            style={styles.messageImage} 
            resizeMode="cover" 
          />
        </View>
      )
    } else if (item.content_type === 'buttons') {
      content = (
        <View style={styles.buttonContainer}>
          {(item.payload as any).buttons.map((buttonText: string, btnIndex: number) => (
            <TouchableOpacity
              key={btnIndex}
              style={[styles.chatButton, { borderColor: theme.colors.primary }]}
              onPress={() => {
                audioService.playButtonTap()
                setText(buttonText)
              }}
            >
              <Text style={[styles.chatButtonText, { color: theme.colors.primary }]}>
                {buttonText}
              </Text>
            </TouchableOpacity>
          ))}
        </View>
      )
    } else if (item.content_type === 'chart') {
      const payload = item.payload as any
      if (payload.labels && payload.values) {
        content = (
          <View style={styles.chartContainer}>
            <LineChart
              data={{
                labels: payload.labels,
                datasets: [
                  {
                    data: payload.values,
                    color: (opacity = 1) => `rgba(59, 130, 246, ${opacity})`,
                    strokeWidth: 3,
                  },
                ],
              }}
              width={Math.min(screenWidth * 0.75, 300)}
              height={200}
              chartConfig={{
                backgroundColor: 'transparent',
                backgroundGradientFrom: 'transparent',
                backgroundGradientTo: 'transparent',
                decimalPlaces: 0,
                color: (opacity = 1) => `rgba(59, 130, 246, ${opacity})`,
                labelColor: (opacity = 1) => `rgba(107, 114, 128, ${opacity})`,
                style: {
                  borderRadius: 16,
                },
                propsForDots: {
                  r: '6',
                  strokeWidth: '2',
                  stroke: '#3B82F6',
                },
                propsForBackgroundLines: {
                  strokeDasharray: '5,5',
                  stroke: '#E5E7EB',
                  strokeWidth: 1,
                },
              }}
              style={styles.chart}
              bezier
            />
          </View>
        )
      } else if (payload.url || payload.chart_url) {
        // Fallback for chart images returned by the backend
        const imageUrl = payload.url ?? payload.chart_url
        content = (
          <View style={styles.imageContainer}>
            <Image
              source={{ uri: imageUrl }}
              style={styles.messageImage}
              resizeMode="cover"
            />
          </View>
        )
      }
    }

    return (
      <Animated.View 
        style={[
          styles.messageContainer, 
          isUser ? styles.userContainer : styles.agentContainer,
          { opacity: fadeAnim }
        ]}
      >
        {!isUser && (
          <View style={styles.avatarContainer}>
            <LinearGradient
              colors={[theme.colors.primary, theme.colors.secondary]}
              style={styles.avatar}
            >
              <Text style={styles.avatarText}>AI</Text>
            </LinearGradient>
          </View>
        )}
        
        <View style={bubbleStyle}>
          {isUser ? (
            <LinearGradient
              colors={['#3B82F6', '#1D4ED8']}
              style={styles.userGradient}
              start={{ x: 0, y: 0 }}
              end={{ x: 1, y: 1 }}
            >
              {content}
            </LinearGradient>
          ) : (
            <View style={[styles.agentContent, { backgroundColor: theme.colors.surface }]}>
              {content}
            </View>
          )}
        </View>
        
        {isUser && (
          <View style={styles.avatarContainer}>
            <View style={[styles.avatar, { backgroundColor: theme.colors.primary }]}>
              <Text style={styles.avatarText}>You</Text>
            </View>
          </View>
        )}
        
        {isUser && (
          <View style={styles.statusContainer}>
            {renderMessageStatus(item.status)}
          </View>
        )}
      </Animated.View>
    )
  }

  const renderTypingIndicator = () => {
    if (!isTyping) return null
    
    return (
      <Animated.View style={[styles.messageContainer, styles.agentContainer, { opacity: fadeAnim }]}>
        <View style={styles.avatarContainer}>
          <LinearGradient
            colors={[theme.colors.primary, theme.colors.secondary]}
            style={styles.avatar}
          >
            <Text style={styles.avatarText}>AI</Text>
          </LinearGradient>
        </View>
        
        <View style={[styles.messageBubble, styles.agentBubble]}>
          <View style={[styles.agentContent, { backgroundColor: theme.colors.surface }]}>
            <View style={styles.typingIndicator}>
              <Animated.View style={[styles.typingDot, styles.typingDot1]} />
              <Animated.View style={[styles.typingDot, styles.typingDot2]} />
              <Animated.View style={[styles.typingDot, styles.typingDot3]} />
            </View>
          </View>
        </View>
      </Animated.View>
    )
  }

  return (
    <LinearGradient
      colors={[theme.colors.background, theme.colors.surface]}
      style={styles.container}
    >
      <SafeAreaView style={styles.safeArea}>
        <KeyboardAvoidingView 
          style={styles.keyboardView}
          behavior={Platform.OS === 'ios' ? 'padding' : 'height'}
          keyboardVerticalOffset={Platform.OS === 'ios' ? 90 : 0}
        >
          <FlatList 
            ref={flatListRef}
            data={messages} 
            renderItem={renderItem} 
            keyExtractor={(item) => item.id.toString()}
            contentContainerStyle={styles.messagesList}
            showsVerticalScrollIndicator={false}
            ListFooterComponent={renderTypingIndicator}
            onContentSizeChange={scrollToBottom}
            onLayout={scrollToBottom}
          />
          
          <View style={[styles.inputContainer, { backgroundColor: theme.colors.surface }]}>
            <View style={styles.inputWrapper}>
              <TextInput
                style={[styles.textInput, { 
                  backgroundColor: theme.colors.background,
                  color: theme.colors.onBackground,
                  borderColor: theme.colors.outline
                }]}
                value={text}
                onChangeText={handleTextChange}
                placeholder="Type your message..."
                placeholderTextColor={theme.colors.onSurfaceVariant}
                multiline
                maxLength={500}
                editable={!isSending}
              />
              
              <Animated.View style={{ transform: [{ scale: scaleAnim }] }}>
                <TouchableOpacity
                  style={[styles.sendButton, { opacity: text.trim() && !isSending ? 1 : 0.5 }]}
                  onPress={send}
                  disabled={!text.trim() || isSending}
                  onPressIn={() => audioService.playButtonTap()}
                >
                  <LinearGradient
                    colors={['#3B82F6', '#1D4ED8']}
                    style={styles.sendGradient}
                    start={{ x: 0, y: 0 }}
                    end={{ x: 1, y: 1 }}
                  >
                    {isSending ? (
                      <ActivityIndicator size="small" color="#FFFFFF" />
                    ) : (
                      <IconButton
                        icon="send"
                        iconColor="#FFFFFF"
                        size={20}
                        style={styles.sendIcon}
                      />
                    )}
                  </LinearGradient>
                </TouchableOpacity>
              </Animated.View>
            </View>
          </View>
        </KeyboardAvoidingView>
      </SafeAreaView>
    </LinearGradient>
  )
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
  },
  safeArea: {
    flex: 1,
  },
  keyboardView: {
    flex: 1,
  },
  messagesList: {
    paddingHorizontal: 16,
    paddingTop: 16,
    paddingBottom: 8,
  },
  messageContainer: {
    flexDirection: 'row',
    marginBottom: 16,
    alignItems: 'flex-end',
  },
  userContainer: {
    justifyContent: 'flex-end',
  },
  agentContainer: {
    justifyContent: 'flex-start',
  },
  avatarContainer: {
    marginHorizontal: 8,
  },
  avatar: {
    width: 32,
    height: 32,
    borderRadius: 16,
    justifyContent: 'center',
    alignItems: 'center',
    shadowColor: '#000',
    shadowOffset: { width: 0, height: 2 },
    shadowOpacity: 0.1,
    shadowRadius: 4,
    elevation: 3,
  },
  avatarText: {
    color: '#FFFFFF',
    fontSize: 10,
    fontWeight: '600',
  },
  messageBubble: {
    maxWidth: screenWidth * 0.75,
    borderRadius: 20,
    shadowColor: '#000',
    shadowOffset: { width: 0, height: 2 },
    shadowOpacity: 0.1,
    shadowRadius: 8,
    elevation: 4,
  },
  userBubble: {
    borderBottomRightRadius: 6,
  },
  agentBubble: {
    borderBottomLeftRadius: 6,
  },
  lastMessage: {
    marginBottom: 24,
  },
  userGradient: {
    borderRadius: 20,
    borderBottomRightRadius: 6,
    padding: 16,
  },
  agentContent: {
    borderRadius: 20,
    borderBottomLeftRadius: 6,
    padding: 16,
  },
  messageText: {
    fontSize: 16,
    lineHeight: 22,
    fontWeight: '400',
  },
  imageContainer: {
    borderRadius: 12,
    overflow: 'hidden',
  },
  messageImage: {
    width: 250,
    height: 180,
    borderRadius: 12,
  },
  buttonContainer: {
    flexDirection: 'row',
    flexWrap: 'wrap',
    marginTop: 8,
  },
  chatButton: {
    borderWidth: 1.5,
    borderRadius: 20,
    paddingHorizontal: 16,
    paddingVertical: 8,
    margin: 4,
    backgroundColor: 'rgba(59, 130, 246, 0.05)',
  },
  chatButtonText: {
    fontSize: 14,
    fontWeight: '500',
  },
  chartContainer: {
    alignItems: 'center',
    marginVertical: 8,
  },
  chart: {
    borderRadius: 16,
  },
  typingIndicator: {
    flexDirection: 'row',
    alignItems: 'center',
    paddingVertical: 8,
  },
  typingDot: {
    width: 8,
    height: 8,
    borderRadius: 4,
    backgroundColor: '#9CA3AF',
    marginHorizontal: 2,
  },
  typingDot1: {
    animationDelay: '0ms',
  },
  typingDot2: {
    animationDelay: '150ms',
  },
  typingDot3: {
    animationDelay: '300ms',
  },
  statusContainer: {
    marginLeft: 4,
    justifyContent: 'flex-end',
    paddingBottom: 4,
  },
  statusIndicator: {
    width: 16,
    height: 16,
  },
  statusText: {
    fontSize: 12,
    color: '#9CA3AF',
    fontWeight: '500',
  },
  inputContainer: {
    paddingHorizontal: 16,
    paddingVertical: 12,
    borderTopWidth: 1,
    borderTopColor: 'rgba(0, 0, 0, 0.1)',
    shadowColor: '#000',
    shadowOffset: { width: 0, height: -2 },
    shadowOpacity: 0.05,
    shadowRadius: 8,
    elevation: 8,
  },
  inputWrapper: {
    flexDirection: 'row',
    alignItems: 'flex-end',
  },
  textInput: {
    flex: 1,
    borderWidth: 1,
    borderRadius: 24,
    paddingHorizontal: 16,
    paddingVertical: 12,
    marginRight: 12,
    fontSize: 16,
    maxHeight: 100,
    minHeight: 48,
    textAlignVertical: 'center',
  },
  sendButton: {
    width: 48,
    height: 48,
    borderRadius: 24,
    justifyContent: 'center',
    alignItems: 'center',
  },
  sendGradient: {
    width: 48,
    height: 48,
    borderRadius: 24,
    justifyContent: 'center',
    alignItems: 'center',
  },
  sendIcon: {
    margin: 0,
  },
})
