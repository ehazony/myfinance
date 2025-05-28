import { StyleSheet } from "react-native"
import { Button } from "react-native-paper"
import { LinearGradient } from "expo-linear-gradient"

interface CustomButtonProps {
  title: string
  onPress: () => void
  mode?: "contained" | "outlined" | "text"
  loading?: boolean
  disabled?: boolean
  gradient?: boolean
  style?: any
}

export default function CustomButton({
  title,
  onPress,
  mode = "contained",
  loading = false,
  disabled = false,
  gradient = false,
  style,
}: CustomButtonProps) {
  if (gradient && mode === "contained") {
    return (
      <LinearGradient
        colors={["#2753a7", "#9bcada"]}
        start={{ x: 0, y: 0 }}
        end={{ x: 1, y: 0 }}
        style={[styles.gradientButton, style]}
      >
        <Button
          mode="text"
          onPress={onPress}
          loading={loading}
          disabled={disabled}
          labelStyle={styles.gradientButtonText}
          style={styles.transparentButton}
        >
          {title}
        </Button>
      </LinearGradient>
    )
  }

  return (
    <Button
      mode={mode}
      onPress={onPress}
      loading={loading}
      disabled={disabled}
      style={[styles.button, style]}
      contentStyle={styles.buttonContent}
    >
      {title}
    </Button>
  )
}

const styles = StyleSheet.create({
  button: {
    borderRadius: 12,
  },
  buttonContent: {
    paddingVertical: 8,
  },
  gradientButton: {
    borderRadius: 12,
    elevation: 4,
    shadowColor: "#000",
    shadowOffset: { width: 0, height: 2 },
    shadowOpacity: 0.25,
    shadowRadius: 4,
  },
  transparentButton: {
    backgroundColor: "transparent",
    margin: 0,
  },
  gradientButtonText: {
    color: "#ffffff",
    fontWeight: "bold",
  },
})
