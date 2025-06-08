<template>
  <div class="max-w-6xl mx-auto p-6 themed-bg">
    <!-- Theme Toggle Button (fixed position) -->
    <div class="theme-toggle-container">
      <ThemeToggleButton />
    </div>

    <!-- Campaign Header -->
    <div class="mb-8 bg-gradient-to-r from-purple-600 to-blue-600 text-white p-6 rounded-lg">
      <div class="flex justify-between items-start">
        <h1 class="text-3xl font-bold">{{ selectedCampaign?.name || 'Derngerns ern Dergens' }}</h1>
        <div class="text-right text-sm opacity-90">
          <p v-if="selectedCampaign?.description" class="mb-1">{{ selectedCampaign.description }}</p>
          <p v-if="selectedCampaign?.dmUsername">DM: {{ selectedCampaign.dmUsername }}</p>
        </div>
      </div>
    </div>
    
    <!-- Campaign & Character Selectors -->
    <div class="mb-6 button-container" v-if="campaignData && Object.keys(campaignData).length > 0">
      <ul class="button-list">
        <!-- Campaign Selector -->
        <li>
          <label class="block text-sm font-medium themed-text-secondary mb-2">
            Select Campaign:
          </label>
          <select 
            v-model="selectedCampaignId"
            class="themed-select block w-64 px-3 py-2 border rounded-md shadow-sm focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
          >
          <option key="all" value="all">All Campaigns</option>
          <option v-for="id in computedCampaignIds" :key="id" :value="id">
            {{ campaignData[id].name }}
          </option>
        </select>
        </li>
        <!-- Character Selector -->
        <li>
          <label class="block text-sm font-medium themed-text-secondary mb-2">
            Select Character:
          </label>
          <select 
            v-model="selectedCharacterId"
            class="themed-select block w-64 px-3 py-2 border rounded-md shadow-sm focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
          >
            <option value="-" disabled selected>Select an item...</option>
            <option v-for="id in computedFilteredCharacterIds" :key="id" :value="id">
              {{ characterData[id].name }}
            </option>
          </select>
        </li>
        <li>
          <GenericButton
            :onClick="() => getAllCharacterData(computedAllCharacterIds, true)"
            text="Update All Characters"
          />
        </li>
        <li>
          <GenericButton
            :onClick="() => updateCurrentCharactersData(selectedCharacterId, true)"
            text="Update Current Character"
          />
        </li>
        <li>
          <GenericButton
            :onClick="showDeleteAllConfirmation"
            text="Delete All Data"
            variant="danger"
          />
        </li>
      </ul>
    </div>

    <!-- Character ID Input Section - Only show when no data is available -->
    <div class="text-center text-gray-500 py-8" v-else>
        <CharacterIdInput
          :getAllCharacterData="props.getAllCharacterData"
          :character-ids="characterIds"
          @update:character-ids="updateCharacterIds"
        />
    </div>

    <!-- Character Display -->
    <div v-if="selectedCharacter">
      <!-- Character Name -->
       <div class="character-title-container">
         <p class="text-2xl font-bold themed-text-primary mb-6 character-title">{{ selectedCharacter.name }}</p>
       </div>

      <!-- Spells Table -->
      <div class="mb-8" v-if="selectedCharacter.spells">
        <h3 class="text-xl font-semibold themed-text-primary mb-4">Spells</h3>
        <div class="overflow-x-auto themed-bg-secondary rounded-lg shadow">
          <table class="min-w-full divide-y themed-border-primary">
            <thead class="themed-bg-tertiary">
              <tr>
                <th class="px-6 py-3 text-center text-xs font-medium themed-text-muted uppercase tracking-wider">
                  Name
                </th>
                <th class="px-6 py-3 text-center text-xs font-medium themed-text-muted uppercase tracking-wider">
                  Components Description
                </th>
                <th class="px-6 py-3 text-center text-xs font-medium themed-text-muted uppercase tracking-wider">
                  Components Consumed
                </th>
                <th class="px-6 py-3 text-center text-xs font-medium themed-text-muted uppercase tracking-wider">
                  Components Have Cost
                </th>
                <th class="px-6 py-3 text-center text-xs font-medium themed-text-muted uppercase tracking-wider">
                  Focus Will Work
                </th>
              </tr>
            </thead>
            <tbody class="themed-bg-secondary divide-y themed-border-primary">
              <tr v-if="selectedCharacter.spells.length == 0">
                <td class="px-6 py-4 whitespace-nowrap text-medium font-medium themed-text-primary">
                  -
                </td>
                <td class="px-6 py-4 whitespace-nowrap text-sm font-medium themed-text-primary">
                  -
                </td>
                <td class="px-6 py-4 whitespace-nowrap text-sm themed-text-tertiary">
                  -
                </td>
                <td class="px-6 py-4 whitespace-nowrap text-sm themed-text-tertiary">
                  -
                </td>
                <td class="px-6 py-4 whitespace-nowrap text-sm themed-text-tertiary">
                  -
                </td>
              </tr>
              <tr v-for="(spell, index) in selectedCharacter.spells" :key="index" class="themed-row-hover">
                <td class="px-6 py-4 whitespace-nowrap text-sm font-medium themed-text-primary">
                  {{ spell.name }}
                </td>
                <td class="px-6 py-4 whitespace-nowrap text-sm themed-text-tertiary max-w-xs break-words text-wrap">
                  {{ spell.componentsDescription || '—' }}
                </td>
                <td class="px-6 py-4 whitespace-nowrap text-sm themed-text-tertiary">
                  <span class="px-2 py-1 rounded-full text-xs">
                    <img :src="spell.componentsAreConsumed ? checkMark : xMark " width="20" height="20">
                  </span>
                </td>
                <td class="px-6 py-4 whitespace-nowrap text-sm themed-text-tertiary">
                  <span class="px-2 py-1 rounded-full text-xs">
                    <img :src="spell.componentsHaveCost ? checkMark : xMark " width="20" height="20">
                  </span>
                </td>
                <td class="px-6 py-4 whitespace-nowrap text-sm themed-text-tertiary">
                  <span class="px-2 py-1 rounded-full text-xs">
                    <img :src="spell.focusWillWork ? checkMark : xMark " width="20" height="20">
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
        <div class="themed-bg-secondary rounded-lg shadow" v-if="selectedCharacter.inventory">
          <button
            @click="showInventory = !showInventory"
            class="w-full px-6 py-4 text-left flex items-center justify-between themed-hover rounded-lg transition-colors"
          >
            <h3 class="text-lg font-semibold themed-text-primary">Inventory</h3>
            <svg class="w-5 h-5" :class="{ 'transform rotate-90': showInventory }" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7"></path>
            </svg>
          </button>
          <div v-show="showInventory" class="px-6 pb-4">
            <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
              <div v-for="(quantity, item) in selectedCharacter.inventory" :key="item" 
                  class="flex justify-between items-center py-2 px-3 border themed-border-secondary rounded themed-bg-tertiary">
                <span class="themed-text-primary font-medium">{{ item }}</span>
                <span class="themed-text-secondary themed-bg-secondary px-2 py-1 rounded text-sm font-semibold">
                  {{ quantity }}
                </span>
              </div>
            </div>
          </div>
        </div>

        <!-- Custom Items and Focus - Two Column Layout -->
        <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
          <!-- Custom Items -->
          <div class="themed-bg-secondary rounded-lg shadow" v-if="selectedCharacter.custom_items">
            <button
              @click="showCustomItems = !showCustomItems"
              class="w-full px-6 py-4 text-left flex items-center justify-between themed-hover rounded-lg transition-colors"
            >
              <div class="">
                <h3 class="text-lg font-semibold themed-text-primary smc-title">Custom Spell Material Components</h3>
                <div class="smc-note flex">
                  <p class="px-6 py-3 text-left text-xs themed-text-muted smc-info">(Expected custom item naming format: "SMC:Diamond_Dust:500GP")</p>
                </div>
              </div>
              <svg class="w-5 h-5 alight-right" :class="{ 'transform rotate-90': showCustomItems }" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7"></path>
              </svg>
            </button>
            <div v-show="showCustomItems" class="px-6 pb-4">
              <ul class="space-y-2">
                <li v-for="(value, item) in selectedCharacter.custom_items" :key="item" 
                    class="flex justify-between items-center py-2 border-b themed-border-tertiary last:border-b-0">
                  <span class="themed-text-primary">{{ item.replace(/_/g, ' ') }}</span>
                  <span class="themed-text-secondary bg-yellow-100 px-2 py-1 rounded text-sm">
                    {{ value }}
                  </span>
                </li>
              </ul>
            </div>
          </div>

          <!-- Focus -->
          <div class="themed-bg-secondary rounded-lg shadow" v-if="selectedCharacter.focus">
            <button
              @click="showFocus = !showFocus"
              class="w-full px-6 py-4 text-left flex items-center justify-between themed-hover rounded-lg transition-colors"
            >
              <h3 class="text-lg font-semibold themed-text-primary">Focus</h3>
              <svg class="w-5 h-5" :class="{ 'transform rotate-90': showFocus }" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7"></path>
              </svg>
            </button>
            <div v-show="showFocus" class="px-6 pb-4 space-y-3">
              <div v-if="selectedCharacter.focus.name">
                <span class="font-medium themed-text-secondary">Name:</span>
                <span class="ml-2 themed-text-primary">{{ selectedCharacter.focus.name }}</span>
              </div>
              <div v-if="selectedCharacter.focus.type">
                <span class="font-medium themed-text-secondary">Type:</span>
                <span class="ml-2 themed-text-primary">{{ selectedCharacter.focus.type }}</span>
              </div>
              <div v-if="selectedCharacter.focus.subType">
                <span class="font-medium themed-text-secondary">Subtype:</span>
                <span class="ml-2 themed-text-primary">{{ selectedCharacter.focus.subType }}</span>
              </div>
              <div v-if="selectedCharacter.focus.description">
                <span class="font-medium themed-text-secondary">Description:</span>
                <div class="mt-1 themed-text-primary text-sm leading-relaxed" v-html="selectedCharacter.focus.description">
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
    <!-- Confirmation Modal for Delete All Cached Data -->
    <ConfirmationModal
      :show="showDeleteConfirmation"
      message="Are you sure you want to delete all cached character data? This will clear all stored information and cannot be undone."
      title="Delete All Cached Data"
      confirmText="Delete All"
      cancelText="Cancel"
      confirmVariant="danger"
      @confirm="handleDeleteAllCachedData"
      @cancel="hideDeleteConfirmation"
    />
  </div>
