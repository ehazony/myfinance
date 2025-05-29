import React from 'react'
import { TouchableOpacity, Image, StyleSheet, Dimensions } from 'react-native'
import ChartCard from './ChartCard'

const screenWidth = Dimensions.get('window').width

interface MediaItemProps {
  type: 'chart' | 'image'
  data: any // chartData for charts, imageUrl for images
  onPress: () => void
  width?: number
  height?: number
  title?: string
}

export default function MediaItem({
  type,
  data,
  onPress,
  width = 250,
  height = type === 'chart' ? 220 : 180,
  title
}: MediaItemProps) {
  
  if (type === 'chart') {
    return (
      <TouchableOpacity
        onPress={onPress}
        activeOpacity={0.8}
        style={styles.container}
      >
        <ChartCard
          data={data}
          title={title || "Chart"}
          width={width}
          height={height}
        />
      </TouchableOpacity>
    )
  }

  // type === 'image'
  return (
    <TouchableOpacity 
      style={styles.imageContainer}
      onPress={onPress}
      activeOpacity={0.8}
    >
      <Image
        source={{ uri: data }}
        style={[styles.image, { width, height }]}
        resizeMode="cover"
      />
    </TouchableOpacity>
  )
}

const styles = StyleSheet.create({
  container: {
    alignItems: 'center',
  },
  imageContainer: {
    borderRadius: 12,
    overflow: 'hidden',
  },
  image: {
    borderRadius: 12,
  },
}) 