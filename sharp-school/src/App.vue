<template>
  <el-config-provider namespace="ep">
    <router-view />
  </el-config-provider>
</template>

<script setup lang="ts">
import { ElConfigProvider } from 'element-plus'
</script>

<style>
html, body {
  margin: 0;
  padding: 0;
  height: 100vh;
  background-color: #1a1a1a;
  color: #fff;
}

#app {
  height: 100vh;
}
</style> 