"use client"
import { View, StyleSheet, ScrollView, Dimensions } from "react-native"
import { Text, Card, useTheme, IconButton, Button } from "react-native-paper"
import { SafeAreaView } from "react-native-safe-area-context"
import { LinearGradient } from "expo-linear-gradient"
import { LineChart, PieChart } from "react-native-chart-kit"
import GradientCard from "../../components/common/GradientCard"
import { useTheme as useCustomTheme } from "../../context/ThemeContext"

const screenWidth = Dimensions.get("window").width

export default function DashboardScreen() {
  const theme = useTheme()
  const { toggleTheme, isDarkMode } = useCustomTheme()

  const balanceData = {
    labels: ["Jan", "Feb", "Mar", "Apr", "May", "Jun"],
    datasets: [
      {
        data: [2000, 2500, 2200, 2800, 3200, 3500],
        color: (opacity = 1) => `rgba(39, 83, 167, ${opacity})`,
        strokeWidth: 3,
      },
    ],
  }

  const expenseData = [
    {
      name: "Food",
      population: 800,
      color: "#2753a7",
      legendFontColor: theme.colors.onSurface,
      legendFontSize: 12,
    },
    {
      name: "Transport",
      population: 400,
      color: "#9bcada",
      legendFontColor: theme.colors.onSurface,
      legendFontSize: 12,
    },
    {
      name: "Shopping",
      population: 600,
      color: "#d2cdce",
      legendFontColor: theme.colors.onSurface,
      legendFontSize: 12,
    },
    {
      name: "Bills",
      population: 300,
      color: "#272a2d",
      legendFontColor: theme.colors.onSurface,
      legendFontSize: 12,
    },
  ]

  return (
    <LinearGradient colors={[theme.colors.background, theme.colors.surface]} style={styles.container}>
      <SafeAreaView style={styles.safeArea}>
        <View style={styles.header}>
          <View>
            <Text variant="headlineSmall" style={[styles.greeting, { color: theme.colors.onBackground }]}>
              Good Morning
            </Text>
            <Text variant="bodyLarge" style={[styles.username, { color: theme.colors.onSurfaceVariant }]}>
              John Doe
            </Text>
          </View>
          <IconButton
            icon={isDarkMode ? "weather-sunny" : "weather-night"}
            onPress={toggleTheme}
            iconColor={theme.colors.primary}
          />
        </View>

        <ScrollView style={styles.content} showsVerticalScrollIndicator={false}>
          {/* Balance Card */}
          <GradientCard style={styles.balanceCard}>
            <Text variant="bodyMedium" style={styles.balanceLabel}>
              Total Balance
            </Text>
            <Text variant="headlineLarge" style={styles.balanceAmount}>
              $3,500.00
            </Text>
            <View style={styles.balanceRow}>
              <View style={styles.balanceItem}>
                <Text variant="bodySmall" style={styles.balanceSubLabel}>
                  Income
                </Text>
                <Text variant="titleMedium" style={styles.balanceSubAmount}>
                  +$2,100
                </Text>
              </View>
              <View style={styles.balanceItem}>
                <Text variant="bodySmall" style={styles.balanceSubLabel}>
                  Expenses
                </Text>
                <Text variant="titleMedium" style={styles.balanceSubAmount}>
                  -$1,200
                </Text>
              </View>
            </View>
          </GradientCard>

          {/* Quick Actions */}
          <View style={styles.quickActions}>
            <Text variant="titleLarge" style={[styles.sectionTitle, { color: theme.colors.onBackground }]}>
              Quick Actions
            </Text>
            <View style={styles.actionGrid}>
              <Card style={[styles.actionCard, { backgroundColor: theme.colors.surface }]} elevation={2}>
                <Card.Content style={styles.actionContent}>
                  <IconButton icon="plus" iconColor={theme.colors.primary} size={24} />
                  <Text variant="bodyMedium" style={{ color: theme.colors.onSurface }}>
                    Add Income
                  </Text>
                </Card.Content>
              </Card>
              <Card style={[styles.actionCard, { backgroundColor: theme.colors.surface }]} elevation={2}>
                <Card.Content style={styles.actionContent}>
                  <IconButton icon="minus" iconColor={theme.colors.error} size={24} />
                  <Text variant="bodyMedium" style={{ color: theme.colors.onSurface }}>
                    Add Expense
                  </Text>
                </Card.Content>
              </Card>
              <Card style={[styles.actionCard, { backgroundColor: theme.colors.surface }]} elevation={2}>
                <Card.Content style={styles.actionContent}>
                  <IconButton icon="swap-horizontal" iconColor={theme.colors.secondary} size={24} />
                  <Text variant="bodyMedium" style={{ color: theme.colors.onSurface }}>
                    Transfer
                  </Text>
                </Card.Content>
              </Card>
              <Card style={[styles.actionCard, { backgroundColor: theme.colors.surface }]} elevation={2}>
                <Card.Content style={styles.actionContent}>
                  <IconButton icon="chart-line" iconColor={theme.colors.tertiary} size={24} />
                  <Text variant="bodyMedium" style={{ color: theme.colors.onSurface }}>
                    Analytics
                  </Text>
                </Card.Content>
              </Card>
            </View>
          </View>

          {/* Balance Trend Chart */}
          <Card style={[styles.chartCard, { backgroundColor: theme.colors.surface }]} elevation={4}>
            <Card.Content>
              <Text variant="titleLarge" style={[styles.chartTitle, { color: theme.colors.onSurface }]}>
                Balance Trend
              </Text>
              <LineChart
                data={balanceData}
                width={screenWidth - 80}
                height={200}
                chartConfig={{
                  backgroundColor: theme.colors.surface,
                  backgroundGradientFrom: theme.colors.surface,
                  backgroundGradientTo: theme.colors.surface,
                  decimalPlaces: 0,
                  color: (opacity = 1) => `rgba(39, 83, 167, ${opacity})`,
                  labelColor: (opacity = 1) => theme.colors.onSurface,
                  style: {
                    borderRadius: 16,
                  },
                  propsForDots: {
                    r: "6",
                    strokeWidth: "2",
                    stroke: "#2753a7",
                  },
                }}
                bezier
                style={styles.chart}
              />
            </Card.Content>
          </Card>

          {/* Expense Breakdown */}
          <Card style={[styles.chartCard, { backgroundColor: theme.colors.surface }]} elevation={4}>
            <Card.Content>
              <Text variant="titleLarge" style={[styles.chartTitle, { color: theme.colors.onSurface }]}>
                Expense Breakdown
              </Text>
              <PieChart
                data={expenseData}
                width={screenWidth - 80}
                height={200}
                chartConfig={{
                  color: (opacity = 1) => `rgba(0, 0, 0, ${opacity})`,
                }}
                accessor="population"
                backgroundColor="transparent"
                paddingLeft="15"
                absolute
              />
            </Card.Content>
          </Card>

          {/* Recent Transactions */}
          <Card style={[styles.transactionsCard, { backgroundColor: theme.colors.surface }]} elevation={4}>
            <Card.Content>
              <Text variant="titleLarge" style={[styles.sectionTitle, { color: theme.colors.onSurface }]}>
                Recent Transactions
              </Text>
              {[
                { title: "Grocery Store", amount: "-$85.50", category: "Food", time: "2 hours ago" },
                { title: "Salary Deposit", amount: "+$2,500.00", category: "Income", time: "1 day ago" },
                { title: "Gas Station", amount: "-$45.20", category: "Transport", time: "2 days ago" },
              ].map((transaction, index) => (
                <View key={index} style={styles.transactionItem}>
                  <View style={styles.transactionLeft}>
                    <Text variant="bodyLarge" style={{ color: theme.colors.onSurface }}>
                      {transaction.title}
                    </Text>
                    <Text variant="bodySmall" style={{ color: theme.colors.onSurfaceVariant }}>
                      {transaction.category} • {transaction.time}
                    </Text>
                  </View>
                  <Text
                    variant="titleMedium"
                    style={{
                      color: transaction.amount.startsWith("+") ? "#4CAF50" : "#F44336",
                      fontWeight: "bold",
                    }}
                  >
                    {transaction.amount}
                  </Text>
                </View>
              ))}
            </Card.Content>
          </Card>
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
    flexDirection: "row",
    justifyContent: "space-between",
    alignItems: "center",
    paddingHorizontal: 24,
    paddingVertical: 16,
  },
  greeting: {
    fontWeight: "bold",
  },
  username: {
    marginTop: 4,
  },
  content: {
    flex: 1,
    paddingHorizontal: 24,
  },
  balanceCard: {
    marginBottom: 24,
  },
  balanceLabel: {
    color: "#ffffff80",
    marginBottom: 8,
  },
  balanceAmount: {
    color: "#ffffff",
    fontWeight: "bold",
    marginBottom: 16,
  },
  balanceRow: {
    flexDirection: "row",
    justifyContent: "space-between",
  },
  balanceItem: {
    flex: 1,
  },
  balanceSubLabel: {
    color: "#ffffff80",
    marginBottom: 4,
  },
  balanceSubAmount: {
    color: "#ffffff",
    fontWeight: "600",
  },
  quickActions: {
    marginBottom: 24,
  },
  sectionTitle: {
    fontWeight: "bold",
    marginBottom: 16,
  },
  actionGrid: {
    flexDirection: "row",
    flexWrap: "wrap",
    justifyContent: "space-between",
  },
  actionCard: {
    width: "48%",
    marginBottom: 12,
    borderRadius: 12,
  },
  actionContent: {
    alignItems: "center",
    paddingVertical: 8,
  },
  chartCard: {
    marginBottom: 24,
    borderRadius: 16,
  },
  chartTitle: {
    fontWeight: "bold",
    marginBottom: 16,
  },
  chart: {
    borderRadius: 16,
  },
  transactionsCard: {
    marginBottom: 24,
    borderRadius: 16,
  },
  transactionItem: {
    flexDirection: "row",
    justifyContent: "space-between",
    alignItems: "center",
    paddingVertical: 12,
    borderBottomWidth: 1,
    borderBottomColor: "#f0f0f0",
  },
  transactionLeft: {
    flex: 1,
  },
})
