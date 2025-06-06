<!-- ThemeToggleButton.vue -->
<template>
    <button
        @click="toggleTheme"
        class="theme-toggle-btn"
        :title="isDark ? 'Switch to light mode' : 'Switch to dark mode'"
    >
        <!-- Sun icon for light mode -->
        <svg
            v-if="!isDark"
            xmlns="http://www.w3.org/2000/svg"
            width="20"
            height="20"
            viewBox="0 0 24 24"
            fill="none"
            stroke="currentColor"
            stroke-width="2"
            stroke-linecap="round"
            stroke-linejoin="round"
        >
            <circle cx="12" cy="12" r="5" />
            <line x1="12" y1="1" x2="12" y2="3" />
            <line x1="12" y1="21" x2="12" y2="23" />
            <line x1="4.22" y1="4.22" x2="5.64" y2="5.64" />
            <line x1="18.36" y1="18.36" x2="19.78" y2="19.78" />
            <line x1="1" y1="12" x2="3" y2="12" />
            <line x1="21" y1="12" x2="23" y2="12" />
            <line x1="4.22" y1="19.78" x2="5.64" y2="18.36" />
            <line x1="18.36" y1="5.64" x2="19.78" y2="4.22" />
        </svg>

        <!-- Moon icon for dark mode -->
        <svg
            v-else
            xmlns="http://www.w3.org/2000/svg"
            width="20"
            height="20"
            viewBox="0 0 24 24"
            fill="none"
            stroke="currentColor"
            stroke-width="2"
            stroke-linecap="round"
            stroke-linejoin="round"
        >
            <path d="M21 12.79A9 9 0 1 1 11.21 3 7 7 0 0 0 21 12.79z" />
        </svg>
    </button>
</template>

<script setup>
import { inject } from 'vue'

// Inject theme context from ThemeProvider
const theme = inject('theme')
const { isDark, toggleTheme } = theme
</script>

<style scoped>
.theme-toggle-btn {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 2.5rem;
  height: 2.5rem;
  background-color: var(--bg-secondary);
  color: var(--text-primary);
  border: 1px solid var(--border-primary);
  border-radius: 0.5rem;
  cursor: pointer;
  transition: all 0.2s ease;
  box-shadow: var(--shadow-sm);
}

.theme-toggle-btn:hover {
  background-color: var(--bg-hover);
  transform: scale(1.05);
  box-shadow: var(--shadow-md);
}

.theme-toggle-btn:focus {
  outline: 2px solid var(--bg-gradient-to);
  outline-offset: 2px;
}

.theme-toggle-btn:active {
  transform: scale(0.95);
}

.theme-toggle-btn svg {
  transition: transform 0.2s ease;
}

.theme-toggle-btn:hover svg {
  transform: rotate(15deg);
}
</style>
