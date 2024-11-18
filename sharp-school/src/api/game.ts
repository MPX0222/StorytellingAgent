import axios from 'axios'
import type { GameState } from '../types/game'

const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000'

const api = axios.create({
  baseURL: API_URL,
  headers: {
    'Content-Type': 'application/json'
  }
})

export const getGameState = async (): Promise<GameState> => {
  const response = await api.get('/api/game/state')
  return response.data
}

export const processAction = async (action: { actionType: string }): Promise<{ next_state: GameState }> => {
  const response = await api.post('/api/game/action', action)
  return response.data
} 