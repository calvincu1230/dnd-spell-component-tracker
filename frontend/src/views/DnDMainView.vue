<template>
  <div class="max-w-6xl mx-auto p-6 bg-white">
    <!-- Campaign Header -->
    <div class="mb-8 bg-gradient-to-r from-purple-600 to-blue-600 text-white p-6 rounded-lg">
      <div class="flex justify-between items-start">
        <h1 class="text-3xl font-bold">{{ campaignData?.name || 'Derngerns ern Dergens' }}</h1>
        <div class="text-right text-sm opacity-90">
          <p v-if="campaignData?.description" class="mb-1">{{ campaignData.description }}</p>
          <p v-if="campaignData?.dmUsername">DM: {{ campaignData.dmUsername }}</p>
        </div>
      </div>
    </div>

    <!-- Character Selector -->
    <div class="mb-6" v-if="characterIds.length > 0">
      <label class="block text-sm font-medium text-gray-700 mb-2">
        Select Character:
      </label>
      <select 
        v-model="selectedCharacterId"
        class="block w-64 px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
      >
        <option v-for="id in characterIds" :key="id" :value="id">
          {{ characterData[id]?.name || `Character ${id}` }}
        </option>
      </select>
    </div>

    <!-- Character Display -->
    <div v-if="selectedCharacter">
      <!-- Character Name -->
      <h2 class="text-2xl font-bold text-gray-800 mb-6">{{ selectedCharacter.name }}</h2>

      <!-- Spells Table -->
      <div class="mb-8" v-if="selectedCharacter.spells && selectedCharacter.spells.length > 0">
        <h3 class="text-xl font-semibold text-gray-800 mb-4">Spells</h3>
        <div class="overflow-x-auto bg-white rounded-lg shadow">
          <table class="min-w-full divide-y divide-gray-200">
            <thead class="bg-gray-50">
              <tr>
                <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  Name
                </th>
                <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  Components Description
                </th>
                <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  Components Consumed
                </th>
                <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  Components Have Cost
                </th>
                <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  Focus Will Work
                </th>
              </tr>
            </thead>
            <tbody class="bg-white divide-y divide-gray-200">
              <tr v-for="(spell, index) in selectedCharacter.spells" :key="index" class="hover:bg-gray-50">
                <td class="px-6 py-4 whitespace-nowrap text-sm font-medium text-gray-900">
                  {{ spell.name }}
                </td>
                <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                  {{ spell.componentsDescription || '—' }}
                </td>
                <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                  <span :class="`px-2 py-1 rounded-full text-xs ${
                    spell.componentsAreConsumed 
                      ? 'bg-red-100 text-red-800' 
                      : 'bg-green-100 text-green-800'
                  }`">
                    {{ spell.componentsAreConsumed ? 'Yes' : 'No' }}
                  </span>
                </td>
                <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                  <span :class="`px-2 py-1 rounded-full text-xs ${
                    spell.componentsHaveCost 
                      ? 'bg-red-100 text-red-800' 
                      : 'bg-green-100 text-green-800'
                  }`">
                    {{ spell.componentsHaveCost ? 'Yes' : 'No' }}
                  </span>
                </td>
                <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                  <span :class="`px-2 py-1 rounded-full text-xs ${
                    spell.focusWillWork 
                      ? 'bg-green-100 text-green-800' 
                      : 'bg-red-100 text-red-800'
                  }`">
                    {{ spell.focusWillWork ? 'Yes' : 'No' }}
                  </span>
                </td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>

      <!-- Collapsible Sections -->
      <div class="space-y-4">
        <!-- Inventory -->
        <div class="bg-white rounded-lg shadow" v-if="selectedCharacter.inventory">
          <button
            @click="showInventory = !showInventory"
            class="w-full px-6 py-4 text-left flex items-center justify-between hover:bg-gray-50 rounded-lg transition-colors"
          >
            <h3 class="text-lg font-semibold text-gray-800">Inventory</h3>
            <svg class="w-5 h-5" :class="{ 'transform rotate-90': showCustomItems }" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7"></path>
            </svg>
          </button>
          <div v-show="showInventory" class="px-6 pb-4">
            <ul class="space-y-2">
              <li v-for="(quantity, item) in selectedCharacter.inventory" :key="item" 
                  class="flex justify-between items-center py-2 border-b border-gray-100 last:border-b-0">
                <span class="text-gray-800">{{ item }}</span>
                <span class="text-gray-600 bg-gray-100 px-2 py-1 rounded text-sm">
                  {{ quantity }}
                </span>
              </li>
            </ul>
          </div>
        </div>

        <!-- Custom Items -->
        <div class="bg-white rounded-lg shadow" v-if="selectedCharacter.custom_items">
          <button
            @click="showCustomItems = !showCustomItems"
            class="w-full px-6 py-4 text-left flex items-center justify-between hover:bg-gray-50 rounded-lg transition-colors"
          >
            <h3 class="text-lg font-semibold text-gray-800">Custom Items</h3>
            <svg class="w-5 h-5" :class="{ 'transform rotate-90': showCustomItems }" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7"></path>
            </svg>
          </button>
          <div v-show="showCustomItems" class="px-6 pb-4">
            <ul class="space-y-2">
              <li v-for="(value, item) in selectedCharacter.custom_items" :key="item" 
                  class="flex justify-between items-center py-2 border-b border-gray-100 last:border-b-0">
                <span class="text-gray-800">{{ item.replace(/_/g, ' ') }}</span>
                <span class="text-gray-600 bg-yellow-100 px-2 py-1 rounded text-sm">
                  {{ value }}
                </span>
              </li>
            </ul>
          </div>
        </div>

        <!-- Focus -->
        <div class="bg-white rounded-lg shadow" v-if="selectedCharacter.focus">
          <button
            @click="showFocus = !showFocus"
            class="w-full px-6 py-4 text-left flex items-center justify-between hover:bg-gray-50 rounded-lg transition-colors"
          >
            <h3 class="text-lg font-semibold text-gray-800">Focus</h3>
            <svg class="w-5 h-5" :class="{ 'transform rotate-90': showFocus }" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7"></path>
            </svg>
          </button>
          <div v-show="showFocus" class="px-6 pb-4 space-y-3">
            <div v-if="selectedCharacter.focus.name">
              <span class="font-medium text-gray-700">Name:</span>
              <span class="ml-2 text-gray-800">{{ selectedCharacter.focus.name }}</span>
            </div>
            <div v-if="selectedCharacter.focus.type">
              <span class="font-medium text-gray-700">Type:</span>
              <span class="ml-2 text-gray-800">{{ selectedCharacter.focus.type }}</span>
            </div>
            <div v-if="selectedCharacter.focus.subType">
              <span class="font-medium text-gray-700">Subtype:</span>
              <span class="ml-2 text-gray-800">{{ selectedCharacter.focus.subType }}</span>
            </div>
            <div v-if="selectedCharacter.focus.description">
              <span class="font-medium text-gray-700">Description:</span>
              <div class="mt-1 text-gray-800 text-sm leading-relaxed" v-html="selectedCharacter.focus.description">
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- No Character Selected -->
    <div v-else class="text-center text-gray-500 py-8">
      <p>No character data available. Click the button to load character data.</p>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, watch } from 'vue'

const props = defineProps({
  campaignData: Object,
  characterData: Object,
  getOneCharactersData: Function,
  getAllCharacterData: Function
})

// Reactive state
const showInventory = ref(false)
const showCustomItems = ref(false)
const showFocus = ref(false)
const selectedCharacterId = ref('')

// Computed properties
const characterIds = computed(() => {
  return props.characterData ? Object.keys(props.characterData) : []
})

const selectedCharacter = computed(() => {
  if (!props.characterData || !selectedCharacterId.value) return null
  return props.characterData[selectedCharacterId.value]
})

// Watch for character data changes and set first character as selected
watch(() => props.characterData, (newData) => {
  if (newData && Object.keys(newData).length > 0 && !selectedCharacterId.value) {
    selectedCharacterId.value = Object.keys(newData)[0]
  }
}, { immediate: true })
</script>

<style scoped>
/* Reset and base styles */
* {
  box-sizing: border-box;
}

/* Container */
.max-w-6xl {
  max-width: 72rem;
}

.mx-auto {
  margin-left: auto;
  margin-right: auto;
}

.p-6 {
  padding: 1.5rem;
}

.bg-white {
  background-color: #ffffff;
}

/* Campaign Header */
.mb-8 {
  margin-bottom: 2rem;
}

.bg-gradient-to-r {
  background-image: linear-gradient(to right, #9333ea, #2563eb);
}

.from-purple-600 {
  --tw-gradient-from: #9333ea;
}

.to-blue-600 {
  --tw-gradient-to: #2563eb;
}

.text-white {
  color: #ffffff;
}

.rounded-lg {
  border-radius: 0.5rem;
}

.flex {
  display: flex;
}

.justify-between {
  justify-content: space-between;
}

.items-start {
  align-items: flex-start;
}

.items-center {
  align-items: center;
}

.text-3xl {
  font-size: 1.875rem;
  line-height: 2.25rem;
}

.text-2xl {
  font-size: 1.5rem;
  line-height: 2rem;
}

.text-xl {
  font-size: 1.25rem;
  line-height: 1.75rem;
}

.text-lg {
  font-size: 1.125rem;
  line-height: 1.75rem;
}

.text-sm {
  font-size: 0.875rem;
  line-height: 1.25rem;
}

.text-xs {
  font-size: 0.75rem;
  line-height: 1rem;
}

.font-bold {
  font-weight: 700;
}

.font-semibold {
  font-weight: 600;
}

.font-medium {
  font-weight: 500;
}

.text-right {
  text-align: right;
}

.text-left {
  text-align: left;
}

.text-center {
  text-align: center;
}

.opacity-90 {
  opacity: 0.9;
}

/* Margins and Padding */
.mb-1 {
  margin-bottom: 0.25rem;
}

.mb-2 {
  margin-bottom: 0.5rem;
}

.mb-4 {
  margin-bottom: 1rem;
}

.mb-6 {
  margin-bottom: 1.5rem;
}

.mt-1 {
  margin-top: 0.25rem;
}

.ml-2 {
  margin-left: 0.5rem;
}

.px-2 {
  padding-left: 0.5rem;
  padding-right: 0.5rem;
}

.px-3 {
  padding-left: 0.75rem;
  padding-right: 0.75rem;
}

.px-6 {
  padding-left: 1.5rem;
  padding-right: 1.5rem;
}

.py-1 {
  padding-top: 0.25rem;
  padding-bottom: 0.25rem;
}

.py-2 {
  padding-top: 0.5rem;
  padding-bottom: 0.5rem;
}

.py-3 {
  padding-top: 0.75rem;
  padding-bottom: 0.75rem;
}

.py-4 {
  padding-top: 1rem;
  padding-bottom: 1rem;
}

.py-8 {
  padding-top: 2rem;
  padding-bottom: 2rem;
}

.pb-4 {
  padding-bottom: 1rem;
}

/* Colors */
.text-gray-500 {
  color: #6b7280;
}

.text-gray-600 {
  color: #4b5563;
}

.text-gray-700 {
  color: #374151;
}

.text-gray-800 {
  color: #1f2937;
}

.text-gray-900 {
  color: #111827;
}

.bg-gray-50 {
  background-color: #f9fafb;
}

.bg-gray-100 {
  background-color: #f3f4f6;
}

.border-gray-100 {
  border-color: #f3f4f6;
}

.border-gray-200 {
  border-color: #e5e7eb;
}

.border-gray-300 {
  border-color: #d1d5db;
}

.divide-gray-200 > * + * {
  border-top-color: #e5e7eb;
}

/* Badge Colors */
.bg-red-100 {
  background-color: #fee2e2;
}

.text-red-800 {
  color: #991b1b;
}

.bg-green-100 {
  background-color: #dcfce7;
}

.text-green-800 {
  color: #166534;
}

.bg-yellow-100 {
  background-color: #fef3c7;
}

/* Layout */
.block {
  display: block;
}

.w-5 {
  width: 1.25rem;
}

.h-5 {
  height: 1.25rem;
}

.w-64 {
  width: 16rem;
}

.w-full {
  width: 100%;
}

.min-w-full {
  min-width: 100%;
}

/* Form Elements */
.border {
  border-width: 1px;
}

.border-b {
  border-bottom-width: 1px;
}

.rounded {
  border-radius: 0.25rem;
}

.rounded-md {
  border-radius: 0.375rem;
}

.rounded-full {
  border-radius: 9999px;
}

/* Shadows */
.shadow {
  box-shadow: 0 1px 3px 0 rgba(0, 0, 0, 0.1), 0 1px 2px 0 rgba(0, 0, 0, 0.06);
}

.shadow-sm {
  box-shadow: 0 1px 2px 0 rgba(0, 0, 0, 0.05);
}

/* Table Styles */
.overflow-x-auto {
  overflow-x: auto;
}

.divide-y {
  border-top-width: 1px;
}

.divide-y > * + * {
  border-top-width: 1px;
}

.whitespace-nowrap {
  white-space: nowrap;
}

.uppercase {
  text-transform: uppercase;
}

.tracking-wider {
  letter-spacing: 0.05em;
}

/* Hover Effects */
.hover\:bg-gray-50:hover {
  background-color: #f9fafb;
}

/* Transitions */
.transition-colors {
  transition-property: background-color, border-color, color, fill, stroke;
  transition-timing-function: cubic-bezier(0.4, 0, 0.2, 1);
  transition-duration: 150ms;
}

.transition-transform {
  transition-property: transform;
  transition-timing-function: cubic-bezier(0.4, 0, 0.2, 1);
  transition-duration: 150ms;
}

/* Transform */
.transform {
  transform: translateX(var(--tw-translate-x, 0)) translateY(var(--tw-translate-y, 0)) rotate(var(--tw-rotate, 0deg)) skewX(var(--tw-skew-x, 0deg)) skewY(var(--tw-skew-y, 0deg)) scaleX(var(--tw-scale-x, 1)) scaleY(var(--tw-scale-y, 1));
}

.rotate-90 {
  --tw-rotate: 90deg;
}

/* Spacing */
.space-y-2 > * + * {
  margin-top: 0.5rem;
}

.space-y-3 > * + * {
  margin-top: 0.75rem;
}

.space-y-4 > * + * {
  margin-top: 1rem;
}

/* Focus States */
select:focus {
  outline: 2px solid transparent;
  outline-offset: 2px;
  border-color: #3b82f6;
  box-shadow: 0 0 0 2px #3b82f6;
}

button:focus {
  outline: 2px solid transparent;
  outline-offset: 2px;
}

/* List Styles */
li:last-child.border-b {
  border-bottom-width: 0;
}

.last\:border-b-0:last-child {
  border-bottom-width: 0;
}

/* Text */
.leading-relaxed {
  line-height: 1.625;
}

/* Tables */
table {
  border-collapse: collapse;
}

thead {
  background-color: #f9fafb;
}

tbody {
  background-color: #ffffff;
}

tr:hover {
  background-color: #f9fafb;
}

/* Custom component specific styles */
.character-display {
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', 'Roboto', 'Oxygen', 'Ubuntu', 'Cantarell', 'Fira Sans', 'Droid Sans', 'Helvetica Neue', sans-serif;
}

/* Button reset */
button {
  background: none;
  border: none;
  cursor: pointer;
  font: inherit;
}

/* Select styling */
select {
  appearance: none;
  background-image: url("data:image/svg+xml;charset=utf-8,%3csvg xmlns='http://www.w3.org/2000/svg' fill='none' viewBox='0 0 20 20'%3e%3cpath stroke='%236b7280' stroke-linecap='round' stroke-linejoin='round' stroke-width='1.5' d='M6 8l4 4 4-4'/%3e%3c/svg%3e");
  background-position: right 0.5rem center;
  background-repeat: no-repeat;
  background-size: 1.5em 1.5em;
  padding-right: 2.5rem;
}
</style>