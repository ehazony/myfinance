import React, { useEffect, useRef, useState } from 'react'
import {
  Modal,
  View,
  TouchableOpacity,
  Animated,
  Dimensions,
  StyleSheet,
  StatusBar,
  KeyboardAvoidingView,
  Platform,
  ScrollView,
  Keyboard,
} from 'react-native'
import { BlurView } from 'expo-blur'
import { Text, IconButton, Button, useTheme } from 'react-native-paper'
import { SafeAreaView } from 'react-native-safe-area-context'
import { LinearGradient } from 'expo-linear-gradient'
import * as Haptics from 'expo-haptics'
import FormField from './FormField'

const { width: screenWidth, height: screenHeight } = Dimensions.get('window')

interface FormField {
  id: string
  type: 'text' | 'number' | 'email' | 'dropdown' | 'multiselect' | 'date'
  label: string
  placeholder?: string
  required?: boolean
  options?: string[]
  value?: any
  validation?: {
    min?: number
    max?: number
    pattern?: string
    message?: string
  }
}

interface FormModalProps {
  visible: boolean
  title: string
  subtitle?: string
  fields: FormField[]
  onSubmit: (data: Record<string, any>) => void
  onClose: () => void
  submitText?: string
  showProgress?: boolean
  currentStep?: number
  totalSteps?: number
}

