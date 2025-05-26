import React from 'react';
import { View, Text, StyleSheet, ScrollView } from 'react-native';
import { colors } from '@/constants';
import BottomNav from '@/components/BottomNav';

export default function HomeScreen() {
  return (
    <View style={styles.root}>
      <ScrollView contentContainerStyle={styles.container}>
      <View style={styles.header}>
        <Text style={styles.headerTitle}>Dashboard</Text>
      </View>
      <View style={styles.card}>
        <Text style={styles.cardTitle}>Balance</Text>
        <Text style={styles.balance}>$12,345.67</Text>
      </View>
      <View style={styles.summaryRow}>
        <View style={[styles.summaryCard, styles.incomeCard]}>
          <Text style={styles.summaryLabel}>Income</Text>
          <Text style={styles.summaryValue}>$2,400</Text>
        </View>
        <View style={[styles.summaryCard, styles.expenseCard]}>
          <Text style={styles.summaryLabel}>Expenses</Text>
          <Text style={styles.summaryValue}>$1,100</Text>
        </View>
      </View>
      <View style={styles.section}>
        <Text style={styles.sectionTitle}>Recent Transactions</Text>
        <View style={styles.transactionItem}>
          <View style={[styles.transactionIcon, { backgroundColor: colors.primaryBlue }]} />
          <View style={styles.transactionDetails}>
            <Text style={styles.transactionTitle}>Coffee Shop</Text>
            <Text style={styles.transactionDate}>Jun 1</Text>
          </View>
          <Text style={[styles.transactionAmount, styles.expense]}>- $5.25</Text>
        </View>
        <View style={styles.transactionItem}>
          <View style={[styles.transactionIcon, { backgroundColor: colors.accentBlue }]} />
          <View style={styles.transactionDetails}>
            <Text style={styles.transactionTitle}>Salary</Text>
            <Text style={styles.transactionDate}>May 31</Text>
          </View>
          <Text style={[styles.transactionAmount, styles.income]}>+ $2,400</Text>
        </View>
      </View>
      </ScrollView>
      <BottomNav />
    </View>
  );
}

const styles = StyleSheet.create({
  root: {
    flex: 1,
  },
  container: {
    padding: 16,
  },
  header: {
    marginBottom: 16,
  },
  headerTitle: {
    fontSize: 24,
    fontWeight: '600',
  },
  card: {
    backgroundColor: colors.primaryBlue,
    borderRadius: 12,
    padding: 20,
    marginBottom: 16,
  },
  cardTitle: {
    color: 'white',
    opacity: 0.7,
  },
  balance: {
    color: 'white',
    fontSize: 28,
    fontWeight: '700',
    marginTop: 8,
  },
  summaryRow: {
    flexDirection: 'row',
    gap: 16,
    marginBottom: 24,
  },
  summaryCard: {
    flex: 1,
    borderRadius: 12,
    padding: 16,
  },
  incomeCard: {
    backgroundColor: colors.income,
  },
  expenseCard: {
    backgroundColor: colors.expense,
  },
  summaryLabel: {
    color: 'white',
    opacity: 0.9,
    marginBottom: 8,
  },
  summaryValue: {
    color: 'white',
    fontSize: 20,
    fontWeight: '700',
  },
  section: {
    marginBottom: 24,
  },
  sectionTitle: {
    fontSize: 18,
    fontWeight: '600',
    marginBottom: 12,
  },
  transactionItem: {
    flexDirection: 'row',
    alignItems: 'center',
    paddingVertical: 8,
    borderBottomWidth: StyleSheet.hairlineWidth,
    borderBottomColor: '#ccc',
  },
  transactionIcon: {
    width: 40,
    height: 40,
    borderRadius: 20,
    marginRight: 12,
  },
  transactionDetails: {
    flex: 1,
  },
  transactionTitle: {
    fontWeight: '500',
  },
  transactionDate: {
    fontSize: 12,
    color: '#888',
  },
  transactionAmount: {
    fontWeight: '600',
  },
  income: {
    color: colors.income,
  },
  expense: {
    color: colors.expense,
  },
});