</template>

<script setup>
import { ref, computed } from 'vue';
import checkMark from '../assets/green-checkmark.png';
import xMark from '../assets/red-x-icon.png';
import GenericButton from '../components/buttons/GenericButton.vue';
import CharacterIdInput from '../components/CharacterIdInput.vue';
import ConfirmationModal from '../components/ConfirmationModal.vue';
import ThemeToggleButton from '../components/buttons/ThemeToggleButton.vue';

const props = defineProps({
  campaignData: Object,
  characterData: Object,
  updateCurrentCharactersData: Function,
  getAllCharacterData: Function,
  deleteAllCachedData: Function,
});

// Reactive state
const showInventory = ref(false);
const showCustomItems = ref(false);
const showFocus = ref(false);
const selectedCharacterId = ref("-");
const selectedCampaignId = ref('all');
const characterIds = ref([]);
const showDeleteConfirmation = ref(false);

// // Computed properties
const computedFilteredCharacterIds = computed(() => {
  const allIds = props.characterData ? Object.keys(props.characterData) : [];
  if (selectedCampaignId.value === null || selectedCampaignId.value === 'all') return allIds;
  return allIds.filter(filterCharacterIdsByCampaignId)
})

const computedCampaignIds = computed(() => {
  return props.campaignData ? Object.keys(props.campaignData) : [];
});

