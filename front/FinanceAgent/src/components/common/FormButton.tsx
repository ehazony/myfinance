import React, { useRef } from 'react'
import {
  TouchableOpacity,
  Animated,
  StyleSheet,
  View,
} from 'react-native'
import { Text, IconButton } from 'react-native-paper'
import { LinearGradient } from 'expo-linear-gradient'
import * as Haptics from 'expo-haptics'

interface FormButtonProps {
  title: string
  subtitle?: string
  icon?: string
  onPress: () => void
  disabled?: boolean
  gradient?: string[]
  style?: any
}

const FormButton: React.FC<FormButtonProps> = ({
  title,
  subtitle,
  icon = 'form-textbox',
  onPress,
  disabled = false,
  gradient = ['#3B82F6', '#1D4ED8'],
  style,
}) => {
  // Animation refs
  const scaleAnim = useRef(new Animated.Value(1)).current
  const glowAnim = useRef(new Animated.Value(0)).current
  const pulseAnim = useRef(new Animated.Value(1)).current

  // Pulse animation for attention
  React.useEffect(() => {
    const pulse = Animated.loop(
      Animated.sequence([
        Animated.timing(pulseAnim, {
          toValue: 1.05,
          duration: 2000,
          useNativeDriver: true,
        }),
        Animated.timing(pulseAnim, {
          toValue: 1,
          duration: 2000,
          useNativeDriver: true,
        }),
      ])
    )
    pulse.start()

    return () => pulse.stop()
  }, [])

  const handlePressIn = () => {
    Haptics.impactAsync(Haptics.ImpactFeedbackStyle.Light)
    
    Animated.parallel([
      Animated.spring(scaleAnim, {
        toValue: 0.96,
        tension: 300,
        friction: 10,
        useNativeDriver: true,
      }),
      Animated.timing(glowAnim, {
        toValue: 1,
        duration: 150,
        useNativeDriver: true,
      }),
    ]).start()
  }

  const handlePressOut = () => {
    Animated.parallel([
      Animated.spring(scaleAnim, {
        toValue: 1,
        tension: 300,
        friction: 10,
        useNativeDriver: true,
      }),
      Animated.timing(glowAnim, {
        toValue: 0,
        duration: 200,
        useNativeDriver: true,
      }),
    ]).start()
  }

  const handlePress = () => {
    if (!disabled) {
      Haptics.impactAsync(Haptics.ImpactFeedbackStyle.Medium)
      onPress()
    }
  }

  return (
    <Animated.View
      style={[
        styles.container,
        {
          transform: [
            { scale: scaleAnim },
            { scale: pulseAnim },
          ],
        },
        style,
      ]}
    >
      {/* Glow effect */}
      <Animated.View
        style={[
          styles.glowContainer,
          {
            opacity: glowAnim,
          },
        ]}
      >
        <LinearGradient
          colors={[...gradient, 'transparent']}
          style={styles.glow}
        />
      </Animated.View>

      {/* Main button */}
      <TouchableOpacity
        style={[styles.button, disabled && styles.disabled]}
        onPress={handlePress}
        onPressIn={handlePressIn}
        onPressOut={handlePressOut}
        activeOpacity={0.9}
        disabled={disabled}
      >
        <LinearGradient
          colors={disabled ? ['rgba(255,255,255,0.1)', 'rgba(255,255,255,0.05)'] : gradient}
          style={styles.gradient}
          start={{ x: 0, y: 0 }}
          end={{ x: 1, y: 1 }}
        >
          <View style={styles.content}>
            {/* Icon container */}
            <View style={styles.iconContainer}>
              <View style={styles.iconBackground}>
                <IconButton
                  icon={icon}
                  iconColor={disabled ? 'rgba(255,255,255,0.3)' : '#FFFFFF'}
                  size={24}
                  style={styles.icon}
                />
              </View>
            </View>

            {/* Text content */}
            <View style={styles.textContainer}>
              <Text style={[
                styles.title,
                disabled && styles.disabledText
              ]}>
                {title}
              </Text>
              
              {subtitle && (
                <Text style={[
                  styles.subtitle,
                  disabled && styles.disabledText
                ]}>
                  {subtitle}
                </Text>
              )}
            </View>

            {/* Arrow indicator */}
            <View style={styles.arrowContainer}>
              <IconButton
                icon="chevron-right"
                iconColor={disabled ? 'rgba(255,255,255,0.3)' : 'rgba(255,255,255,0.8)'}
                size={20}
                style={styles.arrow}
              />
            </View>
          </View>

          {/* Shine effect overlay */}
          <Animated.View
            style={[
              styles.shine,
              {
                opacity: glowAnim.interpolate({
                  inputRange: [0, 1],
                  outputRange: [0, 0.3],
                }),
              },
            ]}
          />
        </LinearGradient>
      </TouchableOpacity>
    </Animated.View>
  )
}

const styles = StyleSheet.create({
  container: {
    marginVertical: 8,
    marginHorizontal: 4,
  },
  glowContainer: {
    position: 'absolute',
    top: -8,
    left: -8,
    right: -8,
    bottom: -8,
    borderRadius: 24,
    zIndex: 0,
  },
  glow: {
    flex: 1,
    borderRadius: 24,
    opacity: 0.6,
  },
  button: {
    borderRadius: 16,
    overflow: 'hidden',
    elevation: 8,
    shadowColor: '#000',
    shadowOffset: { width: 0, height: 4 },
    shadowOpacity: 0.3,
    shadowRadius: 8,
    zIndex: 1,
  },
  disabled: {
    elevation: 2,
    shadowOpacity: 0.1,
  },
  gradient: {
    paddingVertical: 16,
    paddingHorizontal: 20,
    minHeight: 72,
  },
  content: {
    flexDirection: 'row',
    alignItems: 'center',
    justifyContent: 'space-between',
  },
  iconContainer: {
    marginRight: 16,
  },
  iconBackground: {
    width: 48,
    height: 48,
    borderRadius: 24,
    backgroundColor: 'rgba(255, 255, 255, 0.2)',
    justifyContent: 'center',
    alignItems: 'center',
    shadowColor: '#000',
    shadowOffset: { width: 0, height: 2 },
    shadowOpacity: 0.2,
    shadowRadius: 4,
    elevation: 4,
  },
  icon: {
    margin: 0,
  },
  textContainer: {
    flex: 1,
    marginRight: 12,
  },
  title: {
    fontSize: 16,
    fontWeight: '600',
    color: '#FFFFFF',
    marginBottom: 2,
    letterSpacing: 0.5,
  },
  subtitle: {
    fontSize: 13,
    color: 'rgba(255, 255, 255, 0.8)',
    fontWeight: '500',
    lineHeight: 18,
  },
  disabledText: {
    color: 'rgba(255, 255, 255, 0.4)',
  },
  arrowContainer: {
    opacity: 0.8,
  },
  arrow: {
    margin: 0,
  },
  shine: {
    position: 'absolute',
    top: 0,
    left: 0,
    right: 0,
    bottom: 0,
    backgroundColor: 'rgba(255, 255, 255, 0.2)',
    borderRadius: 16,
  },
})

export default FormButton 