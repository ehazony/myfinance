import React, { useEffect, useRef } from 'react'
import {
  Modal,
  View,
  Image,
  TouchableOpacity,
  Animated,
  Dimensions,
  StyleSheet,
  StatusBar,
} from 'react-native'
import { BlurView } from 'expo-blur'
import { ActivityIndicator, Text, IconButton } from 'react-native-paper'
import { SafeAreaView } from 'react-native-safe-area-context'
import ChartCard from './ChartCard'

const { width: screenWidth, height: screenHeight } = Dimensions.get('window')

interface MediaModalProps {
  visible: boolean
  type: 'chart' | 'image' | null
  data: any // chartData for charts, imageUrl for images
  onClose: () => void
  title?: string
  originalWidth?: number // Add original dimensions
  originalHeight?: number
}

const MediaModal: React.FC<MediaModalProps> = ({ visible, type, data, onClose, title, originalWidth, originalHeight }) => {
  const scaleAnim = useRef(new Animated.Value(0.7)).current
  const opacityAnim = useRef(new Animated.Value(0)).current
  const backdropOpacity = useRef(new Animated.Value(0)).current
  const [imageLoaded, setImageLoaded] = React.useState(false)
  const [imageError, setImageError] = React.useState(false)
  const [showModal, setShowModal] = React.useState(false)
  
  // Smart container sizing for chart readability
  const maxWidth = screenWidth - 40 // Leave 20px margin on each side
  const maxHeight = screenHeight - 10 // Maximum available space (reduced from 120)
  
  // Use different sizing for charts vs images
  let contentWidth = maxWidth
  let contentHeight = maxWidth / (4/3) // 4:3 aspect ratio default
  
  if (type === 'chart') {
    // Scale from original size with a factor of 1.3-1.5x for better readability
    const baseWidth = originalWidth || 300
    const baseHeight = originalHeight || 220
    const scaleFactor = 1.3 // Reduced from 1.4 to 1.3 (30% larger)
    
    // Add extra height for card padding, title, and chart margins (~150px total)
    contentWidth = Math.min(baseWidth * scaleFactor, maxWidth)
    contentHeight = Math.min((baseHeight * scaleFactor) + 150, maxHeight)
  }
  
  // If dimensions exceed screen limits, scale down proportionally
  if (contentWidth > maxWidth || contentHeight > maxHeight) {
    const widthRatio = maxWidth / contentWidth
    const heightRatio = maxHeight / contentHeight
    const minRatio = Math.min(widthRatio, heightRatio)
    
    contentWidth = contentWidth * minRatio
    contentHeight = contentHeight * minRatio
  }

  useEffect(() => {
    if (visible) {
      // Show modal and start entry animation
      setShowModal(true)
      setImageLoaded(false)
      setImageError(false)
      
      // Reset animation values
      scaleAnim.setValue(0.7)
      opacityAnim.setValue(0)
      backdropOpacity.setValue(0)
      
      // Entry animation
      Animated.parallel([
        Animated.timing(backdropOpacity, {
          toValue: 1,
          duration: 300,
          useNativeDriver: true,
        }),
        Animated.spring(scaleAnim, {
          toValue: 1,
          tension: 65,
          friction: 7,
          useNativeDriver: true,
        }),
        Animated.timing(opacityAnim, {
          toValue: 1,
          duration: 350,
          useNativeDriver: true,
        }),
      ]).start()
    } else if (showModal) {
      // Start exit animation
      Animated.parallel([
        Animated.timing(backdropOpacity, {
          toValue: 0,
          duration: 250,
          useNativeDriver: true,
        }),
        Animated.timing(scaleAnim, {
          toValue: 0.7,
          duration: 200,
          useNativeDriver: true,
        }),
        Animated.timing(opacityAnim, {
          toValue: 0,
          duration: 200,
          useNativeDriver: true,
        }),
      ]).start()
      
      // Hide modal after animation
      setTimeout(() => {
        setShowModal(false)
      }, 250)
    }
  }, [visible])

  const handleBackdropPress = () => {
    onClose()
  }

  const handleImageLoad = () => {
    setImageLoaded(true)
  }

  const handleImageError = () => {
    setImageError(true)
  }

  if (!data || !type) return null

  const renderContent = () => {
    if (type === 'chart') {
      return (
        <ChartCard
          data={data}
          title={title || "Chart"}
          width={contentWidth}
          height={contentHeight}
        />
      )
    }

    // type === 'image'
    return (
      <>
        {/* Loading indicator */}
        {!imageLoaded && !imageError && (
          <View style={styles.loadingContainer}>
            <ActivityIndicator size="large" color="#FFFFFF" />
            <Text style={styles.loadingText}>Loading image...</Text>
          </View>
        )}

        {/* Error state */}
        {imageError && (
          <View style={styles.errorContainer}>
            <Text style={styles.errorText}>Failed to load image</Text>
          </View>
        )}

        {/* Main image */}
        <Image
          source={{ uri: data }}
          style={[styles.image, { width: contentWidth, height: contentHeight }]}
          resizeMode="cover"
          onLoad={handleImageLoad}
          onError={handleImageError}
        />
      </>
    )
  }

  return (
    <Modal
      visible={showModal}
      transparent
      animationType="none"
      statusBarTranslucent
      onRequestClose={onClose}
    >
      <StatusBar backgroundColor="rgba(0,0,0,0.9)" barStyle="light-content" />
      
      {/* Backdrop with blur effect */}
      <Animated.View 
        style={[
          styles.backdrop,
          { opacity: backdropOpacity }
        ]}
      >
        <BlurView intensity={20} style={StyleSheet.absoluteFill} />
        
        <TouchableOpacity
          style={styles.backdropTouchable}
          activeOpacity={1}
          onPress={handleBackdropPress}
        >
          <SafeAreaView style={styles.container}>
            {/* Close button */}
            <TouchableOpacity
              style={styles.closeButton}
              onPress={onClose}
              hitSlop={{ top: 20, bottom: 20, left: 20, right: 20 }}
            >
              <IconButton
                icon="close"
                iconColor="#FFFFFF"
                size={24}
                style={styles.closeIcon}
              />
            </TouchableOpacity>

            <TouchableOpacity
              style={styles.contentContainer}
              activeOpacity={1}
              onPress={() => {}} // Prevent backdrop press when touching content
            >
              <Animated.View
                style={[
                  styles.contentWrapper,
                  {
                    transform: [{ scale: scaleAnim }],
                    opacity: opacityAnim,
                    width: contentWidth,
                    height: contentHeight,
                  },
                ]}
              >
                {renderContent()}
              </Animated.View>
            </TouchableOpacity>
          </SafeAreaView>
        </TouchableOpacity>
      </Animated.View>
    </Modal>
  )
}

