<template>
    <!-- CharacterIdInput.vue -->
    <div class="character-id-input">

        <!-- Character ID Display -->
        <div v-if="props.characterIds.length > 0" class="id-display-section">
            <h4 class="text-sm font-medium text-gray-700 mb-2">
            Added Character IDs ({{ props.characterIds.length }})
            </h4>
            <div class="id-list">
                <div 
                    v-for="id in props.characterIds" 
                    :key="id" 
                    class="id-item"
                >
                    <span class="id-text">{{ id }}</span>
                    <button 
                        @click="removeCharacterId(id)"
                        class="delete-button"
                        title="Remove ID"
                    >
                        ×
                    </button>
                </div>
            </div>
        
            <!-- Clear All Button -->
            <div class="clear-section">
                <GenericButton 
                    :onClick="clearAllIds"
                    text="Clear All"
                    variant="outline"
                />
            </div>
        </div>

        <!-- Input Section -->
        <div class="input-section">
            <!-- <label class="block text-sm font-medium text-gray-700 mb-2">
                Character IDs: 
            </label> -->
            <div class="input-group">
                <input 
                    type="text" 
                    v-model="inputValue"
                    @input="handleInput"
                    @paste="handlePaste"
                    @keyup.enter="addCharacterIds"
                    placeholder="Enter character Id(s) - comma separated"
                    class="text-input"
                />
                <GenericButton 
                    :onClick="addCharacterIds"
                    text="Add"
                    variant="primary"
                    :disabled="!inputValue.trim()"
                />
            </div>
            <!-- Helper Text -->
            <div class="input-group">
                <p class="helper-text">
                    Enter character IDs one by one or separated by commas. These IDs will be used for retrieving data from DnDBeyond. 
                    If nothing happens after adding the IDs and pressing the 'Get Character Data' button, check 
                    that the IDs are correct before contacting tech support.
                </p>
            </div>
        </div>

        <!-- Get Character Data Button Section -->
        <div class="data-button-container">
            <div class="data-button">
                <GenericButton 
                    :onClick="() => getAllCharacterData(characterIds, true)"
                    text="Get Character Data"
                    variant="primary"
                />
                <p class="helper-text">
                    Note: If you have already entered the Character IDs, they should be cached by the backend and  don't need to enter IDs.
                </p>
            </div>
        </div>
    </div>
</template>

<script setup>
import { ref } from 'vue'
import GenericButton from './buttons/GenericButton.vue'

const props = defineProps({
    getAllCharacterData: Function,
    characterIds: {
        type: Array,
        default: () => []
    }
})

const emit = defineEmits(['update:characterIds'])

const inputValue = ref('')

const handleInput = (event) => {
    const value = event.target.value
    // Remove any character that isn't a digit or comma
    const filtered = value.replace(/[^0-9,]/g, '')
    inputValue.value = filtered
}

const handlePaste = (event) => {
    event.preventDefault()
    const paste = (event.clipboardData || window.clipboardData).getData('text')
    const filtered = paste.replace(/[^0-9,]/g, '')
    inputValue.value = filtered
}

const addCharacterIds = () => {
    if (!inputValue.value.trim()) return
  
    // Split by comma, trim whitespace, filter out empty strings
    const newIds = inputValue.value
        .split(',')
        .map(id => id.trim())
        .filter(id => id.length > 0)
        .filter(id => !props.characterIds.includes(id)) // Avoid duplicates
  
    if (newIds.length > 0) {
        const updatedIds = [...new Set([...props.characterIds, ...newIds])]
        emit('update:characterIds', updatedIds)
    }
    inputValue.value = ''
}

const removeCharacterId = (idToRemove) => {
  const updatedIds = props.characterIds.filter(id => id !== idToRemove)
  emit('update:characterIds', updatedIds)
}

const clearAllIds = () => {
  emit('update:characterIds', [])
}
</script>

<style scoped>
.character-id-input {
    display: flex;
    flex-direction: column;
    align-items: center;
    width: 100%;
    max-width: 600px;
}

/* Input Section */
.input-section {
  margin-bottom: 1.5rem;
}

.input-group {
  display: flex;
  gap: 0.5rem;
  justify-content: center;
}

.text-input {
  flex: 1;
  padding: 0.5rem 0.75rem;
  border: 1px solid #d1d5db;
  border-radius: 0.375rem;
  font-size: 0.875rem;
  line-height: 1.25rem;
  transition: border-color 0.15s ease-in-out, box-shadow 0.15s ease-in-out;
  max-width: 500px;
}

.text-input:focus {
  outline: none;
  border-color: #3b82f6;
  box-shadow: 0 0 0 2px rgba(59, 130, 246, 0.2);
}

.text-input::placeholder {
  color: #9ca3af;
}

/* ID Display Section */
.id-display-section {
  margin-bottom: 1rem;
}

.id-list {
  display: flex;
  flex-wrap: wrap;
  gap: 0.5rem;
  margin-bottom: 1rem;
}

.id-item {
  display: flex;
  align-items: center;
  background-color: #e5e7eb;
  border: 1px solid #d1d5db;
  border-radius: 0.5rem;
  padding: 0.25rem 0.5rem;
  transition: all 0.2s ease;
}

.id-item:hover {
  background-color: #d1d5db;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.id-text {
  font-size: 0.875rem;
  font-weight: 500;
  color: #374151;
  padding: 0.25rem 0.5rem;
  user-select: none;
}

.delete-button {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 20px;
  height: 20px;
  background-color: #ef4444;
  color: white;
  border: none;
  border-radius: 50%;
  font-size: 14px;
  font-weight: bold;
  cursor: pointer;
  margin-left: 0.5rem;
  transition: all 0.2s ease;
  line-height: 1;
  padding: 0;
}

.delete-button:hover {
  background-color: #dc2626;
  transform: scale(1.1);
}

.delete-button:active {
  transform: scale(0.95);
}

.delete-button:focus {
  outline: none;
  box-shadow: 0 0 0 2px rgba(239, 68, 68, 0.3);
}

/* Clear Section */
.clear-section {
  display: flex;
  justify-content: flex-end;
}

/* Helper Text */
.helper-text {
  font-size: 0.9rem;
  color: #6b7280;
  line-height: 1.4;
  /* margin-top: 0.5rem; */
  max-width: 600px;
}

/* Utility Classes */
.block {
  display: block;
}

.text-sm {
  font-size: 0.875rem;
  line-height: 1.25rem;
}

.font-medium {
  font-weight: 500;
}

.text-gray-700 {
  color: #374151;
}

.mb-2 {
  margin-bottom: 0.5rem;
}

.data-button-container {
    
}

.data-button {
    max-width: 350px;
    display: grid;
    gap: 0.5rem;
    justify-content: center;
}

/* Responsive Design */
@media (max-width: 640px) {
  .input-group {
    flex-direction: column;
    align-items: stretch;
  }
  
  .id-list {
    flex-direction: column;
  }
  
  .id-item {
    justify-content: space-between;
  }
}
</style>