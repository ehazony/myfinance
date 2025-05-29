import React from 'react'
import { Dimensions, StyleSheet } from 'react-native'
import { Card, useTheme, Text } from 'react-native-paper'
import { LineChart, PieChart, BarChart } from 'react-native-chart-kit'

interface ChartCardProps {
  type?: 'line' | 'bar' | 'pie'
  data: any
  title?: string
  width?: number
  height?: number
  chartProps?: any
}

export default function ChartCard({
  type = 'line',
  data,
  title,
  width = Dimensions.get('window').width - 80,
  height = 200,
  chartProps,
}: ChartCardProps) {
  const theme = useTheme()

  const chartConfig = {
    backgroundColor: theme.colors.surface,
    backgroundGradientFrom: theme.colors.surface,
    backgroundGradientTo: theme.colors.surface,
    decimalPlaces: 0,
    color: (opacity = 1) => `rgba(39, 83, 167, ${opacity})`,
    labelColor: (opacity = 1) => theme.colors.onSurface,
    style: { borderRadius: 16 },
    propsForDots: { r: '6', strokeWidth: '2', stroke: '#2753a7' },
    propsForBackgroundLines: {
      strokeDasharray: '5,5',
      stroke: '#E5E7EB',
      strokeWidth: 1,
    },
  }

  const ChartComponent =
    type === 'pie' ? PieChart : type === 'bar' ? BarChart : LineChart

  return (
    <Card style={styles.card} elevation={4}>
      <Card.Content>
        {title ? (
          <Text variant="titleLarge" style={[styles.title, { color: theme.colors.onSurface }]}>{title}</Text>
        ) : null}
        <ChartComponent
          data={data}
          width={width}
          height={height}
          chartConfig={chartConfig}
          style={styles.chart}
          {...chartProps}
        />
      </Card.Content>
    </Card>
  )
}

const styles = StyleSheet.create({
  card: {
    borderRadius: 16,
    marginBottom: 24,
  },
  title: {
    fontWeight: 'bold',
    marginBottom: 16,
  },
  chart: {
    borderRadius: 16,
  },
})
