import React, { useEffect, useRef, useState } from 'react'
import {
  View,
  TextInput,
  TouchableOpacity,
  Animated,
  StyleSheet,
  Platform,
} from 'react-native'
import { Text, useTheme, IconButton } from 'react-native-paper'
import { LinearGradient } from 'expo-linear-gradient'
import * as Haptics from 'expo-haptics'

interface FormFieldProps {
  id: string
  type: 'text' | 'number' | 'email' | 'dropdown' | 'multiselect' | 'date'
  label: string
  placeholder?: string
  value: any
  onChange: (value: any) => void
  error?: string
  required?: boolean
  options?: string[]
  icon?: string
  autoFocus?: boolean
}

const FormField: React.FC<FormFieldProps> = ({
  id,
  type,
  label,
  placeholder,
  value,
  onChange,
  error,
  required,
  options,
  icon,
  autoFocus = false,
}) => {
  const theme = useTheme()
  
  // Animation refs
  const labelAnim = useRef(new Animated.Value(value ? 1 : 0)).current
  const focusAnim = useRef(new Animated.Value(0)).current
  const errorAnim = useRef(new Animated.Value(0)).current
  const shakeAnim = useRef(new Animated.Value(0)).current
  
  // State
  const [isFocused, setIsFocused] = useState(false)
  const [isDropdownOpen, setIsDropdownOpen] = useState(false)
  const [secureText, setSecureText] = useState(type === 'password')
  
  // Input ref
  const inputRef = useRef<TextInput>(null)

  // Handle focus animations
  useEffect(() => {
    Animated.parallel([
      Animated.spring(labelAnim, {
        toValue: isFocused || value ? 1 : 0,
        tension: 120,
        friction: 8,
        useNativeDriver: false,
      }),
      Animated.timing(focusAnim, {
        toValue: isFocused ? 1 : 0,
        duration: 300,
        useNativeDriver: false,
      }),
    ]).start()
  }, [isFocused, value])

  // Handle error animations
  useEffect(() => {
    if (error) {
      // Shake animation for errors
      Animated.sequence([
        Animated.timing(shakeAnim, {
          toValue: 1,
          duration: 100,
          useNativeDriver: true,
        }),
        Animated.timing(shakeAnim, {
          toValue: -1,
          duration: 100,
          useNativeDriver: true,
        }),
        Animated.timing(shakeAnim, {
          toValue: 1,
          duration: 100,
          useNativeDriver: true,
        }),
        Animated.timing(shakeAnim, {
          toValue: 0,
          duration: 100,
          useNativeDriver: true,
        }),
      ]).start()

      // Error slide down
      Animated.timing(errorAnim, {
        toValue: 1,
        duration: 300,
        useNativeDriver: false,
      }).start()

      Haptics.notificationAsync(Haptics.NotificationFeedbackType.Error)
    } else {
      Animated.timing(errorAnim, {
        toValue: 0,
        duration: 200,
        useNativeDriver: false,
      }).start()
    }
  }, [error])

  const handleFocus = () => {
    setIsFocused(true)
    Haptics.impactAsync(Haptics.ImpactFeedbackStyle.Light)
  }

  const handleBlur = () => {
    setIsFocused(false)
  }

  const handleChangeText = (text: string) => {
    onChange(text)
    Haptics.selectionAsync()
  }

  const handleDropdownSelect = (option: string) => {
    onChange(option)
    setIsDropdownOpen(false)
    Haptics.impactAsync(Haptics.ImpactFeedbackStyle.Light)
  }

  const toggleSecureText = () => {
    setSecureText(!secureText)
    Haptics.impactAsync(Haptics.ImpactFeedbackStyle.Light)
  }

  // Animated label position
  const labelStyle = {
    top: labelAnim.interpolate({
      inputRange: [0, 1],
      outputRange: [20, 4],
    }),
    fontSize: labelAnim.interpolate({
      inputRange: [0, 1],
      outputRange: [16, 12],
    }),
    color: labelAnim.interpolate({
      inputRange: [0, 1],
      outputRange: ['rgba(255, 255, 255, 0.6)', '#3B82F6'],
    }),
  }

  // Border color animation
  const borderColor = focusAnim.interpolate({
    inputRange: [0, 1],
    outputRange: ['rgba(255, 255, 255, 0.2)', '#3B82F6'],
  })

  // Container shake transform
  const shakeTransform = {
    transform: [
      {
        translateX: shakeAnim.interpolate({
          inputRange: [-1, -0.5, 0, 0.5, 1],
          outputRange: [-10, -5, 0, 5, 10],
        }),
      },
    ],
  }

  const getKeyboardType = () => {
    switch (type) {
      case 'number':
        return 'numeric'
      case 'email':
        return 'email-address'
      default:
        return 'default'
    }
  }

  const renderTextInput = () => (
    <View style={styles.inputContainer}>
      {/* Animated label */}
      <Animated.Text style={[styles.label, labelStyle]}>
        {label}
        {required && <Text style={styles.required}> *</Text>}
      </Animated.Text>
      
      {/* Input with animated border */}
      <Animated.View
        style={[
          styles.inputWrapper,
          { borderColor },
          error && styles.inputError,
        ]}
      >
        {/* Icon */}
        {icon && (
          <View style={styles.iconContainer}>
            <IconButton
              icon={icon}
              iconColor="rgba(255, 255, 255, 0.6)"
              size={20}
              style={styles.icon}
            />
          </View>
        )}
        
        {/* Text Input */}
        <TextInput
          ref={inputRef}
          style={[
            styles.input,
            icon && styles.inputWithIcon,
          ]}
          value={value?.toString() || ''}
          onChangeText={handleChangeText}
          onFocus={handleFocus}
          onBlur={handleBlur}
          placeholder={isFocused ? placeholder : ''}
          placeholderTextColor="rgba(255, 255, 255, 0.4)"
          keyboardType={getKeyboardType()}
          secureTextEntry={secureText}
          autoFocus={autoFocus}
          autoCorrect={false}
          autoCapitalize={type === 'email' ? 'none' : 'sentences'}
        />
        
        {/* Password toggle */}
        {type === 'password' && (
          <TouchableOpacity
            style={styles.passwordToggle}
            onPress={toggleSecureText}
            hitSlop={{ top: 10, bottom: 10, left: 10, right: 10 }}
          >
            <IconButton
              icon={secureText ? 'eye-off' : 'eye'}
              iconColor="rgba(255, 255, 255, 0.6)"
              size={20}
            />
          </TouchableOpacity>
        )}
      </Animated.View>
    </View>
  )

  const renderDropdown = () => (
    <View style={styles.inputContainer}>
      {/* Animated label */}
      <Animated.Text style={[styles.label, labelStyle]}>
        {label}
        {required && <Text style={styles.required}> *</Text>}
      </Animated.Text>
      
      {/* Dropdown button */}
      <TouchableOpacity
        style={[
          styles.dropdownButton,
          isFocused && styles.dropdownFocused,
          error && styles.inputError,
        ]}
        onPress={() => {
          setIsDropdownOpen(!isDropdownOpen)
          setIsFocused(!isDropdownOpen)
          Haptics.impactAsync(Haptics.ImpactFeedbackStyle.Light)
        }}
      >
        <Text style={[
          styles.dropdownText,
          !value && styles.dropdownPlaceholder
        ]}>
          {value || placeholder || `Select ${label.toLowerCase()}...`}
        </Text>
        
        <Animated.View
          style={[
            styles.dropdownArrow,
            {
              transform: [{
                rotate: focusAnim.interpolate({
                  inputRange: [0, 1],
                  outputRange: ['0deg', '180deg'],
                })
              }]
            }
          ]}
        >
          <IconButton
            icon="chevron-down"
            iconColor="rgba(255, 255, 255, 0.6)"
            size={20}
          />
        </Animated.View>
      </TouchableOpacity>
      
      {/* Dropdown options */}
      {isDropdownOpen && (
        <Animated.View
          style={[
            styles.dropdownOptions,
            {
              opacity: focusAnim,
              transform: [{
                scaleY: focusAnim,
              }]
            }
          ]}
        >
          {options?.map((option, index) => (
            <TouchableOpacity
              key={index}
              style={[
                styles.dropdownOption,
                value === option && styles.dropdownOptionSelected
              ]}
              onPress={() => handleDropdownSelect(option)}
            >
              <Text style={[
                styles.dropdownOptionText,
                value === option && styles.dropdownOptionTextSelected
              ]}>
                {option}
              </Text>
              
              {value === option && (
                <IconButton
                  icon="check"
                  iconColor="#3B82F6"
                  size={16}
                />
              )}
            </TouchableOpacity>
          ))}
        </Animated.View>
      )}
    </View>
  )

  return (
    <Animated.View style={[styles.container, shakeTransform]}>
      {type === 'dropdown' || type === 'multiselect' ? renderDropdown() : renderTextInput()}
      
      {/* Error message */}
      <Animated.View
        style={[
          styles.errorContainer,
          {
            opacity: errorAnim,
            height: errorAnim.interpolate({
              inputRange: [0, 1],
              outputRange: [0, 24],
            }),
          }
        ]}
      >
        <Text style={styles.errorText}>{error}</Text>
      </Animated.View>
    </Animated.View>
  )
}

