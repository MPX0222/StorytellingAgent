<template>
  <div class="game-container">
    <!-- 游戏标题和背景介绍 -->
    <div class="game-header">
      <h1 class="game-title">Sharp School: The Elite Plan</h1>
      <div class="game-subtitle">A Time Loop Mystery</div>
      <p class="game-intro">
        In a prestigious school where exams determine everything, 
        you find yourself caught in a mysterious time loop. 
        Can you uncover the truth and save a fellow student before it's too late?
      </p>
    </div>

    <!-- 消息类型说明 -->
    <div class="style-guide">
      <div class="guide-title">Message Types:</div>
      <div class="guide-items">
        <div class="guide-item">
          <div class="message system">System Message</div>
          <span>Game status and notifications</span>
        </div>
        <div class="guide-item">
          <div class="message action">Character Action</div>
          <span>Character's physical actions and expressions</span>
        </div>
        <div class="guide-item">
          <div class="message agent">Character Dialogue</div>
          <span>Direct speech from characters</span>
        </div>
        <div class="guide-item">
          <div class="message background">Background</div>
          <span>Scene descriptions and environment</span>
        </div>
        <div class="guide-item">
          <div class="message narration">Narration</div>
          <span>Important story events and transitions</span>
        </div>
      </div>
    </div>

    <!-- 主游戏界面 -->
    <div class="terminal-interface">
      <!-- 游戏状态区域 -->
      <div class="status-bar">
        <div class="time">Time: {{ gameState.currentTime }}</div>
        <div class="location">Location: {{ formatLocation(gameState.location) }}</div>
        <div v-if="gameState.cycleCount > 1" class="cycle">
          Time Loop: #{{ gameState.cycleCount }}
        </div>
      </div>

      <!-- 角色状态区域 -->
      <div class="characters-panel">
        <h2>Characters</h2>
        <div class="character-list">
          <div class="character-item" v-if="hasMetJoey">
            <div class="character-name">Joey</div>
            <div class="character-status">
              <div class="status-icon troubled"></div>
              <span>Troubled Student</span>
            </div>
          </div>
          <div class="character-item" v-if="hasMetRobert">
            <div class="character-name">Robert</div>
            <div class="character-status">
              <div class="status-icon authority"></div>
              <span>School Principal</span>
            </div>
          </div>
        </div>
      </div>

      <!-- 游戏内容区域 -->
      <div class="game-content" ref="gameContentRef">
        <div v-for="(msg, index) in gameState.messages" :key="index" 
             class="message" :class="[msg.type, {'with-speaker': msg.type === 'agent'}]">
          <template v-if="msg.type === 'user'">
            <span class="prompt">> </span>{{ msg.text }}
          </template>
          <template v-else-if="msg.type === 'agent'">
            <div class="speaker-name">{{ msg.speaker }}</div>
            <div class="dialogue-content">{{ msg.text }}</div>
          </template>
          <template v-else-if="msg.type === 'action'">
            <div class="action-content">
              <i>{{ msg.text }}</i>
            </div>
          </template>
          <template v-else>
            {{ msg.text }}
          </template>
        </div>
        
        <!-- 加载状态显示 -->
        <div v-if="gameState.loading" class="loading">
          <div class="loading-dots">
            <span></span><span></span><span></span>
          </div>
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

    <!-- 游戏说明 -->
    <div class="game-footer">
      <div class="footer-content">
        <div class="footer-section">
          <h3>How to Play</h3>
          <div class="instruction-grid">
            <div class="instruction-item">
              <div class="instruction-icon">⌨️</div>
              <div class="instruction-text">
                <h4>Natural Input</h4>
                <p>Use the command line to interact naturally with the game world</p>
              </div>
            </div>
            <div class="instruction-item">
              <div class="instruction-icon">🗣️</div>
              <div class="instruction-text">
                <h4>Character Interaction</h4>
                <p>Talk to characters to uncover the mystery and build trust</p>
              </div>
            </div>
            <div class="instruction-item">
              <div class="instruction-icon">⏰</div>
              <div class="instruction-text">
                <h4>Time Management</h4>
                <p>Pay attention to time - every minute counts in this loop</p>
              </div>
            </div>
            <div class="instruction-item">
              <div class="instruction-icon">🔄</div>
              <div class="instruction-text">
                <h4>Learn & Adapt</h4>
                <p>Use knowledge from previous loops to change the outcome</p>
              </div>
            </div>
          </div>
        </div>
        
        <div class="footer-divider"></div>
        
        <div class="footer-section">
          <div class="quick-tips">
            <h3>Quick Tips</h3>
            <ul>
              <li>
                <span class="tip-highlight">Actions:</span> 
                Click buttons or type commands like "go to hallway", "talk to Joey"
              </li>
              <li>
                <span class="tip-highlight">Dialogue:</span> 
                Express yourself naturally in conversations
              </li>
              <li>
                <span class="tip-highlight">Exploration:</span> 
                Use "look around" to observe your surroundings
              </li>
            </ul>
          </div>
        </div>
        
        <div class="footer-note">
          <div class="note-icon">💡</div>
          <p>Remember: Your choices matter, and time is of the essence. Each loop is a new chance to make things right.</p>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, watch, computed } from 'vue'
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