const FormModal: React.FC<FormModalProps> = ({
  visible,
  title,
  subtitle,
  fields,
  onSubmit,
  onClose,
  submitText = 'Submit',
  showProgress = false,
  currentStep = 1,
  totalSteps = 1,
}) => {
  const theme = useTheme()
  
  // Animation refs
  const slideAnim = useRef(new Animated.Value(screenHeight)).current
  const opacityAnim = useRef(new Animated.Value(0)).current
  const backdropOpacity = useRef(new Animated.Value(0)).current
  const scaleAnim = useRef(new Animated.Value(0.95)).current
  
  // State
  const [formData, setFormData] = useState<Record<string, any>>({})
  const [errors, setErrors] = useState<Record<string, string>>({})
  const [showModal, setShowModal] = useState(false)
  const [keyboardHeight, setKeyboardHeight] = useState(0)

  // Initialize form data
  useEffect(() => {
    const initialData: Record<string, any> = {}
    fields.forEach(field => {
      initialData[field.id] = field.value || ''
    })
    setFormData(initialData)
  }, [fields])

  // Keyboard handling
  useEffect(() => {
    const keyboardWillShow = Keyboard.addListener('keyboardWillShow', (e) => {
      setKeyboardHeight(e.endCoordinates.height)
    })
    const keyboardWillHide = Keyboard.addListener('keyboardWillHide', () => {
      setKeyboardHeight(0)
    })

    return () => {
      keyboardWillShow.remove()
      keyboardWillHide.remove()
    }
  }, [])

  // Modal animations
  useEffect(() => {
    if (visible) {
      setShowModal(true)
      Haptics.impactAsync(Haptics.ImpactFeedbackStyle.Light)
      
      // Entry animation sequence
      Animated.parallel([
        Animated.timing(backdropOpacity, {
          toValue: 1,
          duration: 400,
          useNativeDriver: true,
        }),
        Animated.spring(slideAnim, {
          toValue: 0,
          tension: 65,
          friction: 8,
          useNativeDriver: true,
        }),
        Animated.timing(scaleAnim, {
          toValue: 1,
          duration: 400,
          useNativeDriver: true,
        }),
        Animated.timing(opacityAnim, {
          toValue: 1,
          duration: 400,
          useNativeDriver: true,
        }),
      ]).start()
    } else if (showModal) {
      // Exit animation
      Animated.parallel([
        Animated.timing(backdropOpacity, {
          toValue: 0,
          duration: 300,
          useNativeDriver: true,
        }),
        Animated.spring(slideAnim, {
          toValue: screenHeight,
          tension: 85,
          friction: 8,
          useNativeDriver: true,
        }),
        Animated.timing(scaleAnim, {
          toValue: 0.95,
          duration: 300,
          useNativeDriver: true,
        }),
        Animated.timing(opacityAnim, {
          toValue: 0,
          duration: 300,
          useNativeDriver: true,
        }),
      ]).start(() => {
        setShowModal(false)
      })
    }
  }, [visible])

  const handleClose = () => {
    Haptics.impactAsync(Haptics.ImpactFeedbackStyle.Light)
    onClose()
  }

  const validateField = (field: FormField, value: any): string => {
    if (field.required && (!value || value.toString().trim() === '')) {
      return `${field.label} is required`
    }
    
    if (field.validation) {
      if (field.validation.min && parseFloat(value) < field.validation.min) {
        return `${field.label} must be at least ${field.validation.min}`
      }
      if (field.validation.max && parseFloat(value) > field.validation.max) {
        return `${field.label} must be at most ${field.validation.max}`
      }
      if (field.validation.pattern && !new RegExp(field.validation.pattern).test(value)) {
        return field.validation.message || `${field.label} format is invalid`
      }
    }
    
    return ''
  }

  const handleSubmit = () => {
    const newErrors: Record<string, string> = {}
    
    // Validate all fields
    fields.forEach(field => {
      const error = validateField(field, formData[field.id])
      if (error) {
        newErrors[field.id] = error
      }
    })
    
    setErrors(newErrors)
    
    if (Object.keys(newErrors).length === 0) {
      Haptics.impactAsync(Haptics.ImpactFeedbackStyle.Medium)
      onSubmit(formData)
    } else {
      Haptics.notificationAsync(Haptics.NotificationFeedbackType.Error)
    }
  }

  const updateField = (fieldId: string, value: any) => {
    setFormData(prev => ({ ...prev, [fieldId]: value }))
    
    // Clear error when user starts typing
    if (errors[fieldId]) {
      setErrors(prev => ({ ...prev, [fieldId]: '' }))
    }
  }

  const progress = showProgress ? currentStep / totalSteps : 0

  if (!showModal) return null

  return (
    <Modal
      visible={showModal}
      transparent
      animationType="none"
      statusBarTranslucent
      onRequestClose={handleClose}
    >
      <StatusBar backgroundColor="rgba(0,0,0,0.8)" barStyle="light-content" />
      
      {/* Backdrop with premium blur */}
      <Animated.View 
        style={[
          styles.backdrop,
          { opacity: backdropOpacity }
        ]}
      >
        <BlurView intensity={25} style={StyleSheet.absoluteFill} />
        
        <TouchableOpacity
          style={styles.backdropTouchable}
          activeOpacity={1}
          onPress={handleClose}
        >
          <KeyboardAvoidingView
            style={styles.container}
            behavior={Platform.OS === 'ios' ? 'padding' : 'height'}
            keyboardVerticalOffset={Platform.OS === 'ios' ? 0 : 20}
          >
            <SafeAreaView style={styles.safeArea}>
              <TouchableOpacity
                style={styles.contentContainer}
                activeOpacity={1}
                onPress={() => {}} // Prevent backdrop close when touching content
              >
                <Animated.View
                  style={[
                    styles.modalContent,
                    {
                      transform: [
                        { translateY: slideAnim },
                        { scale: scaleAnim }
                      ],
                      opacity: opacityAnim,
                      marginBottom: keyboardHeight * 0.3, // Smooth keyboard adaptation
                    },
                  ]}
                >
                  {/* Glass morphism container */}
                  <LinearGradient
                    colors={[
                      'rgba(255, 255, 255, 0.25)',
                      'rgba(255, 255, 255, 0.15)',
                    ]}
                    style={styles.glassContainer}
                  >
                    {/* Header */}
                    <View style={styles.header}>
                      <View style={styles.headerContent}>
                        <Text variant="headlineSmall" style={styles.title}>
                          {title}
                        </Text>
                        {subtitle && (
                          <Text variant="bodyMedium" style={styles.subtitle}>
                            {subtitle}
                          </Text>
                        )}
                      </View>
                      
                      <TouchableOpacity
                        style={styles.closeButton}
                        onPress={handleClose}
                        hitSlop={{ top: 20, bottom: 20, left: 20, right: 20 }}
                      >
                        <IconButton
                          icon="close"
                          iconColor="rgba(255, 255, 255, 0.8)"
                          size={24}
                          style={styles.closeIcon}
                        />
                      </TouchableOpacity>
                    </View>

                    {/* Progress indicator */}
                    {showProgress && (
                      <View style={styles.progressContainer}>
                        <View style={styles.progressTrack}>
                          <Animated.View
                            style={[
                              styles.progressFill,
                              { width: `${progress * 100}%` }
                            ]}
                          />
                        </View>
                        <Text style={styles.progressText}>
                          Step {currentStep} of {totalSteps}
                        </Text>
                      </View>
                    )}

                    {/* Form content */}
                    <ScrollView
                      style={styles.formContainer}
                      showsVerticalScrollIndicator={false}
                      keyboardShouldPersistTaps="handled"
                    >
                      {fields.map((field, index) => (
                        <FormField
                          key={field.id}
                          id={field.id}
                          type={field.type}
                          label={field.label}
                          placeholder={field.placeholder}
                          value={formData[field.id]}
                          onChange={(value) => updateField(field.id, value)}
                          error={errors[field.id]}
                          required={field.required}
                          options={field.options}
                          autoFocus={index === 0}
                        />
                      ))}
                    </ScrollView>

                    {/* Action buttons */}
                    <View style={styles.actionContainer}>
                      <TouchableOpacity
                        style={styles.submitButton}
                        onPress={handleSubmit}
                        activeOpacity={0.8}
                      >
                        <LinearGradient
                          colors={['#3B82F6', '#1D4ED8']}
                          style={styles.submitGradient}
                          start={{ x: 0, y: 0 }}
                          end={{ x: 1, y: 1 }}
                        >
                          <Text style={styles.submitText}>{submitText}</Text>
                        </LinearGradient>
                      </TouchableOpacity>
                    </View>
                  </LinearGradient>
                </Animated.View>
              </TouchableOpacity>
            </SafeAreaView>
          </KeyboardAvoidingView>
        </TouchableOpacity>
      </Animated.View>
    </Modal>
  )
}

