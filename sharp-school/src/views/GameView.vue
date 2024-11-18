<template>
  <div class="game-container">
    <el-container>
      <el-aside width="300px">
        <GameStatus />
      </el-aside>
      <el-main>
        <GameDialog />
      </el-main>
      <el-aside width="300px">
        <CharacterPanel />
      </el-aside>
    </el-container>
  </div>
</template>

<script setup lang="ts">
import GameStatus from '../components/GameStatus.vue'
import GameDialog from '../components/GameDialog.vue'
import CharacterPanel from '../components/CharacterPanel.vue'
import { useGameStore } from '../stores/game'
import { onMounted } from 'vue'

const store = useGameStore()

onMounted(async () => {
  await store.fetchGameState()
})
</script>

<style scoped>
.game-container {
  min-height: 100vh;
  background-color: #1a1a1a;
  color: #fff;
}

.el-container {
  height: 100vh;
}
</style> 