const styles = StyleSheet.create({
  container: {
    marginBottom: 16,
  },
  inputContainer: {
    position: 'relative',
  },
  label: {
    position: 'absolute',
    left: 16,
    fontWeight: '500',
    zIndex: 1,
    backgroundColor: 'transparent',
  },
  required: {
    color: '#EF4444',
  },
  inputWrapper: {
    flexDirection: 'row',
    alignItems: 'center',
    borderWidth: 2,
    borderRadius: 16,
    backgroundColor: 'rgba(255, 255, 255, 0.1)',
    minHeight: 56,
  },
  inputError: {
    borderColor: '#EF4444',
  },
  iconContainer: {
    paddingLeft: 8,
  },
  icon: {
    margin: 0,
  },
  input: {
    flex: 1,
    paddingHorizontal: 16,
    paddingTop: 20,
    paddingBottom: 8,
    fontSize: 16,
    color: '#FFFFFF',
    fontWeight: '500',
  },
  inputWithIcon: {
    paddingLeft: 8,
  },
  passwordToggle: {
    paddingRight: 8,
  },
  dropdownButton: {
    flexDirection: 'row',
    alignItems: 'center',
    justifyContent: 'space-between',
    borderWidth: 2,
    borderColor: 'rgba(255, 255, 255, 0.2)',
    borderRadius: 16,
    backgroundColor: 'rgba(255, 255, 255, 0.1)',
    minHeight: 56,
    paddingHorizontal: 16,
    paddingTop: 20,
    paddingBottom: 8,
  },
  dropdownFocused: {
    borderColor: '#3B82F6',
  },
  dropdownText: {
    fontSize: 16,
    color: '#FFFFFF',
    fontWeight: '500',
    flex: 1,
  },
  dropdownPlaceholder: {
    color: 'rgba(255, 255, 255, 0.6)',
  },
  dropdownArrow: {
    marginLeft: 8,
  },
  dropdownOptions: {
    marginTop: 4,
    borderRadius: 16,
    backgroundColor: 'rgba(255, 255, 255, 0.15)',
    borderWidth: 1,
    borderColor: 'rgba(255, 255, 255, 0.2)',
    overflow: 'hidden',
    transformOrigin: 'top',
  },
  dropdownOption: {
    flexDirection: 'row',
    alignItems: 'center',
    justifyContent: 'space-between',
    paddingHorizontal: 16,
    paddingVertical: 12,
    borderBottomWidth: 1,
    borderBottomColor: 'rgba(255, 255, 255, 0.1)',
  },
  dropdownOptionSelected: {
    backgroundColor: 'rgba(59, 130, 246, 0.2)',
  },
  dropdownOptionText: {
    fontSize: 16,
    color: '#FFFFFF',
    fontWeight: '500',
    flex: 1,
  },
  dropdownOptionTextSelected: {
    color: '#3B82F6',
    fontWeight: '600',
  },
  errorContainer: {
    overflow: 'hidden',
    paddingHorizontal: 16,
  },
  errorText: {
    color: '#EF4444',
    fontSize: 12,
    fontWeight: '500',
    marginTop: 4,
  },
})

export default FormField 