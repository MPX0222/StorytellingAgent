<!-- <template>
  <div class="game-status">
    <el-card>
      <template #header>
        <div class="card-header">
          <h3>Game Status</h3>
        </div>
      </template>
      <div class="status-content">
        <p>Time: {{ gameState.currentTime }}</p>
        <p>Location: {{ gameState.location }}</p>
      </div>
    </el-card>
  </div>
</template> -->

<script setup lang="ts">
import { useGameStore } from '../stores/game'
import { storeToRefs } from 'pinia'

const store = useGameStore()
const { gameState } = storeToRefs(store)
</script>

<style scoped>
.game-status {
  padding: 1rem;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.status-content {
  font-size: 1.1rem;
}
</style> 