<template>
  <div class="terminal-interface">
    <!-- 游戏状态区域 -->
    <div class="status-bar">
      <div class="time">Time: {{ gameState.currentTime }}</div>
      <div class="location">Location: {{ gameState.location }}</div>
      <div v-if="gameState.cycleCount > 1" class="cycle">
        Cycle: {{ gameState.cycleCount }}
      </div>
    </div>

    <!-- 游戏内容区域 -->
    <div class="game-content" ref="gameContentRef">
      <div v-for="(msg, index) in gameState.messages" :key="index" class="message" :class="msg.type">
        <template v-if="msg.type === 'user'">
          <span class="prompt">> </span>{{ msg.text }}
        </template>
        <template v-else>
          {{ msg.text }}
        </template>
      </div>
      
      <!-- 加载状态显示 -->
      <div v-if="gameState.loading" class="loading">
        Processing...
      </div>
    </div>

    <!-- 可用动作按钮 -->
    <div class="action-buttons" v-if="gameState.availableActions?.length">
      <button 
        v-for="action in gameState.availableActions" 
        :key="action"
        @click="executeAction(action)"
        class="action-button"
        :disabled="gameState.loading"
      >
        {{ formatActionName(action) }}
      </button>
    </div>

    <!-- 命令输入区域 -->
    <div class="command-input">
      <div class="input-wrapper">
        <span class="prompt">> </span>
        <input
          v-model="userInput"
          @keyup.enter="handleInput"
          type="text"
          :placeholder="'Type anything you want to do...'"
          class="command-input-field"
          ref="inputRef"
          :disabled="gameState.loading"
        />
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, watch } from 'vue'
import { useGameStore } from '../stores/game'
import { storeToRefs } from 'pinia'

const store = useGameStore()
const { gameState } = storeToRefs(store)
const userInput = ref('')
const gameContentRef = ref<HTMLElement | null>(null)
const inputRef = ref<HTMLInputElement | null>(null)

// 格式化动作名称
const formatActionName = (action: string): string => {
  return action
    .split('_')
    .map(word => word.charAt(0).toUpperCase() + word.slice(1))
    .join(' ')
}

// 执行动作按钮
const executeAction = async (action: string) => {
  if (gameState.value.loading) return
  await store.performAction(action)
  scrollToBottom()
}

// 处理用户输入
const handleInput = async () => {
  if (!userInput.value.trim() || gameState.value.loading) return
  
  await store.performAction(userInput.value)
  userInput.value = ''
  scrollToBottom()
  
  // 重新聚焦输入框
  if (inputRef.value) {
    inputRef.value.focus()
  }
}

// 自动滚动到底部
const scrollToBottom = () => {
  setTimeout(() => {
    if (gameContentRef.value) {
      gameContentRef.value.scrollTop = gameContentRef.value.scrollHeight
    }
  }, 100)
}

// 监听消息变化，自动滚动
watch(() => gameState.value.messages, () => {
  scrollToBottom()
}, { deep: true })

// 初始化
onMounted(async () => {
  await store.fetchGameState()
  if (inputRef.value) {
    inputRef.value.focus()
  }
})
</script>

<style scoped>
.terminal-interface {
  height: 100vh;
  background-color: #1a1a1a;
  color: #fff;
  font-family: 'Courier New', monospace;
  padding: 1rem;
  display: flex;
  flex-direction: column;
}

.status-bar {
  display: flex;
  justify-content: space-between;
  padding: 0.5rem;
  background-color: #2d2d2d;
  margin-bottom: 1rem;
  border-radius: 4px;
}

.game-content {
  flex-grow: 1;
  overflow-y: auto;
  padding: 1rem;
  background-color: #2d2d2d;
  margin-bottom: 1rem;
  border-radius: 4px;
  min-height: 300px;
}

.message {
  margin: 0.5rem 0;
  white-space: pre-wrap;
  line-height: 1.5;
  padding: 0.5rem;
  border-radius: 4px;
}

.message.system {
  color: #d4d4d4;
  font-style: italic;
  background-color: rgba(255, 255, 255, 0.05);
}

.message.agent {
  color: #90caf9;
  background-color: rgba(144, 202, 249, 0.1);
  border-left: 3px solid #90caf9;
}

.message.user {
  color: #69f0ae;
  background-color: rgba(105, 240, 174, 0.1);
  border-left: 3px solid #69f0ae;
}

.message.background {
  color: #ffd700;
  background-color: rgba(255, 215, 0, 0.1);
  font-style: italic;
}

.message.narration {
  color: #ff9e80;
  background-color: rgba(255, 158, 128, 0.1);
  font-style: italic;
  text-align: center;
}

.prompt {
  color: #90caf9;
  margin-right: 0.5rem;
}

.action-buttons {
  display: flex;
  flex-wrap: wrap;
  gap: 0.5rem;
  padding: 0.5rem;
  background-color: #2d2d2d;
  margin-bottom: 1rem;
  border-radius: 4px;
}

.action-button {
  background-color: #4a4a4a;
  color: #90caf9;
  border: 1px solid #90caf9;
  border-radius: 4px;
  padding: 0.5rem 1rem;
  cursor: pointer;
  font-family: 'Courier New', monospace;
  transition: all 0.3s ease;
}

.action-button:hover {
  background-color: #90caf9;
  color: #1a1a1a;
}

.action-button:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.command-input {
  background-color: #2d2d2d;
  padding: 0.5rem;
  border-radius: 4px;
}

.input-wrapper {
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.command-input-field {
  flex-grow: 1;
  background: transparent;
  border: none;
  color: #fff;
  font-family: 'Courier New', monospace;
  font-size: 1rem;
  padding: 0.5rem;
}

.command-input-field:focus {
  outline: none;
}

.command-input-field:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.loading {
  color: #90caf9;
  margin: 1rem 0;
  font-style: italic;
}
</style> 