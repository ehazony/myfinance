"use client"
import { View, StyleSheet, ScrollView } from "react-native"
import { Text, Card, useTheme, FAB, IconButton, ProgressBar } from "react-native-paper"
import { SafeAreaView } from "react-native-safe-area-context"
import { LinearGradient } from "expo-linear-gradient"
import GradientCard from "../../components/common/GradientCard"

const accounts = [
  {
    id: "1",
    name: "Checking Account",
    bank: "Chase Bank",
    balance: 2500.0,
    type: "checking",
    cardNumber: "**** 1234",
  },
  {
    id: "2",
    name: "Savings Account",
    bank: "Bank of America",
    balance: 15000.0,
    type: "savings",
    cardNumber: "**** 5678",
  },
  {
    id: "3",
    name: "Credit Card",
    bank: "Capital One",
    balance: -850.0,
    type: "credit",
    cardNumber: "**** 9012",
    limit: 5000,
  },
]

const goals = [
  {
    id: "1",
    name: "Emergency Fund",
    target: 10000,
    current: 6500,
    color: "#4CAF50",
  },
  {
    id: "2",
    name: "Vacation",
    target: 3000,
    current: 1200,
    color: "#2196F3",
  },
  {
    id: "3",
    name: "New Car",
    target: 25000,
    current: 8500,
    color: "#FF9800",
  },
]

