"use client"
import 'react-native-url-polyfill/auto';
import { StatusBar } from "expo-status-bar"
import { NavigationContainer } from "@react-navigation/native"
import { createNativeStackNavigator } from "@react-navigation/native-stack"
import { PaperProvider } from "react-native-paper"
import { SafeAreaProvider } from "react-native-safe-area-context"
import { registerRootComponent } from 'expo';
import { View, Text, StyleSheet } from "react-native"
import { ThemeProvider } from "./src/context/ThemeContext"
import { AuthProvider } from "./src/context/AuthContext"
import AuthNavigator from "./src/navigation/AuthNavigator"
import MainNavigator from "./src/navigation/MainNavigator"
import { useAuth } from "./src/context/AuthContext"
import { useTheme } from "./src/context/ThemeContext"
import { lightTheme, darkTheme } from "./src/theme/theme"

const Stack = createNativeStackNavigator()

function AppContent() {
  console.log("AppContent rendering...");
  try {
    const { isAuthenticated } = useAuth();
    const { isDarkMode } = useTheme();
    console.log("Auth state:", isAuthenticated);
    console.log("Theme state:", isDarkMode);

    return (
      <PaperProvider theme={isDarkMode ? darkTheme : lightTheme}>
        <NavigationContainer>
          <StatusBar style={isDarkMode ? "light" : "dark"} />
          {isAuthenticated ? <MainNavigator /> : <AuthNavigator />}
        </NavigationContainer>
      </PaperProvider>
    );
  } catch (error) {
    console.error("Error in AppContent:", error);
    return (
      <View style={styles.errorContainer}>
        <Text style={styles.errorText}>Error rendering AppContent: {error instanceof Error ? error.message : 'Unknown error'}</Text>
      </View>
    );
  }
}

export default function App() {
  console.log("App component starting...");
  return (
    <SafeAreaProvider>
      <ThemeProvider>
        <AuthProvider>
          <AppContent />
        </AuthProvider>
      </ThemeProvider>
    </SafeAreaProvider>
  );
}

const styles = StyleSheet.create({
  errorContainer: {
    flex: 1,
    justifyContent: 'center',
    alignItems: 'center',
    backgroundColor: 'red',
    padding: 10,
  },
  errorText: {
    color: 'white',
    fontSize: 16,
    textAlign: 'center',
  },
});

registerRootComponent(App);