const styles = StyleSheet.create({
  backdrop: {
    flex: 1,
    backgroundColor: 'rgba(0, 0, 0, 0.9)',
  },
  backdropTouchable: {
    flex: 1,
  },
  container: {
    flex: 1,
    justifyContent: 'center',
    alignItems: 'center',
    paddingHorizontal: 10,
    paddingVertical: 10,
  },
  contentContainer: {
    justifyContent: 'center',
    alignItems: 'center',
  },
  contentWrapper: {
    borderRadius: 16,
    backgroundColor: 'rgba(255, 255, 255, 0.1)',
    shadowColor: '#000',
    shadowOffset: { width: 0, height: 10 },
    shadowOpacity: 0.3,
    shadowRadius: 20,
    elevation: 10,
    justifyContent: 'center',
    alignItems: 'center',
    overflow: 'hidden',
  },
  image: {
    borderRadius: 16,
  },
  loadingContainer: {
    position: 'absolute',
    justifyContent: 'center',
    alignItems: 'center',
    width: '100%',
    height: '100%',
    zIndex: 2,
  },
  loadingText: {
    color: '#FFFFFF',
    marginTop: 12,
    fontSize: 16,
    fontWeight: '500',
  },
  errorContainer: {
    position: 'absolute',
    justifyContent: 'center',
    alignItems: 'center',
    width: '100%',
    height: '100%',
    zIndex: 2,
  },
  errorText: {
    color: '#FFFFFF',
    fontSize: 16,
    fontWeight: '500',
    textAlign: 'center',
  },
  closeButton: {
    position: 'absolute',
    top: 20,
    right: 20,
    zIndex: 10,
  },
  closeIcon: {
    backgroundColor: 'rgba(255, 255, 255, 0.2)',
    borderRadius: 12,
  },
})

export default MediaModal 