// 格式化位置名称
const formatLocation = (location: string): string => {
  return location
    .split('_')
    .map(word => word.charAt(0).toUpperCase() + word.slice(1))
    .join(' ')
}

// 判断是否遇到过角色
const hasMetJoey = computed(() => {
  return gameState.value.messages.some(msg => 
    msg.speaker === 'Joey' || msg.text.includes('Joey')
  )
})

const hasMetRobert = computed(() => {
  return gameState.value.messages.some(msg => 
    msg.speaker === 'Robert' || msg.text.includes('Robert')
  )
})
</script>

<style scoped>
.game-container {
  min-height: 100vh;
  background: linear-gradient(to bottom, #1a1a1a, #2d2d2d);
  color: #fff;
  font-family: 'Courier New', monospace;
  padding: 2rem;
  display: flex;
  flex-direction: column;
  gap: 2rem;
}

.game-header {
  text-align: center;
  padding: 2rem;
  background-color: rgba(0, 0, 0, 0.3);
  border-radius: 8px;
  border: 1px solid #90caf9;
}

.game-title {
  font-size: 2.5rem;
  color: #90caf9;
  margin: 0;
  text-shadow: 0 0 10px rgba(144, 202, 249, 0.5);
}

.game-subtitle {
  font-size: 1.2rem;
  color: #b39ddb;
  margin: 0.5rem 0;
}

.game-intro {
  max-width: 800px;
  margin: 1rem auto;
  color: #d4d4d4;
  line-height: 1.6;
}

.style-guide {
  background-color: rgba(0, 0, 0, 0.3);
  padding: 1.5rem;
  border-radius: 8px;
  border: 1px solid #4a4a4a;
}

.guide-title {
  color: #fff;
  font-weight: bold;
  margin-bottom: 0.5rem;
}

.guide-items {
  display: flex;
  flex-wrap: wrap;
  gap: 1rem;
}

.guide-item {
  flex: 1;
  min-width: 200px;
  display: flex;
  flex-direction: column;
  gap: 0.25rem;
}

.guide-item span {
  font-size: 0.8rem;
  color: #888;
}

.guide-item .message {
  padding: 0.25rem 0.5rem;
  margin: 0;
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
  padding: 0.75rem;
  border-radius: 4px;
  line-height: 1.5;
}

.message.with-speaker {
  display: flex;
  flex-direction: column;
}

.speaker-name {
  font-weight: bold;
  margin-bottom: 0.25rem;
  color: #90caf9;
}

.message.system {
  color: #d4d4d4;
  font-style: italic;
  background-color: rgba(255, 255, 255, 0.05);
  border-left: 3px solid #d4d4d4;
}

.message.agent {
  color: #90caf9;
  background-color: rgba(144, 202, 249, 0.1);
  border-left: 3px solid #90caf9;
}

.message.action {
  color: #b39ddb;
  background-color: rgba(179, 157, 219, 0.1);
  border-left: 3px solid #b39ddb;
  font-style: italic;
}

.message.user {
  color: #69f0ae;
  background-color: rgba(105, 240, 174, 0.1);
  border-left: 3px solid #69f0ae;
}

.message.background {
  color: #ffd700;
  background-color: rgba(255, 215, 0, 0.1);
  border-left: 3px solid #ffd700;
  font-style: italic;
}

.message.narration {
  color: #ff9e80;
  background-color: rgba(255, 158, 128, 0.1);
  border-left: 3px solid #ff9e80;
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

.game-footer {
  background-color: rgba(0, 0, 0, 0.3);
  padding: 2rem;
  border-radius: 8px;
  border: 1px solid #4a4a4a;
  margin-top: 2rem;
}

.footer-content {
  max-width: 1200px;
  margin: 0 auto;
}

.footer-section {
  margin-bottom: 2rem;
}

.footer-section h3 {
  color: #90caf9;
  margin: 0 0 1.5rem 0;
  font-size: 1.4rem;
  text-transform: uppercase;
  letter-spacing: 2px;
  text-align: center;
}

.instruction-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 1.5rem;
  margin-bottom: 2rem;
}

.instruction-item {
  background-color: rgba(0, 0, 0, 0.2);
  padding: 1.5rem;
  border-radius: 8px;
  border: 1px solid #666;
  display: flex;
  align-items: flex-start;
  gap: 1rem;
  transition: transform 0.3s ease, box-shadow 0.3s ease;
}

.instruction-item:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(144, 202, 249, 0.1);
}

