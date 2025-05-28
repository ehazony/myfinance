"use client"

import { useState } from "react"
import { View, StyleSheet, KeyboardAvoidingView, Platform, ScrollView } from "react-native"
import { Text, TextInput, useTheme, Snackbar } from "react-native-paper"
import { SafeAreaView } from "react-native-safe-area-context"
import { LinearGradient } from "expo-linear-gradient"
import CustomButton from "../../components/common/CustomButton"
import GradientCard from "../../components/common/GradientCard"

export default function ForgotPasswordScreen({ navigation }: any) {
  const [email, setEmail] = useState("")
  const [loading, setLoading] = useState(false)
  const [success, setSuccess] = useState(false)
  const [error, setError] = useState("")

  const theme = useTheme()

  const handleResetPassword = async () => {
    if (!email) {
      setError("Please enter your email address")
      return
    }

    setLoading(true)
    try {
      // Simulate API call
      await new Promise((resolve) => setTimeout(resolve, 1000))
      setSuccess(true)
    } catch (err) {
      setError("Failed to send reset email")
    } finally {
      setLoading(false)
    }
  }

  if (success) {
    return (
      <LinearGradient colors={[theme.colors.background, theme.colors.surface]} style={styles.container}>
        <SafeAreaView style={styles.safeArea}>
          <View style={styles.successContainer}>
            <GradientCard style={styles.successCard}>
              <Text variant="headlineSmall" style={styles.successTitle}>
                Check Your Email
              </Text>
              <Text variant="bodyLarge" style={styles.successText}>
                We've sent a password reset link to {email}
              </Text>
              <CustomButton
                title="Back to Login"
                onPress={() => navigation.navigate("Login")}
                gradient
                style={styles.backButton}
              />
            </GradientCard>
          </View>
        </SafeAreaView>
      </LinearGradient>
    )
  }

  return (
    <LinearGradient colors={[theme.colors.background, theme.colors.surface]} style={styles.container}>
      <SafeAreaView style={styles.safeArea}>
        <KeyboardAvoidingView behavior={Platform.OS === "ios" ? "padding" : "height"} style={styles.keyboardView}>
          <ScrollView contentContainerStyle={styles.scrollContent}>
            <View style={styles.header}>
              <Text variant="headlineLarge" style={[styles.title, { color: theme.colors.primary }]}>
                Reset Password
              </Text>
              <Text variant="bodyLarge" style={[styles.subtitle, { color: theme.colors.onSurfaceVariant }]}>
                Enter your email to receive a reset link
              </Text>
            </View>

            <GradientCard style={styles.formCard}>
              <View style={styles.form}>
                <TextInput
                  label="Email"
                  value={email}
                  onChangeText={setEmail}
                  mode="outlined"
                  keyboardType="email-address"
                  autoCapitalize="none"
                  style={styles.input}
                  theme={{ colors: { onSurfaceVariant: "#ffffff80" } }}
                />

                <CustomButton
                  title="Send Reset Link"
                  onPress={handleResetPassword}
                  loading={loading}
                  gradient
                  style={styles.resetButton}
                />

                <CustomButton
                  title="Back to Login"
                  onPress={() => navigation.navigate("Login")}
                  mode="text"
                  style={styles.backToLoginButton}
                />
              </View>
            </GradientCard>
          </ScrollView>
        </KeyboardAvoidingView>

        <Snackbar visible={!!error} onDismiss={() => setError("")} duration={3000}>
          {error}
        </Snackbar>
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
  scrollContent: {
    flexGrow: 1,
    padding: 24,
    justifyContent: "center",
  },
  header: {
    alignItems: "center",
    marginBottom: 32,
  },
  title: {
    fontWeight: "bold",
    marginBottom: 8,
  },
  subtitle: {
    textAlign: "center",
  },
  formCard: {
    marginBottom: 24,
  },
  form: {
    gap: 16,
  },
  input: {
    backgroundColor: "rgba(255, 255, 255, 0.1)",
  },
  resetButton: {
    marginTop: 8,
  },
  backToLoginButton: {
    alignSelf: "center",
  },
  successContainer: {
    flex: 1,
    justifyContent: "center",
    padding: 24,
  },
  successCard: {
    alignItems: "center",
  },
  successTitle: {
    color: "#ffffff",
    fontWeight: "bold",
    marginBottom: 16,
    textAlign: "center",
  },
  successText: {
    color: "#ffffff",
    textAlign: "center",
    marginBottom: 24,
  },
  backButton: {
    width: "100%",
  },
})