// Filter characters based on selected campaign
const filterCharacterIdsByCampaignId = (id) => {
  const character = props.characterData[id];
  return character.campaignId === selectedCampaignId.value;
};

const updateCharacterIds = (newIds) => {
  characterIds.value = newIds;
}

const selectedCharacter = computed(() => {
  if (!props.characterData || !selectedCharacterId.value) return null;
  
  return props.characterData[selectedCharacterId.value];
})

const selectedCampaign = computed(() => {
  if (!props.campaignData || !selectedCampaignId.value) return null;
  if (selectedCampaign.value === 'all') return null;
  return props.campaignData[selectedCampaignId.value];
})

// Confirmation modal functions
const showDeleteAllConfirmation = () => {
  showDeleteConfirmation.value = true
}

const hideDeleteConfirmation = () => {
  showDeleteConfirmation.value = false
}

const handleDeleteAllCachedData = () => {
  if (props.deleteAllCachedData) {
    props.deleteAllCachedData()
  }
  hideDeleteConfirmation()
}
</script>

<style scoped>
/* Theme Toggle Container */
.theme-toggle-container {
  position: fixed;
  top: 1rem;
  right: 1rem;
  z-index: 100;
}

/* Themed classes using CSS custom properties */
.themed-bg {
  background-color: var(--bg-primary);
}

