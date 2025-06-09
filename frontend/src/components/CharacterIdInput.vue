<template>
    <!-- CharacterIdInput.vue -->
     <div class="clear-section">
        <button @click="hideCharacterInputModal" class="close-button">×</button>
     </div>
    <div class="modal-header">
         <!-- Current Character ID Display -->
        <div>
            <h3 class="modal-title">Existing Character(s):
                <div class="id-list">
                    <div 
                        v-for="[id, name] of Object.entries(currentCharIds)" 
                        :key="id" 
                        class="id-item"
                    >
                        <span class="id-text">{{ name }}</span>
                        <!-- These funcs may need special delete func for confirm modal -->
                        <button 
                            @click="removeCharacterId(id)"
                            class="delete-button"
                            title="Remove ID"
                        >
                            ×
                        </button>
                    </div>
                </div>
            </h3>
             <!-- Pending Character ID Display -->
            <h3 class="modal-title">Pending ID(s):
                <!-- Pending is working fine for clearing. Might need to fix for update button -->
                <div class="id-list">
                    <div 
                        v-for="id in pendingCharIds" 
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
                <div v-if="pendingCharIds.length > 0" class="clear-section">
                    <GenericButton 
                        :onClick="confirmClearAllPendingIds"
                        text="Clear All Pending IDs"
                        variant="outline"
                    />
                </div>
            </h3>
            
        </div>
    </div>
    <div class="character-id-input">
        <!-- Input Section -->
        <div class="input-section">
            <div class="input-group">
                <input 
                    type="text" 
                    ref="inputRef"
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
        <div>
            <div class="data-button">
                <GenericButton 
                    :onClick="() => getAllNewCharacterDataCl(pendingCharIds, true)"
                    :disabled="pendingCharIds.length === 0"
                    text="Get Character Data"
                    variant="primary"
                />
                <p class="helper-text">
                    Note: If you have already entered the Character IDs, they should be cached by the backend and  don't need to enter IDs.
                </p>
            </div>
        </div>
        <!-- Confirmation Modal -->
        <ConfirmationModal
            :show="showConfirmation"
            :message="confirmationMessage"
            title="Clear All Pending Character IDs"
            confirmText="Clear All"
            cancelText="Cancel"
            @confirm="confirmAction"
            @cancel="cancelConfirmation"
        />
    </div>
</template>

<script setup>
import { ref, nextTick, defineModel } from 'vue';
import GenericButton from './buttons/GenericButton.vue';
import ConfirmationModal from './ConfirmationModal.vue';

const props = defineProps({
    getAllCharacterData: Function,
    hideCharacterInputModal: Function,
    deleteCharacterById: Function,
});

const currentCharIds = defineModel('currentCharIds', {
  type: Object,
  default: () => {},
});
const pendingCharIds = ref([]);
const inputValue = ref('');
const showConfirmation = ref(false);
const confirmationMessage = ref('');
const pendingAction = ref(null);
const inputRef = ref(null);

const handleInput = (event) => {
    const value = event.target.value;
    // Remove any character that isn't a digit or comma
    const filtered = value.replace(/[^0-9,]/g, '');
    inputValue.value = filtered;
};

const handlePaste = (event) => {
    event.preventDefault();
    const paste = (event.clipboardData || window.clipboardData).getData('text');
    const filtered = paste.replace(/[^0-9,]/g, '');
    inputValue.value = filtered;
};

const addCharacterIds = async () => {
    if (!inputValue.value.trim()) return;
  
    // Split by comma, trim whitespace, filter out empty strings
    const newIds = inputValue.value
        .split(',')
        .map(id => id.trim())
        .filter(id => id.length > 0)
        .filter(id => !Object.keys(currentCharIds.value).includes(id) && id !== '-'); // Avoid duplicates
  
    if (newIds.length > 0) {
        pendingCharIds.value = newIds;
    };
    inputValue.value = '';

    // Refocus the input after the DOM updates
    await nextTick();
    if (inputRef.value) {
      inputRef.value.focus();
    };
};

const removeCharacterId = (idToRemove) => {
    debugger;
    if (Object.keys(currentCharIds.value).includes(idToRemove)) {
        // If id is current, requires a delete request to server
        const temp = currentCharIds.value;
        delete temp[idToRemove];
        currentCharIds.value = temp;
        props.deleteCharacterById(idToRemove);
    }
    const updatedPendingIds = pendingCharIds.value.filter(id => id !== idToRemove);
    pendingCharIds.value = updatedPendingIds;
};

const clearPendingIds = () => {
    pendingCharIds.value = [];
};

// Confirmation functions
const confirmClearAllPendingIds = () => {
  confirmationMessage.value = `Are you sure you want to clear all ${pendingCharIds.value.length} pending character IDs?`;
  pendingAction.value = () => clearPendingIds();
  showConfirmation.value = true;
};

const confirmAction = () => {
  if (pendingAction.value) {
    pendingAction.value();
  };
  showConfirmation.value = false;
  pendingAction.value = null;
};

const cancelConfirmation = () => {
  showConfirmation.value = false;
  pendingAction.value = null;
};

const getAllNewCharacterDataCl = (charIds, forceUpdate) => {
    const filteredIds = charIds.filter(id => {
        return !Object.keys(currentCharIds.value).includes(id);
    });
    clearPendingIds();
    props.getAllCharacterData(filteredIds, forceUpdate);
};
</script>

<style scoped>
/* Themed classes */
.themed-text-secondary {
  color: var(--text-secondary);
}

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
    border: 1px solid var(--border-primary);
    background-color: var(--bg-secondary);
    color: var(--text-primary);
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
    color: var(--text-muted);
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
    margin-top: .5rem
}

.id-item {
    display: flex;
    align-items: center;
    background-color: var(--bg-tertiary);
    border: 1px solid var(--border-primary);
    border-radius: 0.5rem;
    padding: 0.1rem 0.25rem;
    transition: all 0.2s ease;
}

.id-item:hover {
    background-color: var(--bg-hover);
    box-shadow: var(--shadow-sm);
}

.id-text {
    font-size: 0.875rem;
    font-weight: 500;
    color: var(--text-primary);
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

.modal-header {
  padding: 0 1rem 1.5rem 0;
  width: 100%;
}

.modal-title {
  font-size: 1.125rem;
  font-weight: 600;
  color: var(--text-primary);
  margin: 0;
}

.close-button {
  background: none;
  border: none;
  font-size: 1.5rem;
  cursor: pointer;
  color: var(--text-secondary);
  padding: 0;
  width: 2rem;
  height: 2rem;
  display: flex;
  align-items: center;
  justify-content: center;
}

.close-button:hover {
  color: var(--text-primary);
}

/* Clear Section */
.clear-section {
    display: flex;
    justify-content: flex-end;
}

/* Helper Text */
.helper-text {
    font-size: 0.9rem;
    color: var(--text-muted);
    line-height: 1.4;
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

.mb-2 {
    margin-bottom: 0.5rem;
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
}
</style>