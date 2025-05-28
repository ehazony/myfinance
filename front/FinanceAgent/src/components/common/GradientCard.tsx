import type React from "react"
import { StyleSheet, View } from "react-native"
import { Card } from "react-native-paper"
import { LinearGradient } from "expo-linear-gradient"

interface GradientCardProps {
  children: React.ReactNode
  colors?: string[]
  style?: any
}

export default function GradientCard({ children, colors = ["#2753a7", "#9bcada"], style }: GradientCardProps) {
  return (
    <Card style={[styles.card, style]} elevation={4}>
      <View style={styles.contentWrapper}>
        <LinearGradient colors={colors} start={{ x: 0, y: 0 }} end={{ x: 1, y: 1 }} style={styles.gradient}>
          {children}
        </LinearGradient>
      </View>
    </Card>
  )
}

const styles = StyleSheet.create({
  card: {
    borderRadius: 16,
  },
  contentWrapper: {
    borderRadius: 16,
    overflow: "hidden",
  },
  gradient: {
    padding: 20,
    borderRadius: 16,
  },
})
