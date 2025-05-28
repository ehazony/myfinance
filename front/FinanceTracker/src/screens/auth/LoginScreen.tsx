"use client"

import { useState, useEffect } from "react"
import { View, StyleSheet, KeyboardAvoidingView, Platform, ScrollView } from "react-native"
import { Text, TextInput, useTheme, Snackbar, IconButton } from "react-native-paper"
import { SafeAreaView } from "react-native-safe-area-context"
import { useAuth } from "../../context/AuthContext"
import CustomButton from "../../components/common/CustomButton"

export default function LoginScreen({ navigation }: any) {
  const [email, setEmail] = useState("")
  const [password, setPassword] = useState("")
  const [showPassword, setShowPassword] = useState(false)

  const { login, isLoading, error, clearError } = useAuth()
  const theme = useTheme()

  // Clear error when component unmounts or when user starts typing
  useEffect(() => {
    return () => {
      clearError()
    }
  }, [clearError])

  useEffect(() => {
    if (email || password) {
      clearError()
    }
  }, [email, password, clearError])

  const handleLogin = async () => {
    if (!email || !password) {
      // We could set a local error here, but let's use a simple alert for validation
      return
    }
    await login(email, password)
    // Any error will be handled and shown by the AuthContext
  }

  const isFormValid = email.trim() && password.trim()

  return (
    <View style={styles.container}>
      <SafeAreaView style={styles.safeArea}>
        <KeyboardAvoidingView behavior={Platform.OS === "ios" ? "padding" : "height"} style={styles.keyboardView}>
          <ScrollView contentContainerStyle={styles.scrollContent} showsVerticalScrollIndicator={false}>
            
            {/* Main Card */}
            <View style={styles.card}>
              {/* Header */}
              <View style={styles.header}>
                <Text style={styles.welcomeTitle}>Welcome Back</Text>
                <Text style={styles.welcomeSubtitle}>Sign in to continue to your account</Text>
              </View>

              {/* Form */}
              <View style={styles.form}>
                {/* Email Field */}
                <View style={styles.inputGroup}>
                  <Text style={styles.inputLabel}>Email</Text>
                  <TextInput
                    value={email}
                    onChangeText={setEmail}
                    mode="outlined"
                    keyboardType="email-address"
                    autoCapitalize="none"
                    placeholder="your@email.com"
                    style={styles.input}
                    outlineStyle={styles.inputOutline}
                    disabled={isLoading}
                    theme={{
                      colors: {
                        onSurfaceVariant: "#9bcada",
                        outline: "#d2cdce",
                        primary: "#2753a7",
                      },
                    }}
                    textColor="#272a2d"
                    placeholderTextColor="#9bcada"
                  />
                </View>

                {/* Password Field */}
                <View style={styles.inputGroup}>
                  <Text style={styles.inputLabel}>Password</Text>
                  <TextInput
                    value={password}
                    onChangeText={setPassword}
                    mode="outlined"
                    secureTextEntry={!showPassword}
                    placeholder="••••••••"
                    style={styles.input}
                    outlineStyle={styles.inputOutline}
                    disabled={isLoading}
                    theme={{
                      colors: {
                        onSurfaceVariant: "#9bcada",
                        outline: "#d2cdce",
                        primary: "#2753a7",
                      },
                    }}
                    textColor="#272a2d"
                    placeholderTextColor="#9bcada"
                    right={
                      <TextInput.Icon
                        icon={showPassword ? "eye-off-outline" : "eye-outline"}
                        color="#9bcada"
                        onPress={() => setShowPassword(!showPassword)}
                        disabled={isLoading}
                      />
                    }
                  />
                </View>

                {/* Error Message */}
                {error && (
                  <View style={styles.errorContainer}>
                    <Text style={styles.errorText}>{error}</Text>
                  </View>
                )}

                {/* Forgot Password Link */}
                <View style={styles.forgotContainer}>
                  <CustomButton
                    title="Forgot Password?"
                    onPress={() => navigation.navigate("ForgotPassword")}
                    mode="text"
                    style={styles.forgotButton}
                    disabled={isLoading}
                  />
                </View>

                {/* Sign In Button */}
                <CustomButton
                  title={isLoading ? "Signing In..." : "Sign In"}
                  onPress={handleLogin}
                  loading={isLoading}
                  disabled={!isFormValid || isLoading}
                  gradient={true}
                  style={styles.signInButton}
                />
              </View>

              {/* Divider */}
              <View style={styles.dividerContainer}>
                <View style={styles.dividerLine} />
                <Text style={styles.dividerText}>or continue with</Text>
                <View style={styles.dividerLine} />
              </View>

              {/* Social Login */}
              <View style={styles.socialContainer}>
                <View style={styles.socialButton}>
                  <IconButton 
                    icon="google" 
                    iconColor="#272a2d" 
                    size={24}
                  />
                </View>
                <View style={styles.socialButton}>
                  <IconButton 
                    icon="facebook" 
                    iconColor="#272a2d" 
                    size={24}
                  />
                </View>
                <View style={styles.socialButton}>
                  <IconButton 
                    icon="twitter" 
                    iconColor="#272a2d" 
                    size={24}
                  />
                </View>
              </View>

              {/* Sign Up Link */}
              <View style={styles.signupContainer}>
                <Text style={styles.signupText}>Don't have an account? </Text>
                <CustomButton
                  title="Sign Up"
                  onPress={() => navigation.navigate("Register")}
                  mode="text"
                  style={styles.signupButton}
                />
              </View>
            </View>

          </ScrollView>
        </KeyboardAvoidingView>

        <Snackbar visible={!!error} onDismiss={clearError} duration={3000} style={styles.snackbar}>
          {error}
        </Snackbar>
      </SafeAreaView>
    </View>
  )
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: "#f8f9fa",
  },
  safeArea: {
    flex: 1,
  },
  keyboardView: {
    flex: 1,
  },
  scrollContent: {
    flexGrow: 1,
    justifyContent: "center",
    paddingHorizontal: 24,
    paddingVertical: 40,
  },
  card: {
    backgroundColor: "#ffffff",
    borderRadius: 16,
    padding: 32,
    shadowColor: "#272a2d",
    shadowOffset: { width: 0, height: 4 },
    shadowOpacity: 0.1,
    shadowRadius: 12,
    elevation: 6,
    borderWidth: 1,
    borderColor: "#f0f0f0",
  },
  header: {
    alignItems: "center",
    marginBottom: 32,
  },
  welcomeTitle: {
    fontSize: 28,
    fontWeight: "700",
    color: "#272a2d",
    marginBottom: 8,
    textAlign: "center",
  },
  welcomeSubtitle: {
    fontSize: 16,
    color: "#9bcada",
    textAlign: "center",
    fontWeight: "400",
  },
  form: {
    gap: 20,
    marginBottom: 32,
  },
  inputGroup: {
    gap: 8,
  },
  inputLabel: {
    fontSize: 14,
    fontWeight: "600",
    color: "#272a2d",
    marginLeft: 4,
  },
  input: {
    backgroundColor: "#ffffff",
    fontSize: 16,
  },
  inputOutline: {
    borderRadius: 8,
    borderWidth: 1,
  },
  errorContainer: {
    backgroundColor: "rgba(231, 76, 60, 0.1)",
    padding: 12,
    borderRadius: 8,
    borderLeftWidth: 4,
    borderLeftColor: "#e74c3c",
  },
  errorText: {
    color: "#e74c3c",
    fontSize: 14,
    fontWeight: "500",
  },
  forgotContainer: {
    alignItems: "flex-end",
    marginTop: -8,
  },
  forgotButton: {
    paddingVertical: 4,
  },
  signInButton: {
    paddingVertical: 8,
    marginTop: 8,
  },
  dividerContainer: {
    flexDirection: "row",
    alignItems: "center",
    marginBottom: 24,
  },
  dividerLine: {
    flex: 1,
    height: 1,
    backgroundColor: "#d2cdce",
  },
  dividerText: {
    color: "#9bcada",
    fontSize: 14,
    fontWeight: "500",
    marginHorizontal: 16,
  },
  socialContainer: {
    flexDirection: "row",
    justifyContent: "center",
    gap: 16,
    marginBottom: 32,
  },
  socialButton: {
    width: 48,
    height: 48,
    borderRadius: 24,
    backgroundColor: "#ffffff",
    justifyContent: "center",
    alignItems: "center",
    borderWidth: 1,
    borderColor: "#d2cdce",
    shadowColor: "#272a2d",
    shadowOffset: { width: 0, height: 2 },
    shadowOpacity: 0.05,
    shadowRadius: 4,
    elevation: 2,
  },
  signupContainer: {
    flexDirection: "row",
    justifyContent: "center",
    alignItems: "center",
  },
  signupText: {
    color: "#9bcada",
    fontSize: 16,
    fontWeight: "400",
  },
  signupButton: {
    marginLeft: -8,
  },
  snackbar: {
    backgroundColor: "#e74c3c",
  },
})