const styles = StyleSheet.create({
  backdrop: {
    flex: 1,
    backgroundColor: 'rgba(0, 0, 0, 0.8)',
  },
  backdropTouchable: {
    flex: 1,
  },
  container: {
    flex: 1,
  },
  safeArea: {
    flex: 1,
  },
  contentContainer: {
    flex: 1,
    justifyContent: 'flex-end',
  },
  modalContent: {
    maxHeight: screenHeight * 0.85,
    marginHorizontal: 16,
    marginBottom: 16,
  },
  glassContainer: {
    borderRadius: 24,
    borderWidth: 1,
    borderColor: 'rgba(255, 255, 255, 0.2)',
    shadowColor: '#000',
    shadowOffset: { width: 0, height: 20 },
    shadowOpacity: 0.3,
    shadowRadius: 30,
    elevation: 20,
    overflow: 'hidden',
  },
  header: {
    flexDirection: 'row',
    alignItems: 'flex-start',
    justifyContent: 'space-between',
    padding: 24,
    paddingBottom: 16,
  },
  headerContent: {
    flex: 1,
    marginRight: 16,
  },
  title: {
    color: '#FFFFFF',
    fontWeight: '700',
    marginBottom: 4,
  },
  subtitle: {
    color: 'rgba(255, 255, 255, 0.8)',
    lineHeight: 20,
  },
  closeButton: {
    marginTop: -8,
  },
  closeIcon: {
    backgroundColor: 'rgba(255, 255, 255, 0.1)',
    borderRadius: 12,
  },
  progressContainer: {
    paddingHorizontal: 24,
    paddingBottom: 20,
  },
  progressTrack: {
    height: 4,
    backgroundColor: 'rgba(255, 255, 255, 0.2)',
    borderRadius: 2,
    overflow: 'hidden',
  },
  progressFill: {
    height: '100%',
    backgroundColor: '#3B82F6',
    borderRadius: 2,
  },
  progressText: {
    color: 'rgba(255, 255, 255, 0.8)',
    fontSize: 12,
    textAlign: 'center',
    marginTop: 8,
    fontWeight: '500',
  },
  formContainer: {
    maxHeight: screenHeight * 0.4,
    paddingHorizontal: 24,
  },
  placeholder: {
    color: 'rgba(255, 255, 255, 0.8)',
    textAlign: 'center',
    fontSize: 16,
    fontWeight: '500',
    padding: 40,
  },
  actionContainer: {
    padding: 24,
    paddingTop: 20,
  },
  submitButton: {
    borderRadius: 16,
    overflow: 'hidden',
  },
  submitGradient: {
    paddingVertical: 16,
    paddingHorizontal: 32,
    alignItems: 'center',
  },
  submitText: {
    color: '#FFFFFF',
    fontSize: 16,
    fontWeight: '600',
    letterSpacing: 0.5,
  },
})

export default FormModal 