<template>
  <!-- 工具栏 -->
  <div class="toolbar" :class="{ 'map-minimized': isMinimized }">
    <div class="toolbar-button" @click="toggleMap">
      <div class="button-icon">🗺️</div>
      <div class="button-tooltip">Map</div>
    </div>
  </div>

  <!-- 小地图 -->
  <div class="mini-map" v-show="!isMinimized">
    <div class="map-header">
      <div class="map-title">SHARP SCHOOL</div>
      <div class="current-time">{{ store.gameState.currentTime }}</div>
      <div class="minimize-button" @click="toggleMap">
        <span>−</span>
      </div>
    </div>
    
    <div class="map-container">
      <!-- 连接走廊 -->
      <div class="corridors">
        <div class="corridor-h"></div>
        <div class="corridor-v"></div>
      </div>

      <!-- 地图区域 -->
      <div class="map-areas">
        <!-- 考试大厅（左侧） -->
        <div class="map-area exam-hall">
          <div class="area-name">Examination Hall</div>
          <div class="area-icon">📝</div>
          <div class="area-desc">Preliminary Screening Test</div>
        </div>
        
        <!-- 楼梯（右上） -->
        <div class="map-area stairs">
          <div class="area-name">Stairway</div>
          <div class="area-icon">⬆️</div>
          <div class="area-desc">To Rooftop</div>
        </div>
        
        <!-- 校长办公室（右下） -->
        <div class="map-area office">
          <div class="area-name">Principal's Office</div>
          <div class="area-icon">🏢</div>
          <div class="area-desc">Robert's Office</div>
        </div>
      </div>

      <!-- 玩家和NPC标记 -->
      <div 
        v-for="marker in locationMarkers" 
        :key="marker.id"
        :class="['marker', marker.type]"
        :style="getMarkerPosition(marker.location)"
      >
        <div class="marker-dot"></div>
        <div class="marker-pulse"></div>
        <div class="marker-label">{{ marker.label }}</div>
      </div>
    </div>

    <!-- 图例 -->
    <div class="map-legend">
      <div class="legend-item">
        <span class="legend-marker player"></span>
        <span>You (Labor Class)</span>
      </div>
      <div class="legend-item">
        <span class="legend-marker joey"></span>
        <span>Joey (Senior)</span>
      </div>
      <div class="legend-item">
        <span class="legend-marker robert"></span>
        <span>Principal Robert</span>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed } from 'vue'
import { useGameStore } from '../stores/game'

const store = useGameStore()
const isMinimized = ref(false)

const toggleMap = () => {
  isMinimized.value = !isMinimized.value
}

// 修改地图区域位置定义
const mapLocations = {
  exam_hall: { x: 20, y: 50 },   // 左侧
  corridor: { x: 50, y: 50 },    // 中央
  stairs: { x: 80, y: 20 },      // 右上
  office: { x: 80, y: 70 },      // 右下
  rooftop: { x: 80, y: 20 }      // 与楼梯位置相同
}

// 计算所有标记的位置
const locationMarkers = computed(() => {
  const markers = [
    {
      id: 'player',
      type: 'player-marker',
      label: 'You',
      location: store.gameState.playerLocation
    },
    ...store.gameState.agents.map(agent => ({
      id: agent.name.toLowerCase(),
      type: agent.name.toLowerCase(),
      label: agent.name,
      location: agent.location
    }))
  ]
  return markers
})

// 修改获取标记位置的方法
const getMarkerPosition = (location: string) => {
  // 如果目标是屋顶，显示在楼梯位置
  if (location === 'rooftop') {
    location = 'stairs'
  }
  
  const pos = mapLocations[location as keyof typeof mapLocations] || mapLocations.corridor
  return {
    left: `${pos.x}%`,
    top: `${pos.y}%`
  }
}
</script>

