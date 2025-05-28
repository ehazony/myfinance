"use client"
import { createBottomTabNavigator } from "@react-navigation/bottom-tabs"
import { useTheme } from "react-native-paper"
import Icon from "react-native-vector-icons/MaterialCommunityIcons"
import DashboardScreen from "../screens/main/DashboardScreen"
import ChatScreen from "../screens/main/ChatScreen"
import TransactionsScreen from "../screens/main/TransactionsScreen"
import AccountsScreen from "../screens/main/AccountsScreen"
import SettingsScreen from "../screens/main/SettingsScreen"

const Tab = createBottomTabNavigator()

export default function MainNavigator() {
  const theme = useTheme()

  return (
    <Tab.Navigator
      screenOptions={({ route }) => ({
        headerShown: false,
        tabBarIcon: ({ focused, color, size }) => {
          let iconName

          if (route.name === "Chat") {
            iconName = focused ? "message" : "message-outline"
          } else if (route.name === "Dashboard") {
            iconName = focused ? "view-dashboard" : "view-dashboard-outline"
          } else if (route.name === "Transactions") {
            iconName = focused ? "swap-horizontal" : "swap-horizontal"
          } else if (route.name === "Accounts") {
            iconName = focused ? "bank" : "bank-outline"
          } else if (route.name === "Settings") {
            iconName = focused ? "cog" : "cog-outline"
          }

          return <Icon name={iconName} size={size} color={color} />
        },
        tabBarActiveTintColor: theme.colors.primary,
        tabBarInactiveTintColor: theme.colors.onSurfaceVariant,
        tabBarStyle: {
          backgroundColor: theme.colors.surface,
          borderTopColor: theme.colors.outline,
          elevation: 8,
          shadowColor: "#000",
          shadowOffset: { width: 0, height: -2 },
          shadowOpacity: 0.1,
          shadowRadius: 8,
        },
      })}
    >
      <Tab.Screen name="Chat" component={ChatScreen} />
      <Tab.Screen name="Dashboard" component={DashboardScreen} />
      <Tab.Screen name="Transactions" component={TransactionsScreen} />
      <Tab.Screen name="Accounts" component={AccountsScreen} />
      <Tab.Screen name="Settings" component={SettingsScreen} />
    </Tab.Navigator>
  )
}
