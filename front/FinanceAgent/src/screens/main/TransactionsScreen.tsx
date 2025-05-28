"use client"

import { useState } from "react"
import { View, StyleSheet, ScrollView, FlatList } from "react-native"
import { Text, Card, useTheme, Searchbar, Chip, FAB, IconButton } from "react-native-paper"
import { SafeAreaView } from "react-native-safe-area-context"
import { LinearGradient } from "expo-linear-gradient"

const transactions = [
  {
    id: "1",
    title: "Grocery Store",
    amount: -85.5,
    category: "Food",
    date: "2024-01-15",
    time: "14:30",
    type: "expense",
  },
  {
    id: "2",
    title: "Salary Deposit",
    amount: 2500.0,
    category: "Income",
    date: "2024-01-14",
    time: "09:00",
    type: "income",
  },
  {
    id: "3",
    title: "Gas Station",
    amount: -45.2,
    category: "Transport",
    date: "2024-01-13",
    time: "18:45",
    type: "expense",
  },
  {
    id: "4",
    title: "Coffee Shop",
    amount: -12.5,
    category: "Food",
    date: "2024-01-13",
    time: "08:15",
    type: "expense",
  },
  {
    id: "5",
    title: "Online Shopping",
    amount: -156.99,
    category: "Shopping",
    date: "2024-01-12",
    time: "20:30",
    type: "expense",
  },
  {
    id: "6",
    title: "Freelance Payment",
    amount: 800.0,
    category: "Income",
    date: "2024-01-11",
    time: "16:20",
    type: "income",
  },
]

const categories = ["All", "Food", "Transport", "Shopping", "Income", "Bills"]

export default function TransactionsScreen() {
  const theme = useTheme()
  const [searchQuery, setSearchQuery] = useState("")
  const [selectedCategory, setSelectedCategory] = useState("All")
  const [filteredTransactions, setFilteredTransactions] = useState(transactions)

  const filterTransactions = (query: string, category: string) => {
    let filtered = transactions

    if (category !== "All") {
      filtered = filtered.filter((t) => t.category === category)
    }

    if (query) {
      filtered = filtered.filter(
        (t) =>
          t.title.toLowerCase().includes(query.toLowerCase()) || t.category.toLowerCase().includes(query.toLowerCase()),
      )
    }

    setFilteredTransactions(filtered)
  }

  const handleSearch = (query: string) => {
    setSearchQuery(query)
    filterTransactions(query, selectedCategory)
  }

  const handleCategoryFilter = (category: string) => {
    setSelectedCategory(category)
    filterTransactions(searchQuery, category)
  }

  const getCategoryIcon = (category: string) => {
    switch (category) {
      case "Food":
        return "food"
      case "Transport":
        return "car"
      case "Shopping":
        return "shopping"
      case "Income":
        return "cash-plus"
      case "Bills":
        return "receipt"
      default:
        return "cash"
    }
  }

  const renderTransaction = ({ item }: { item: any }) => (
    <Card style={[styles.transactionCard, { backgroundColor: theme.colors.surface }]} elevation={2}>
      <Card.Content style={styles.transactionContent}>
        <View style={styles.transactionLeft}>
          <View style={[styles.iconContainer, { backgroundColor: item.type === "income" ? "#4CAF5020" : "#F4433620" }]}>
            <IconButton
              icon={getCategoryIcon(item.category)}
              iconColor={item.type === "income" ? "#4CAF50" : "#F44336"}
              size={20}
            />
          </View>
          <View style={styles.transactionDetails}>
            <Text variant="bodyLarge" style={[styles.transactionTitle, { color: theme.colors.onSurface }]}>
              {item.title}
            </Text>
            <Text variant="bodySmall" style={{ color: theme.colors.onSurfaceVariant }}>
              {item.category} • {item.time}
            </Text>
            <Text variant="bodySmall" style={{ color: theme.colors.onSurfaceVariant }}>
              {new Date(item.date).toLocaleDateString()}
            </Text>
          </View>
        </View>
        <View style={styles.transactionRight}>
          <Text
            variant="titleMedium"
            style={[styles.transactionAmount, { color: item.amount > 0 ? "#4CAF50" : "#F44336" }]}
          >
            {item.amount > 0 ? "+" : ""}${Math.abs(item.amount).toFixed(2)}
          </Text>
        </View>
      </Card.Content>
    </Card>
  )

  return (
    <LinearGradient colors={[theme.colors.background, theme.colors.surface]} style={styles.container}>
      <SafeAreaView style={styles.safeArea}>
        <View style={styles.header}>
          <Text variant="headlineSmall" style={[styles.title, { color: theme.colors.onBackground }]}>
            Transactions
          </Text>
        </View>

        <View style={styles.searchContainer}>
          <Searchbar
            placeholder="Search transactions..."
            onChangeText={handleSearch}
            value={searchQuery}
            style={[styles.searchbar, { backgroundColor: theme.colors.surface }]}
            iconColor={theme.colors.onSurfaceVariant}
            placeholderTextColor={theme.colors.onSurfaceVariant}
          />
        </View>

        <ScrollView
          horizontal
          showsHorizontalScrollIndicator={false}
          style={styles.categoryContainer}
          contentContainerStyle={styles.categoryContent}
        >
          {categories.map((category) => (
            <Chip
              key={category}
              selected={selectedCategory === category}
              onPress={() => handleCategoryFilter(category)}
              style={[styles.categoryChip, selectedCategory === category && { backgroundColor: theme.colors.primary }]}
              textStyle={{
                color: selectedCategory === category ? "#ffffff" : theme.colors.onSurface,
              }}
            >
              {category}
            </Chip>
          ))}
        </ScrollView>

        <FlatList
          data={filteredTransactions}
          renderItem={renderTransaction}
          keyExtractor={(item) => item.id}
          style={styles.transactionsList}
          contentContainerStyle={styles.transactionsContent}
          showsVerticalScrollIndicator={false}
        />

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
  searchContainer: {
    paddingHorizontal: 24,
    marginBottom: 16,
  },
  searchbar: {
    elevation: 2,
    borderRadius: 12,
  },
  categoryContainer: {
    marginBottom: 16,
  },
  categoryContent: {
    paddingHorizontal: 24,
    gap: 8,
  },
  categoryChip: {
    marginRight: 8,
  },
  transactionsList: {
    flex: 1,
  },
  transactionsContent: {
    paddingHorizontal: 24,
    paddingBottom: 100,
  },
  transactionCard: {
    marginBottom: 12,
    borderRadius: 12,
  },
  transactionContent: {
    paddingVertical: 8,
  },
  transactionLeft: {
    flexDirection: "row",
    alignItems: "center",
    flex: 1,
  },
  iconContainer: {
    borderRadius: 8,
    marginRight: 12,
  },
  transactionDetails: {
    flex: 1,
  },
  transactionTitle: {
    fontWeight: "600",
    marginBottom: 2,
  },
  transactionRight: {
    alignItems: "flex-end",
  },
  transactionAmount: {
    fontWeight: "bold",
  },
  fab: {
    position: "absolute",
    margin: 16,
    right: 0,
    bottom: 0,
  },
})
