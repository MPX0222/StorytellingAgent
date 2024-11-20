import { defineStore } from 'pinia'
import axios from 'axios'
import { ElMessageBox } from 'element-plus'

interface GameState {
  currentTime: string
  location: string
  phase: string
  cycleCount: number
  inDialogue: boolean
  availableActions: string[]
  messages: Array<{
    text: string
    type: string
  }>
  loading: boolean
  playerLocation: string
  agents: Array<{
    name: string
    location: string
  }>
}

export const useGameStore = defineStore('game', {
  state: (): { gameState: GameState } => ({
    gameState: {
      currentTime: '',
      location: '',
      phase: '',
      cycleCount: 1,
      inDialogue: false,
      availableActions: [],
      messages: [],
      loading: false,
      playerLocation: 'exam_hall',
      agents: [
        { name: 'Joey', location: 'corridor' },
        { name: 'Robert', location: 'corridor' }
      ]
    }
  }),

  actions: {
    async fetchGameState() {
      try {
        const response = await axios.post('http://localhost:8000/api/game/start')
        this.updateGameState(response.data)
      } catch (error) {
        console.error('Failed to fetch game state:', error)
        this.gameState.messages.push({
          text: 'Error: Failed to connect to game server',
          type: 'system'
        })
      }
    },

    async performAction(input: string) {
      this.gameState.loading = true
      try {
        // 记录用户输入
        this.gameState.messages.push({
          text: input,
          type: 'user'
        })

        // 处理对话
        if (this.gameState.inDialogue) {
          const response = await axios.post('http://localhost:8000/api/dialogue/respond', {
            message: input,
            parameters: {}
          })
          this.updateGameState(response.data.game_state)
          if (response.data.response) {
            this.gameState.messages.push({
              text: response.data.response,
              type: 'agent'
            })
          }
        } 
        // 处理游戏动作
        else {
          const action = this.parseAction(input)
          const response = await axios.post('http://localhost:8000/api/game/action', {
            action: action,
            parameters: {}
          })
          
          // 立即更新位置（不等待服务器响应）
          if (action.startsWith('go_to_')) {
            const location = action.replace('go_to_', '').replace('_', '')
            this.updatePlayerLocation(location)
          }
          
          this.updateGameState(response.data)
        }
      } catch (error) {
        console.error('Failed to perform action:', error)
        this.gameState.messages.push({
          text: 'Error: Failed to process action',
          type: 'system'
        })
      } finally {
        this.gameState.loading = false
      }
    },

    // 新增：直接更新玩家位置
    updatePlayerLocation(location: string) {
      this.gameState.playerLocation = location
      this.gameState.location = location // 同时更新游戏状态的位置
    },

    updateGameState(newState: any) {
      // 更新时间
      this.gameState.currentTime = newState.current_time || this.gameState.currentTime
      
      // 检查是否需要重置时间循环
      const [hours, minutes] = this.gameState.currentTime.split(':').map(Number)
      if (hours >= 9 && minutes >= 5) {
        this.resetGameState()
        return
      }

      // 其他状态更新保持不变...
      this.gameState.phase = newState.phase || this.gameState.phase
      this.gameState.cycleCount = newState.cycle_count || this.gameState.cycleCount
      this.gameState.inDialogue = newState.in_dialogue || false
      
      // 更新位置信息
      if (newState.player_location) {
        this.gameState.playerLocation = newState.player_location
      }
      if (newState.location) {
        this.gameState.location = newState.location
        this.gameState.playerLocation = newState.location // 确保两个位置同步
      }
      
      // 更新NPC位置
      if (newState.agents) {
        this.gameState.agents = newState.agents.map((agent: any) => ({
          name: agent.name,
          location: agent.location
        }))
      }
      
      // 更新可用动作
      if (newState.available_actions) {
        this.gameState.availableActions = newState.available_actions
      }
      
      // 更新消息
      if (newState.messages && Array.isArray(newState.messages)) {
        const currentMessages = this.gameState.messages.map(m => m.text)
        newState.messages.forEach((msg: any) => {
          if (!currentMessages.includes(msg.text)) {
            this.gameState.messages.push(msg)
          }
        })
      }
    },

    parseAction(input: string): string {
      input = input.toLowerCase().trim()
      
      // 处理移动命令
      if (input.startsWith('go to ')) {
        const location = input.replace('go to ', '')
        return `go_to_${location.replace(' ', '_')}`
      }

      // 处理对话命令
      if (input.startsWith('talk to ')) {
        const npc = input.replace('talk to ', '')
        return `talk_to_${npc.replace(' ', '_')}`
      }

      // 直接匹配可用动作
      const exactMatch = this.gameState.availableActions.find(
        action => action.toLowerCase() === input
      )
      if (exactMatch) return exactMatch

      // 默认返回原始输入
      return input
    },

    // 添加重置状态的方法
    resetGameState() {
      this.gameState.currentTime = '09:00'
      this.gameState.playerLocation = 'exam_hall'
      this.gameState.location = 'exam_hall'
      this.gameState.agents = [
        { name: 'Joey', location: 'corridor' },
        { name: 'Robert', location: 'corridor' }
      ]
      this.gameState.cycleCount += 1
      this.gameState.inDialogue = false
      
      // 清空之前的消息，只保留新循环开始的提示
      this.gameState.messages = [{
        text: `Time Loop ${this.gameState.cycleCount} Started`,
        type: 'system'
      }]
      
      // 重新获取游戏状态
      this.fetchGameState()
    }
  }
}) 