.themed-bg-secondary {
  background-color: var(--bg-secondary);
}

.themed-bg-tertiary {
  background-color: var(--bg-tertiary);
}

.themed-text-primary {
  color: var(--text-primary);
}

.themed-text-secondary {
  color: var(--text-secondary);
}

.themed-text-tertiary {
  color: var(--text-tertiary);
}

.themed-text-muted {
  color: var(--text-muted);
}

.themed-border-primary {
  border-color: var(--border-primary);
}

.themed-border-secondary {
  border-color: var(--border-secondary);
}

.themed-border-tertiary {
  border-color: var(--border-tertiary);
}

.themed-hover:hover {
  background-color: var(--bg-hover);
}

.themed-row-hover:hover {
  background-color: var(--bg-hover);
}

.themed-select {
  background-color: var(--bg-secondary);
  color: var(--text-primary);
  border-color: var(--border-primary);
}

.themed-select:focus {
  border-color: #3b82f6;
  box-shadow: 0 0 0 2px rgba(59, 130, 246, 0.5);
}

/* Base Layout */
.max-w-6xl {
  max-width: 72rem;
}

.mx-auto {
  margin-left: auto;
  margin-right: auto;
}

/* Spacing */
.p-6 { padding: 1.5rem; }
.px-2 { padding-left: 0.5rem; padding-right: 0.5rem; }
.px-3 { padding-left: 0.75rem; padding-right: 0.75rem; }
.px-6 { padding-left: 1.5rem; padding-right: 1.5rem; }
.py-1 { padding-top: 0.25rem; padding-bottom: 0.25rem; }
.py-2 { padding-top: 0.5rem; padding-bottom: 0.5rem; }
.py-3 { padding-top: 0.75rem; padding-bottom: 0.75rem; }
.py-4 { padding-top: 1rem; padding-bottom: 1rem; }
.py-8 { padding-top: 2rem; padding-bottom: 2rem; display: flex; justify-content: center;}
.pb-4 { padding-bottom: 1rem; }

.mb-1 { margin-bottom: 0.25rem; }
.mb-2 { margin-bottom: 0.5rem; }
.mb-4 { margin-bottom: 1rem; }
.mb-6 { margin-bottom: 1.5rem; }
.mb-8 { margin-bottom: 2rem; }
.mt-1 { margin-top: 0.25rem; }
.ml-2 { margin-left: 0.5rem; }

/* Grid Layout */
.grid {
  display: grid;
}

.grid-cols-1 {
  grid-template-columns: repeat(1, minmax(0, 1fr));
}

.gap-4 {
  gap: 1rem;
}

/* Medium screens and up - two columns */
@media (min-width: 768px) {
  .md\:grid-cols-2 {
    grid-template-columns: repeat(2, minmax(0, 1fr));
  }
}

/* Typography */
.text-xs { font-size: 0.75rem; line-height: 1rem; }
.text-sm { font-size: 0.875rem; line-height: 1.25rem; }
.text-lg { font-size: 1.125rem; line-height: 1.75rem; }
.text-xl { font-size: 1.25rem; line-height: 1.75rem; }
.text-2xl { font-size: 1.5rem; line-height: 2rem; }
.text-3xl { font-size: 1.875rem; line-height: 2.25rem; }

.font-medium { font-weight: 500; }
.font-semibold { font-weight: 600; }
.font-bold { font-weight: 700; }

.text-left { text-align: left; }
.text-right { text-align: right; }
.text-center { text-align: center; }

.uppercase { text-transform: uppercase; }
.tracking-wider { letter-spacing: 0.05em; }
.leading-relaxed { line-height: 1.625; }

/* Layout */
.block { display: block; }
.flex { display: flex; }
.items-start { align-items: flex-start; }
.items-center { align-items: center; }
.justify-between { justify-content: space-between; }

.w-5 { width: 1.25rem; }
.h-5 { height: 1.25rem; }
.w-64 { width: 16rem; }
.w-full { width: 100%; }
.min-w-full { min-width: 100%; }
.max-w-xs { max-width: 20rem; }

/* Borders and Shapes */
.border { border-width: 1px; }
.border-b { border-bottom-width: 1px; }
.rounded { border-radius: 0.25rem; }
.rounded-md { border-radius: 0.375rem; }
.rounded-lg { border-radius: 0.5rem; }
.rounded-full { border-radius: 9999px; }