export default function AccountsScreen() {
  const theme = useTheme()

  const getAccountIcon = (type: string) => {
    switch (type) {
      case "checking":
        return "bank"
      case "savings":
        return "piggy-bank"
      case "credit":
        return "credit-card"
      default:
        return "bank"
    }
  }

  const getAccountGradient = (type: string) => {
    switch (type) {
      case "checking":
        return ["#2753a7", "#9bcada"]
      case "savings":
        return ["#4CAF50", "#81C784"]
      case "credit":
        return ["#F44336", "#EF5350"]
      default:
        return ["#2753a7", "#9bcada"]
    }
  }

  return (
    <LinearGradient colors={[theme.colors.background, theme.colors.surface]} style={styles.container}>
      <SafeAreaView style={styles.safeArea}>
        <View style={styles.header}>
          <Text variant="headlineSmall" style={[styles.title, { color: theme.colors.onBackground }]}>
            Accounts
          </Text>
        </View>

        <ScrollView style={styles.content} showsVerticalScrollIndicator={false}>
          {/* Total Balance */}
          <GradientCard style={styles.totalCard}>
            <Text variant="bodyMedium" style={styles.totalLabel}>
              Total Net Worth
            </Text>
            <Text variant="headlineLarge" style={styles.totalAmount}>
              $16,650.00
            </Text>
            <View style={styles.totalBreakdown}>
              <View style={styles.breakdownItem}>
                <Text variant="bodySmall" style={styles.breakdownLabel}>
                  Assets
                </Text>
                <Text variant="titleMedium" style={styles.breakdownAmount}>
                  $17,500
                </Text>
              </View>
              <View style={styles.breakdownItem}>
                <Text variant="bodySmall" style={styles.breakdownLabel}>
                  Liabilities
                </Text>
                <Text variant="titleMedium" style={styles.breakdownAmount}>
                  $850
                </Text>
              </View>
            </View>
          </GradientCard>

          {/* Accounts List */}
          <View style={styles.section}>
            <Text variant="titleLarge" style={[styles.sectionTitle, { color: theme.colors.onBackground }]}>
              My Accounts
            </Text>
            {accounts.map((account) => (
              <GradientCard key={account.id} colors={getAccountGradient(account.type)} style={styles.accountCard}>
                <View style={styles.accountHeader}>
                  <View style={styles.accountInfo}>
                    <IconButton
                      icon={getAccountIcon(account.type)}
                      iconColor="#ffffff"
                      size={24}
                      style={styles.accountIcon}
                    />
                    <View>
                      <Text variant="titleMedium" style={styles.accountName}>
                        {account.name}
                      </Text>
                      <Text variant="bodySmall" style={styles.accountBank}>
                        {account.bank} • {account.cardNumber}
                      </Text>
                    </View>
                  </View>
                  <IconButton icon="dots-vertical" iconColor="#ffffff" size={20} />
                </View>
                <View style={styles.accountBalance}>
                  <Text variant="headlineSmall" style={styles.balanceAmount}>
                    ${Math.abs(account.balance).toLocaleString("en-US", { minimumFractionDigits: 2 })}
                  </Text>
                  {account.type === "credit" && account.limit && (
                    <Text variant="bodySmall" style={styles.creditLimit}>
                      Limit: ${account.limit.toLocaleString()}
                    </Text>
                  )}
                </View>
              </GradientCard>
            ))}
          </View>

          {/* Savings Goals */}
          <View style={styles.section}>
            <Text variant="titleLarge" style={[styles.sectionTitle, { color: theme.colors.onBackground }]}>
              Savings Goals
            </Text>
            {goals.map((goal) => (
              <Card key={goal.id} style={[styles.goalCard, { backgroundColor: theme.colors.surface }]} elevation={2}>
                <Card.Content>
                  <View style={styles.goalHeader}>
                    <Text variant="titleMedium" style={{ color: theme.colors.onSurface }}>
                      {goal.name}
                    </Text>
                    <Text variant="bodyMedium" style={{ color: theme.colors.onSurfaceVariant }}>
                      ${goal.current.toLocaleString()} / ${goal.target.toLocaleString()}
                    </Text>
                  </View>
                  <ProgressBar progress={goal.current / goal.target} color={goal.color} style={styles.progressBar} />
                  <Text variant="bodySmall" style={[styles.progressText, { color: theme.colors.onSurfaceVariant }]}>
                    {Math.round((goal.current / goal.target) * 100)}% complete
                  </Text>
                </Card.Content>
              </Card>
            ))}
          </View>

          {/* Quick Actions */}
          <View style={styles.section}>
            <Text variant="titleLarge" style={[styles.sectionTitle, { color: theme.colors.onBackground }]}>
              Quick Actions
            </Text>
            <View style={styles.actionGrid}>
              <Card style={[styles.actionCard, { backgroundColor: theme.colors.surface }]} elevation={2}>
                <Card.Content style={styles.actionContent}>
                  <IconButton icon="plus" iconColor={theme.colors.primary} size={24} />
                  <Text variant="bodyMedium" style={{ color: theme.colors.onSurface }}>
                    Add Account
                  </Text>
                </Card.Content>
              </Card>
              <Card style={[styles.actionCard, { backgroundColor: theme.colors.surface }]} elevation={2}>
                <Card.Content style={styles.actionContent}>
                  <IconButton icon="target" iconColor={theme.colors.secondary} size={24} />
                  <Text variant="bodyMedium" style={{ color: theme.colors.onSurface }}>
                    New Goal
                  </Text>
                </Card.Content>
              </Card>
              <Card style={[styles.actionCard, { backgroundColor: theme.colors.surface }]} elevation={2}>
                <Card.Content style={styles.actionContent}>
                  <IconButton icon="swap-horizontal" iconColor={theme.colors.tertiary} size={24} />
                  <Text variant="bodyMedium" style={{ color: theme.colors.onSurface }}>
                    Transfer
                  </Text>
                </Card.Content>
              </Card>
              <Card style={[styles.actionCard, { backgroundColor: theme.colors.surface }]} elevation={2}>
                <Card.Content style={styles.actionContent}>
                  <IconButton icon="chart-line" iconColor={theme.colors.primary} size={24} />
                  <Text variant="bodyMedium" style={{ color: theme.colors.onSurface }}>
                    Reports
                  </Text>
                </Card.Content>
              </Card>
            </View>
          </View>
        </ScrollView>

        <FAB icon="plus" style={[styles.fab, { backgroundColor: theme.colors.primary }]} onPress={() => {}} />
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
  totalCard: {
    marginBottom: 24,
  },
  totalLabel: {
    color: "#ffffff80",
    marginBottom: 8,
  },
  totalAmount: {
    color: "#ffffff",
    fontWeight: "bold",
    marginBottom: 16,
  },
  totalBreakdown: {
    flexDirection: "row",
    justifyContent: "space-between",
  },
  breakdownItem: {
    flex: 1,
  },
  breakdownLabel: {
    color: "#ffffff80",
    marginBottom: 4,
  },
  breakdownAmount: {
    color: "#ffffff",
    fontWeight: "600",
  },
  section: {
    marginBottom: 24,
  },
  sectionTitle: {
    fontWeight: "bold",
    marginBottom: 16,
  },
  accountCard: {
    marginBottom: 16,
  },
  accountHeader: {
    flexDirection: "row",
    justifyContent: "space-between",
    alignItems: "center",
    marginBottom: 12,
  },
  accountInfo: {
    flexDirection: "row",
    alignItems: "center",
  },
  accountIcon: {
    margin: 0,
    marginRight: 8,
  },
  accountName: {
    color: "#ffffff",
    fontWeight: "bold",
  },
  accountBank: {
    color: "#ffffff80",
    marginTop: 2,
  },
  accountBalance: {
    alignItems: "flex-start",
  },
  balanceAmount: {
    color: "#ffffff",
    fontWeight: "bold",
  },
  creditLimit: {
    color: "#ffffff80",
    marginTop: 4,
  },
  goalCard: {
    marginBottom: 12,
    borderRadius: 12,
  },
  goalHeader: {
    flexDirection: "row",
    justifyContent: "space-between",
    alignItems: "center",
    marginBottom: 12,
  },
  progressBar: {
    height: 8,
    borderRadius: 4,
    marginBottom: 8,
  },
  progressText: {
    textAlign: "right",
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
  fab: {
    position: "absolute",
    margin: 16,
    right: 0,
    bottom: 0,
  },
})
