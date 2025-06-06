<!-- ThemeProvider.vue -->
<template>
  <div :class="[themeClass]">
    <slot />
  </div>
</template>

<script setup>
import { ref, onMounted, watch, provide } from 'vue'

const isDark = ref(true) // Default to dark mode
const themeClass = ref('theme-dark')

// Provide theme state to children
provide('theme', {
  isDark,
  toggleTheme: () => {
    isDark.value = !isDark.value
  }
})

// Update theme class when isDark changes
watch(isDark, (newValue) => {
  themeClass.value = newValue ? 'theme-dark' : 'theme-light'
  // Save to localStorage
  localStorage.setItem('theme', newValue ? 'dark' : 'light')
  // Update document class for global theming
  document.documentElement.className = themeClass.value
}, { immediate: true })

// Load theme from localStorage on mount
onMounted(() => {
  const savedTheme = localStorage.getItem('theme')
  if (savedTheme) {
    isDark.value = savedTheme === 'dark'
  }
})
</script>

<style>
/* CSS Custom Properties for theming */
:root.theme-light {
  --bg-primary: #ffffff;
  --bg-secondary: #f9fafb;
  --bg-tertiary: #f3f4f6;
  --bg-accent: #e5e7eb;
  --bg-hover: #f9fafb;
  --bg-gradient-from: #9333ea;
  --bg-gradient-to: #2563eb;
  
  --text-primary: #111827;
  --text-secondary: #374151;
  --text-tertiary: #4b5563;
  --text-muted: #6b7280;
  --text-inverse: #ffffff;
  
  --border-primary: #e5e7eb;
  --border-secondary: #d1d5db;
  --border-tertiary: #f3f4f6;
  
  --shadow-sm: 0 1px 2px 0 rgba(0, 0, 0, 0.05);
  --shadow-md: 0 1px 3px 0 rgba(0, 0, 0, 0.1), 0 1px 2px 0 rgba(0, 0, 0, 0.06);
  --shadow-lg: 0 10px 25px rgba(0, 0, 0, 0.25);
}

:root.theme-dark {
  --bg-primary: #1f2937;
  --bg-secondary: #374151;
  --bg-tertiary: #4b5563;
  --bg-accent: #6b7280;
  --bg-hover: #374151;
  --bg-gradient-from: #9333ea;
  --bg-gradient-to: #2563eb;
  
  --text-primary: #f9fafb;
  --text-secondary: #e5e7eb;
  --text-tertiary: #d1d5db;
  --text-muted: #9ca3af;
  --text-inverse: #111827;
  
  --border-primary: #4b5563;
  --border-secondary: #6b7280;
  --border-tertiary: #374151;
  
  --shadow-sm: 0 1px 2px 0 rgba(0, 0, 0, 0.3);
  --shadow-md: 0 1px 3px 0 rgba(0, 0, 0, 0.4), 0 1px 2px 0 rgba(0, 0, 0, 0.3);
  --shadow-lg: 0 10px 25px rgba(0, 0, 0, 0.5);
}

/* Global theme styles */
.theme-light,
.theme-dark {
  background-color: var(--bg-primary);
  color: var(--text-primary);
  transition: background-color 0.2s ease, color 0.2s ease;
}
</style>