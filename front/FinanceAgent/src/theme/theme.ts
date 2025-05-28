import { MD3LightTheme, MD3DarkTheme } from "react-native-paper"

const colors = {
  primary: "#2753a7",
  secondary: "#9bcada",
  tertiary: "#d2cdce",
  surface: "#272a2d",
  background: "#f8f9fa",
  darkBackground: "#1a1d20",
}

export const lightTheme = {
  ...MD3LightTheme,
  colors: {
    ...MD3LightTheme.colors,
    primary: colors.primary,
    secondary: colors.secondary,
    tertiary: colors.tertiary,
    surface: "#ffffff",
    surfaceVariant: colors.tertiary,
    background: colors.background,
    onBackground: colors.surface,
    onSurface: colors.surface,
    outline: "#e0e0e0",
  },
}

export const darkTheme = {
  ...MD3DarkTheme,
  colors: {
    ...MD3DarkTheme.colors,
    primary: colors.secondary,
    secondary: colors.primary,
    tertiary: colors.tertiary,
    surface: colors.surface,
    surfaceVariant: "#3a3d40",
    background: colors.darkBackground,
    onBackground: "#ffffff",
    onSurface: "#ffffff",
    outline: "#4a4d50",
  },
}
