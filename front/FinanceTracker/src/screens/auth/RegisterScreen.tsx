"use client"

import { useState } from "react"
import { View, StyleSheet, KeyboardAvoidingView, Platform, ScrollView } from "react-native"
import { Text, TextInput, useTheme, Snackbar } from "react-native-paper"
import { SafeAreaView } from "react-native-safe-area-context"
import { LinearGradient } from "expo-linear-gradient"
import { useAuth } from "../../context/AuthContext"
import CustomButton from "../../components/common/CustomButton"
import GradientCard from "../../components/common/GradientCard"

export default function RegisterScreen({ navigation }: any) {
  const [name, setName] = useState("")
  const [email, setEmail] = useState("")
  const [password, setPassword] = useState("")
  const [confirmPassword, setConfirmPassword] = useState("")
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState("")
  const [showPassword, setShowPassword] = useState(false)

  const { register } = useAuth()
  const theme = useTheme()

  const handleRegister = async () => {
    if (!name || !email || !password || !confirmPassword) {
      setError("Please fill in all fields")
      return
    }

    if (password !== confirmPassword) {
      setError("Passwords do not match")
      return
    }

    setLoading(true)
    try {
      await register(email, password, name)
    } catch (err) {
      setError("Registration failed")
    } finally {
      setLoading(false)
    }
  }

  return (
    <LinearGradient colors={[theme.colors.background, theme.colors.surface]} style={styles.container}>
      <SafeAreaView style={styles.safeArea}>
        <KeyboardAvoidingView behavior={Platform.OS === "ios" ? "padding" : "height"} style={styles.keyboardView}>
          <ScrollView contentContainerStyle={styles.scrollContent}>
            <View style={styles.header}>
              <Text variant="headlineLarge" style={[styles.title, { color: theme.colors.primary }]}>
                Create Account
              </Text>
              <Text variant="bodyLarge" style={[styles.subtitle, { color: theme.colors.onSurfaceVariant }]}>
                Join us to start tracking your finances
              </Text>
            </View>

            <GradientCard style={styles.formCard}>
              <View style={styles.form}>
                <TextInput
                  label="Full Name"
                  value={name}
                  onChangeText={setName}
                  mode="outlined"
                  style={styles.input}
                  theme={{ colors: { onSurfaceVariant: "#ffffff80" } }}
                />

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

                <TextInput
                  label="Password"
                  value={password}
                  onChangeText={setPassword}
                  mode="outlined"
                  secureTextEntry={!showPassword}
                  right={
                    <TextInput.Icon
                      icon={showPassword ? "eye-off" : "eye"}
                      onPress={() => setShowPassword(!showPassword)}
                    />
                  }
                  style={styles.input}
                  theme={{ colors: { onSurfaceVariant: "#ffffff80" } }}
                />

                <TextInput
                  label="Confirm Password"
                  value={confirmPassword}
                  onChangeText={setConfirmPassword}
                  mode="outlined"
                  secureTextEntry={!showPassword}
                  style={styles.input}
                  theme={{ colors: { onSurfaceVariant: "#ffffff80" } }}
                />

                <CustomButton
                  title="Create Account"
                  onPress={handleRegister}
                  loading={loading}
                  gradient
                  style={styles.registerButton}
                />
              </View>
            </GradientCard>

            <View style={styles.footer}>
              <Text style={[styles.footerText, { color: theme.colors.onSurfaceVariant }]}>
                Already have an account?{" "}
              </Text>
              <CustomButton title="Sign In" onPress={() => navigation.navigate("Login")} mode="text" />
            </View>
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
  registerButton: {
    marginTop: 8,
  },
  footer: {
    flexDirection: "row",
    justifyContent: "center",
    alignItems: "center",
  },
  footerText: {
    fontSize: 16,
  },
})