<style scoped>
.mini-map {
  position: fixed;
  bottom: 2vh;
  right: 2vh;
  width: 25vw;
  min-width: 300px;
  max-width: 450px;
  height: 600px;
  background: rgba(15, 23, 42, 0.98);
  border-radius: 1rem;
  padding: 1.5rem;
  color: #e2e8f0;
  box-shadow: 0 0.5rem 2rem rgba(0, 0, 0, 0.4);
  backdrop-filter: blur(12px);
  border: 1px solid rgba(255, 255, 255, 0.1);
  font-family: 'Segoe UI', system-ui, sans-serif;
  z-index: 1000;
  transition: all 0.3s ease;
}

.map-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1rem;
  padding-bottom: 0.75rem;
  border-bottom: 1px solid rgba(255, 255, 255, 0.1);
}

.map-title {
  font-weight: 600;
  font-size: 1.25rem;
  color: #fff;
  letter-spacing: 0.1em;
  text-shadow: 0 0 10px rgba(255, 255, 255, 0.3);
}

.current-time {
  font-size: 1.1rem;
  color: #94a3b8;
  font-weight: 500;
  font-variant-numeric: tabular-nums;
}

.map-container {
  position: relative;
  aspect-ratio: 2/2.5;
  /* min-height: 0%; */
  background: rgba(30, 41, 59, 0.98);
  border-radius: 0.75rem;
  padding: 1.5rem;
  margin-bottom: 1rem;
}

.map-areas {
  position: relative;
  width: 100%;
  height: 100%;
}

.map-area {
  position: absolute;
  width: 28%;
  aspect-ratio: 3/2;
  background: rgba(51, 65, 85, 0.4);
  border: 1px solid rgba(148, 163, 184, 0.2);
  border-radius: 0.75rem;
  padding: 1rem;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  transition: all 0.3s ease;
}

.area-name {
  font-size: 0.9rem;
  font-weight: 600;
  color: #fff;
  margin-bottom: 0.5rem;
  text-align: center;
}

.area-icon {
  font-size: 1.5rem;
  margin-bottom: 0.5rem;
}

.area-desc {
  font-size: 0.7rem;
  color: #94a3b8;
  text-align: center;
  opacity: 0.8;
}

/* 区域位置调整 */
.exam-hall {
  left: 5%;
  top: 50%;
  width: 30%;
  transform: translateY(-50%);
}

.stairs {
  right: 5%;
  top: 0%;
  width: 25%;
}

.office {
  right: 5%;
  bottom: 0%;
  width: 25%;
}

/* 区域激活状态 */
.map-area:has(.marker) {
  background: rgba(51, 65, 85, 0.8);
  border-color: rgba(148, 163, 184, 0.4);
  box-shadow: 0 0 15px rgba(148, 163, 184, 0.2);
}

.marker {
  position: absolute;
  transform: translate(-50%, -50%);
  z-index: 10;
}

.marker-dot {
  width: 12px;
  height: 12px;
  border-radius: 50%;
}

.marker-label {
  position: absolute;
  top: 100%;
  left: 50%;
  transform: translateX(-50%);
  margin-top: 0.5rem;
  font-size: 0.75rem;
  white-space: nowrap;
  background: rgba(0, 0, 0, 0.8);
  padding: 0.25rem 0.5rem;
  border-radius: 0.25rem;
  z-index: 11;
}

.map-legend {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
  padding: 0.75rem;
  background: rgba(51, 65, 85, 0.4);
  border-radius: 0.5rem;
  font-size: 0.8rem;
}

