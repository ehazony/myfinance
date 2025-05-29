import React from 'react'
import { Dimensions, StyleSheet, View } from 'react-native'
import { Card, useTheme, Text } from 'react-native-paper'
import { LineChart, PieChart, BarChart } from 'react-native-chart-kit'

const screenWidth = Dimensions.get("window").width

interface ChartCardProps {
  type?: 'line' | 'bar' | 'pie'
  data: any
  title?: string
  width?: number
  height?: number
  chartProps?: any
  showCard?: boolean
}

export default function ChartCard({
  type = 'line',
  data,
  title,
  width = screenWidth - 80,
  height = 200,
  chartProps,
  showCard = true,
}: ChartCardProps) {
  const theme = useTheme()

  const chartConfig = {
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
  }

  const ChartComponent =
    type === 'pie' ? PieChart : type === 'bar' ? BarChart : LineChart

  const lineChartProps = type === 'line' ? { 
    bezier: true,
    formatXLabel: (value: string) => value
  } : {}

  const chartContent = (
    <>
      {title ? (
        <Text variant="titleLarge" style={[styles.chartTitle, { color: theme.colors.onSurface }]}>
          {title}
        </Text>
      ) : null}
      <ChartComponent
        data={data}
        width={width}
        height={height}
        chartConfig={chartConfig}
        style={styles.chart}
        {...lineChartProps}
        {...chartProps}
      />
    </>
  )

  if (!showCard) {
    return (
      <View style={styles.chartOnly}>
        {chartContent}
      </View>
    )
  }

  return (
    <Card style={[styles.chartCard, { backgroundColor: theme.colors.surface }]} elevation={4}>
      <Card.Content>
        {chartContent}
      </Card.Content>
    </Card>
  )
}

const styles = StyleSheet.create({
  chartCard: {
    marginBottom: 24,
    borderRadius: 16,
  },
  chartTitle: {
    fontWeight: 'bold',
    marginBottom: 16,
  },
  chart: {
    borderRadius: 16,
  },
  chartOnly: {
    alignItems: 'center',
    marginVertical: 8,
  },
})
