import { defineStore } from 'pinia'
import axios from 'axios'

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
      loading: false
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
          const response = await axios.post('http://localhost:8000/api/game/action', {
            action: this.parseAction(input),
            parameters: {}
          })
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

    updateGameState(newState: any) {
      this.gameState.currentTime = newState.current_time
      this.gameState.location = newState.location
      this.gameState.phase = newState.phase
      this.gameState.cycleCount = newState.cycle_count
      this.gameState.inDialogue = newState.in_dialogue
      this.gameState.availableActions = newState.available_actions
      
      // 只添加新消息
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
      // 将用户输入转换为游戏动作
      input = input.toLowerCase().trim()
      
      // 直接匹配可用动作
      const exactMatch = this.gameState.availableActions.find(
        action => action.toLowerCase() === input
      )
      if (exactMatch) return exactMatch

      // 处理移动命令
      if (input.startsWith('go to ')) {
        const location = input.replace('go to ', '')
        const moveAction = `go_to_${location.replace(' ', '_')}`
        if (this.gameState.availableActions.includes(moveAction)) {
          return moveAction
        }
      }

      // 处理对话命令
      if (input.startsWith('talk to ')) {
        const npc = input.replace('talk to ', '')
        const talkAction = `talk_to_${npc.replace(' ', '_')}`
        if (this.gameState.availableActions.includes(talkAction)) {
          return talkAction
        }
      }

      // 默认返回原始输入
      return input
    }
  }
}) 