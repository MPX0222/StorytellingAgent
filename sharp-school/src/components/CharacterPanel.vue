<template>
  <div class="character-panel">
    <!-- <el-card>
      <template #header>
        <div class="card-header">
          <h3>Characters</h3>
        </div>
      </template>
      <div class="character-buttons">
        <el-button @click="showCharacterInfo('joey')" type="info" plain>Joey</el-button>
        <el-button @click="showCharacterInfo('robert')" type="info" plain>Robert</el-button>
      </div>
    </el-card> -->

    <el-dialog
      v-model="dialogVisible"
      :title="currentCharacter?.name || ''"
      width="50%"
    >
      <template v-if="currentCharacter">
        <p><strong>Age:</strong> {{ currentCharacter.age }}</p>
        <p>{{ currentCharacter.description }}</p>
      </template>
    </el-dialog>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import type { Character } from '@/types/game'

const dialogVisible = ref(false)
const currentCharacter = ref<Character | null>(null)

const characters: Record<string, Character> = {
  joey: {
    name: 'Joey (朱一)',
    age: 24,
    description: '来自劳工阶级家庭的学生，正在经历巨大的压力和绝望。'
  },
  robert: {
    name: 'Robert (罗勃特)',
    age: 48,
    description: 'Sharp School的校长，维护精英阶级统治的守门人。'
  }
}

const showCharacterInfo = (characterId: string) => {
  currentCharacter.value = characters[characterId]
  dialogVisible.value = true
}
</script>

<style scoped>
.character-panel {
  padding: 1rem;
}

.character-buttons {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}
</style> 