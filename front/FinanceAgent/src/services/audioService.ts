import { Audio } from 'expo-av'
import * as Haptics from 'expo-haptics'

class AudioService {
  private sounds: { [key: string]: Audio.Sound } = {}
  private isEnabled = true

  async initialize() {
    try {
      await Audio.setAudioModeAsync({
        allowsRecordingIOS: false,
        staysActiveInBackground: false,
        playsInSilentModeIOS: true,
        shouldDuckAndroid: true,
        playThroughEarpieceAndroid: false,
      })

      // Load sound effects
      await this.loadSounds()
    } catch (error) {
      console.warn('Audio initialization failed:', error)
    }
  }

  private async loadSounds() {
    try {
      // Create simple sound effects programmatically since we don't have audio files
      // In a real app, you'd load actual audio files here
      
      // For now, we'll use haptic feedback as the primary feedback mechanism
      // and create placeholder sound objects
      this.sounds = {
        typing: new Audio.Sound(),
        send: new Audio.Sound(),
        receive: new Audio.Sound(),
        buttonTap: new Audio.Sound(),
      }
    } catch (error) {
      console.warn('Failed to load sounds:', error)
    }
  }

  async playTyping() {
    if (!this.isEnabled) return
    
    try {
      // Use light haptic feedback for typing
      await Haptics.impactAsync(Haptics.ImpactFeedbackStyle.Light)
    } catch (error) {
      console.warn('Typing feedback failed:', error)
    }
  }

  async playSend() {
    if (!this.isEnabled) return
    
    try {
      // Use medium haptic feedback for sending
      await Haptics.impactAsync(Haptics.ImpactFeedbackStyle.Medium)
      
      // Create a subtle "send" sound effect using Web Audio API if available
      if (typeof window !== 'undefined' && window.AudioContext) {
        this.createSendTone()
      }
    } catch (error) {
      console.warn('Send feedback failed:', error)
    }
  }

  async playReceive() {
    if (!this.isEnabled) return
    
    try {
      // Use light haptic feedback for receiving
      await Haptics.impactAsync(Haptics.ImpactFeedbackStyle.Light)
      
      // Create a subtle "receive" sound effect
      if (typeof window !== 'undefined' && window.AudioContext) {
        this.createReceiveTone()
      }
    } catch (error) {
      console.warn('Receive feedback failed:', error)
    }
  }

  async playButtonTap() {
    if (!this.isEnabled) return
    
    try {
      // Use selection haptic feedback for button taps
      await Haptics.selectionAsync()
    } catch (error) {
      console.warn('Button tap feedback failed:', error)
    }
  }

  async playSuccess() {
    if (!this.isEnabled) return
    
    try {
      // Use success haptic feedback
      await Haptics.notificationAsync(Haptics.NotificationFeedbackType.Success)
    } catch (error) {
      console.warn('Success feedback failed:', error)
    }
  }

  async playError() {
    if (!this.isEnabled) return
    
    try {
      // Use error haptic feedback
      await Haptics.notificationAsync(Haptics.NotificationFeedbackType.Error)
    } catch (error) {
      console.warn('Error feedback failed:', error)
    }
  }

  private createSendTone() {
    try {
      if (typeof window === 'undefined' || !window.AudioContext) return
      
      const audioContext = new (window.AudioContext || (window as any).webkitAudioContext)()
      const oscillator = audioContext.createOscillator()
      const gainNode = audioContext.createGain()
      
      oscillator.connect(gainNode)
      gainNode.connect(audioContext.destination)
      
      oscillator.frequency.setValueAtTime(800, audioContext.currentTime)
      oscillator.frequency.exponentialRampToValueAtTime(400, audioContext.currentTime + 0.1)
      
      gainNode.gain.setValueAtTime(0.1, audioContext.currentTime)
      gainNode.gain.exponentialRampToValueAtTime(0.01, audioContext.currentTime + 0.1)
      
      oscillator.start(audioContext.currentTime)
      oscillator.stop(audioContext.currentTime + 0.1)
    } catch (error) {
      console.warn('Send tone creation failed:', error)
    }
  }

  private createReceiveTone() {
    try {
      if (typeof window === 'undefined' || !window.AudioContext) return
      
      const audioContext = new (window.AudioContext || (window as any).webkitAudioContext)()
      const oscillator = audioContext.createOscillator()
      const gainNode = audioContext.createGain()
      
      oscillator.connect(gainNode)
      gainNode.connect(audioContext.destination)
      
      oscillator.frequency.setValueAtTime(400, audioContext.currentTime)
      oscillator.frequency.exponentialRampToValueAtTime(600, audioContext.currentTime + 0.15)
      
      gainNode.gain.setValueAtTime(0.05, audioContext.currentTime)
      gainNode.gain.exponentialRampToValueAtTime(0.01, audioContext.currentTime + 0.15)
      
      oscillator.start(audioContext.currentTime)
      oscillator.stop(audioContext.currentTime + 0.15)
    } catch (error) {
      console.warn('Receive tone creation failed:', error)
    }
  }

  setEnabled(enabled: boolean) {
    this.isEnabled = enabled
  }

  isAudioEnabled() {
    return this.isEnabled
  }

  async cleanup() {
    try {
      // Cleanup sound objects
      for (const sound of Object.values(this.sounds)) {
        if (sound) {
          await sound.unloadAsync()
        }
      }
      this.sounds = {}
    } catch (error) {
      console.warn('Audio cleanup failed:', error)
    }
  }
}

export const audioService = new AudioService() 