.instruction-icon {
  font-size: 2rem;
  min-width: 40px;
  text-align: center;
}

.instruction-text h4 {
  color: #90caf9;
  margin: 0 0 0.5rem 0;
  font-size: 1.1rem;
}

.instruction-text p {
  color: #d4d4d4;
  margin: 0;
  font-size: 0.9rem;
  line-height: 1.4;
}

.footer-divider {
  height: 1px;
  background: linear-gradient(to right, transparent, #4a4a4a, transparent);
  margin: 2rem 0;
}

.quick-tips {
  background-color: rgba(0, 0, 0, 0.2);
  padding: 1.5rem;
  border-radius: 8px;
  border: 1px solid #666;
}

.quick-tips ul {
  list-style: none;
  padding: 0;
  margin: 0;
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
  gap: 1rem;
}

.quick-tips li {
  color: #d4d4d4;
  line-height: 1.6;
  padding: 0.5rem;
  background-color: rgba(0, 0, 0, 0.1);
  border-radius: 4px;
  transition: background-color 0.3s ease;
}

.quick-tips li:hover {
  background-color: rgba(144, 202, 249, 0.1);
}

.tip-highlight {
  color: #90caf9;
  font-weight: bold;
  margin-right: 0.5rem;
}

.footer-note {
  margin-top: 2rem;
  padding: 1rem;
  background-color: rgba(179, 157, 219, 0.1);
  border-radius: 8px;
  border: 1px solid #b39ddb;
  display: flex;
  align-items: center;
  gap: 1rem;
}

.note-icon {
  font-size: 1.5rem;
}

.footer-note p {
  color: #b39ddb;
  font-style: italic;
  margin: 0;
  line-height: 1.4;
}

.loading-dots {
  display: flex;
  justify-content: center;
  gap: 0.5rem;
}

.loading-dots span {
  width: 8px;
  height: 8px;
  background-color: #90caf9;
  border-radius: 50%;
  animation: loading 1.4s infinite ease-in-out both;
}

.loading-dots span:nth-child(1) { animation-delay: -0.32s; }
.loading-dots span:nth-child(2) { animation-delay: -0.16s; }

@keyframes loading {
  0%, 80%, 100% { transform: scale(0); }
  40% { transform: scale(1); }
}

.characters-panel {
  background-color: rgba(0, 0, 0, 0.3);
  padding: 1rem;
  margin: 1rem 0;
  border-radius: 8px;
  border: 1px solid #4a4a4a;
}

.characters-panel h2 {
  color: #90caf9;
  margin: 0 0 1rem 0;
  font-size: 1.2rem;
  text-transform: uppercase;
  letter-spacing: 2px;
}

.character-list {
  display: flex;
  gap: 1rem;
  flex-wrap: wrap;
}

.character-item {
  background-color: rgba(0, 0, 0, 0.2);
  padding: 0.75rem;
  border-radius: 4px;
  border: 1px solid #666;
  min-width: 200px;
}

.character-name {
  color: #fff;
  font-weight: bold;
  margin-bottom: 0.5rem;
}

.character-status {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  color: #888;
  font-size: 0.9rem;
}

.status-icon {
  width: 8px;
  height: 8px;
  border-radius: 50%;
}

.status-icon.troubled {
  background-color: #ff9e80;
  box-shadow: 0 0 5px #ff9e80;
}

.status-icon.authority {
  background-color: #90caf9;
  box-shadow: 0 0 5px #90caf9;
}
</style> 