.legend-item {
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.legend-marker {
  width: 0.5rem;
  height: 0.5rem;
  border-radius: 50%;
}

/* 标记颜色 */
.player-marker .marker-dot,
.legend-marker.player {
  background: #4ade80;
  box-shadow: 0 0 0.75rem #4ade80;
}

.joey .marker-dot,
.legend-marker.joey {
  background: #ff69b4;
  box-shadow: 0 0 0.75rem #ff69b4;
}

.robert .marker-dot,
.legend-marker.robert {
  background: #ff5722;
  box-shadow: 0 0 0.75rem #ff5722;
}

/* 连接线样式 */
.corridors {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  z-index: 1;
}

.corridor-h {
  position: absolute;
  left: 35%;
  top: 50%;
  width: 40%;
  height: 4px;
  background: rgba(51, 65, 85, 0.5);
  transform: translateY(-50%);
}

.corridor-v {
  position: absolute;
  right: 25%;
  top: 20%;
  width: 4px;
  height: 60%;
  background: rgba(51, 65, 85, 0.5);
}

@keyframes pulse {
  0% { transform: scale(1); opacity: 0.8; }
  50% { transform: scale(1.5); opacity: 0; }
  100% { transform: scale(1); opacity: 0.8; }
}

@media (max-width: 768px) {
  .mini-map {
    width: 90vw;
    left: 5vw;
    right: 5vw;
  }
}

/* 改工具栏样式 */
.toolbar {
  position: fixed;
  right: 0;
  top: 50%;
  transform: translateY(-50%);
  background: rgba(15, 23, 42, 0.98);
  border-radius: 0.75rem 0 0 0.75rem;
  padding: 0.75rem;
  display: flex;
  flex-direction: column;
  gap: 0.75rem;
  z-index: 1000;
  border: 1px solid rgba(255, 255, 255, 0.1);
  border-right: none;
  transition: all 0.3s ease;
  backdrop-filter: blur(12px);
  font-family: 'Segoe UI', system-ui, sans-serif;
}

.toolbar.map-minimized {
  box-shadow: 0 0.5rem 2rem rgba(0, 0, 0, 0.4);
}

.toolbar-button {
  width: 3rem;
  height: 3rem;
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: 0.5rem;
  cursor: pointer;
  position: relative;
  background: rgba(51, 65, 85, 0.4);
  transition: all 0.2s ease;
  border: 1px solid rgba(255, 255, 255, 0.1);
}

.toolbar-button:hover {
  background: rgba(51, 65, 85, 0.6);
  border-color: rgba(255, 255, 255, 0.2);
  transform: translateX(-2px);
}

.button-icon {
  font-size: 1.5rem;
}

.button-tooltip {
  position: absolute;
  right: 100%;
  top: 50%;
  transform: translateY(-50%);
  background: rgba(15, 23, 42, 0.98);
  padding: 0.5rem 1rem;
  border-radius: 0.5rem;
  font-size: 0.9rem;
  white-space: nowrap;
  margin-right: 0.75rem;
  opacity: 0;
  visibility: hidden;
  transition: all 0.2s ease;
  border: 1px solid rgba(255, 255, 255, 0.1);
  color: #e2e8f0;
  font-weight: 500;
  letter-spacing: 0.05em;
  backdrop-filter: blur(12px);
  box-shadow: 0 0.25rem 1rem rgba(0, 0, 0, 0.2);
}

.toolbar-button:hover .button-tooltip {
  opacity: 1;
  visibility: visible;
  transform: translateY(-50%) translateX(-0.25rem);
}

/* 修改最小化按钮样式 */
.minimize-button {
  width: 2rem;
  height: 2rem;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  border-radius: 0.5rem;
  background: rgba(51, 65, 85, 0.4);
  transition: all 0.2s ease;
  margin-left: 0.75rem;
  border: 1px solid rgba(255, 255, 255, 0.1);
  font-family: 'Segoe UI', system-ui, sans-serif;
  font-size: 1.25rem;
  color: #e2e8f0;
}

.minimize-button:hover {
  background: rgba(51, 65, 85, 0.6);
  border-color: rgba(255, 255, 255, 0.2);
}

.map-header {
  display: flex;
  align-items: center;
}

/* 确保小地图的过渡动画平滑 */
.mini-map {
  transition: all 0.3s ease;
}
</style> 