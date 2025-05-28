"use client"
import { View, StyleSheet, ScrollView } from "react-native"
import { Text, Card, useTheme, Switch, List, Avatar, Divider } from "react-native-paper"
import { SafeAreaView } from "react-native-safe-area-context"
import { LinearGradient } from "expo-linear-gradient"
import { useTheme as useCustomTheme } from "../../context/ThemeContext"
import { useAuth } from "../../context/AuthContext"
import GradientCard from "../../components/common/GradientCard"
import CustomButton from "../../components/common/CustomButton"

export default function SettingsScreen() {
  const theme = useTheme()
  const { isDarkMode, toggleTheme } = useCustomTheme()
  const { user, logout } = useAuth()

  const settingsGroups = [
    {
      title: "Account",
      items: [
        { title: "Profile Information", icon: "account", onPress: () => {} },
        { title: "Security & Privacy", icon: "shield-account", onPress: () => {} },
        { title: "Notifications", icon: "bell", onPress: () => {} },
      ],
    },
    {
      title: "App Preferences",
      items: [
        { title: "Currency", icon: "currency-usd", subtitle: "USD ($)", onPress: () => {} },
        { title: "Language", icon: "translate", subtitle: "English", onPress: () => {} },
        { title: "Date Format", icon: "calendar", subtitle: "MM/DD/YYYY", onPress: () => {} },
      ],
    },
    {
      title: "Data & Backup",
      items: [
        { title: "Export Data", icon: "download", onPress: () => {} },
        { title: "Import Data", icon: "upload", onPress: () => {} },
        { title: "Backup Settings", icon: "cloud-upload", onPress: () => {} },
      ],
    },
    {
      title: "Support",
      items: [
        { title: "Help Center", icon: "help-circle", onPress: () => {} },
        { title: "Contact Support", icon: "email", onPress: () => {} },
        { title: "Rate App", icon: "star", onPress: () => {} },
        { title: "About", icon: "information", onPress: () => {} },
      ],
    },
  ]

  return (
    <LinearGradient colors={[theme.colors.background, theme.colors.surface]} style={styles.container}>
      <SafeAreaView style={styles.safeArea}>
        <View style={styles.header}>
          <Text variant="headlineSmall" style={[styles.title, { color: theme.colors.onBackground }]}>
            Settings
          </Text>
        </View>

        <ScrollView style={styles.content} showsVerticalScrollIndicator={false}>
          {/* Profile Card */}
          <GradientCard style={styles.profileCard}>
            <View style={styles.profileContent}>
              <Avatar.Text size={64} label={user?.first_name?.charAt(0) || user?.username?.charAt(0) || "U"} style={styles.avatar} />
              <View style={styles.userInfo}>
                <Text style={styles.userName}>
                  {user ? `${user.first_name} ${user.last_name}`.trim() || user.username : "User"}
                </Text>
                <Text variant="bodyMedium" style={styles.profileEmail}>
                  {user?.email || "user@example.com"}
                </Text>
              </View>
            </View>
          </GradientCard>

          {/* Theme Toggle */}
          <Card style={[styles.themeCard, { backgroundColor: theme.colors.surface }]} elevation={2}>
            <List.Item
              title="Dark Mode"
              description="Switch between light and dark themes"
              left={(props) => <List.Icon {...props} icon="theme-light-dark" />}
              right={() => <Switch value={isDarkMode} onValueChange={toggleTheme} color={theme.colors.primary} />}
            />
          </Card>

          {/* Settings Groups */}
          {settingsGroups.map((group, groupIndex) => (
            <View key={groupIndex} style={styles.settingsGroup}>
              <Text variant="titleMedium" style={[styles.groupTitle, { color: theme.colors.onBackground }]}>
                {group.title}
              </Text>
              <Card style={[styles.groupCard, { backgroundColor: theme.colors.surface }]} elevation={2}>
                {group.items.map((item, itemIndex) => (
                  <View key={itemIndex}>
                    <List.Item
                      title={item.title}
                      description={item.subtitle}
                      left={(props) => <List.Icon {...props} icon={item.icon} />}
                      right={(props) => <List.Icon {...props} icon="chevron-right" />}
                      onPress={item.onPress}
                      style={styles.listItem}
                    />
                    {itemIndex < group.items.length - 1 && (
                      <Divider style={[styles.divider, { backgroundColor: theme.colors.outline }]} />
                    )}
                  </View>
                ))}
              </Card>
            </View>
          ))}

          {/* App Version */}
          <Card style={[styles.versionCard, { backgroundColor: theme.colors.surface }]} elevation={2}>
            <Card.Content style={styles.versionContent}>
              <Text variant="bodyMedium" style={{ color: theme.colors.onSurfaceVariant }}>
                Finance Tracker
              </Text>
              <Text variant="bodySmall" style={{ color: theme.colors.onSurfaceVariant }}>
                Version 1.0.0
              </Text>
            </Card.Content>
          </Card>

          {/* Logout Button */}
          <CustomButton
            title="Sign Out"
            onPress={logout}
            mode="outlined"
            style={[styles.logoutButton, { borderColor: theme.colors.error }]}
          />
        </ScrollView>
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
  header: {
    paddingHorizontal: 24,
    paddingVertical: 16,
  },
  title: {
    fontWeight: "bold",
  },
  content: {
    flex: 1,
    paddingHorizontal: 24,
  },
  profileCard: {
    marginBottom: 24,
  },
  profileContent: {
    flexDirection: "row",
    alignItems: "center",
  },
  avatar: {
    backgroundColor: "rgba(255, 255, 255, 0.2)",
    marginRight: 16,
  },
  userInfo: {
    flex: 1,
  },
  userName: {
    color: "#ffffff",
    fontWeight: "bold",
    marginBottom: 4,
  },
  profileEmail: {
    color: "#ffffff80",
  },
  themeCard: {
    marginBottom: 24,
    borderRadius: 12,
  },
  settingsGroup: {
    marginBottom: 24,
  },
  groupTitle: {
    fontWeight: "bold",
    marginBottom: 12,
  },
  groupCard: {
    borderRadius: 12,
  },
  listItem: {
    paddingVertical: 8,
  },
  divider: {
    marginLeft: 56,
  },
  versionCard: {
    marginBottom: 24,
    borderRadius: 12,
  },
  versionContent: {
    alignItems: "center",
  },
  logoutButton: {
    marginBottom: 32,
  },
})