/* Effects */
.shadow { 
  box-shadow: var(--shadow-md);
}
.shadow-sm { 
  box-shadow: var(--shadow-sm);
}
.opacity-90 { opacity: 0.9; }

/* Button and interactive element styling */
button {
  background: none;
  border: none;
  cursor: pointer;
  font: inherit;
}

/* Transitions */
.transition-colors {
  transition-property: background-color, border-color, color, fill, stroke;
  transition-timing-function: cubic-bezier(0.4, 0, 0.2, 1);
  transition-duration: 150ms;
}

/* Transform */
.transform { transform: translateX(var(--tw-translate-x, 0)) translateY(var(--tw-translate-y, 0)) rotate(var(--tw-rotate, 0deg)); }
.rotate-90 { --tw-rotate: 90deg; }

/* Spacing utilities */
.space-y-2 > * + * { margin-top: 0.5rem; }
.space-y-3 > * + * { margin-top: 0.75rem; }
.space-y-4 > * + * { margin-top: 1rem; }

/* Table */
.overflow-x-auto { overflow-x: auto; }
.divide-y > * + * { border-top-width: 1px; }
.whitespace-nowrap { white-space: nowrap; }

/* Text utilities */
.break-words { word-wrap: break-word; word-break: break-word; }
.text-wrap { white-space: normal; }

/* Focus states */
.focus\:outline-none:focus { outline: 2px solid transparent; outline-offset: 2px; }
.focus\:ring-2:focus { 
  box-shadow: var(--tw-ring-offset-shadow), var(--tw-ring-shadow), var(--tw-shadow, 0 0 #0000); 
  --tw-ring-offset-width: 0px; 
  --tw-ring-shadow: var(--tw-ring-inset) 0 0 0 calc(2px + var(--tw-ring-offset-width)) var(--tw-ring-color); 
}
.focus\:ring-offset-2:focus { --tw-ring-offset-width: 2px; }
.focus\:ring-blue-500:focus { --tw-ring-color: #3b82f6; }
.focus\:border-blue-500:focus { border-color: #3b82f6; }

/* Form elements */
select {
  appearance: none;
  background-image: url("data:image/svg+xml;charset=utf-8,%3csvg xmlns='http://www.w3.org/2000/svg' fill='none' viewBox='0 0 20 20'%3e%3cpath stroke='%236b7280' stroke-linecap='round' stroke-linejoin='round' stroke-width='1.5' d='M6 8l4 4 4-4'/%3e%3c/svg%3e");
  background-position: right 0.5rem center;
  background-repeat: no-repeat;
  background-size: 1.5em 1.5em;
  padding-right: 2.5rem;
}

/* Gradient - keeping original colors for header */
.bg-gradient-to-r {
  background-image: linear-gradient(to right, var(--tw-gradient-stops));
}

.from-purple-600 {
  --tw-gradient-from: #9333ea;
  --tw-gradient-stops: var(--tw-gradient-from), var(--tw-gradient-to, rgba(147, 51, 234, 0));
}

.to-blue-600 {
  --tw-gradient-to: #2563eb;
}

.text-white { color: #ffffff; }

/* List utilities */
.last\:border-b-0:last-child {
  border-bottom-width: 0;
}

/* Button list layout */
.button-list {
  display: flex;
  flex-wrap: wrap;
  gap: 1rem;
  align-items: flex-end;
  list-style: none;
  padding: 0;
  margin: 0;
  justify-content: space-evenly;
}

/* Table centering */
table {
  text-align: center;
  border-collapse: collapse;
}

thead {
  text-align: center;
}

tr:hover {
  background-color: var(--bg-hover);
}

.smc-title {
  margin-bottom: 0px;
}

.smc-info {
  margin-top: 0px;
  padding-top: 0px;
  padding-left: 0px;
  font-size: 10px;
}

.character-title-container {
  display: flex;
  justify-content: center;
}

.character-title{
  font-size: 3em;
  font-family: 'Medieval Times', sans-serif;
}

/* Special color overrides for elements that should stay consistent */
.text-gray-500 {
  color: var(--text-muted);
}

.bg-yellow-100 {
  background-color: #B8860B;
}

/* Responsive Design */
@media (max-width: 640px) {
  .theme-toggle-container {
    top: 0.5rem;
    right: 0.5rem;
  }
}
</style>