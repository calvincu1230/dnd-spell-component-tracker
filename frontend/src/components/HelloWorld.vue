<!-- <script setup>
defineProps({
  msg: {
    type: String,
    required: true,
  },
})
</script>

<template>
  <div class="greetings">
    <h1 class="green">{{ msg }}</h1>
    <h3>
      You’ve successfully created a project with
      <a href="https://vite.dev/" target="_blank" rel="noopener">Vite</a> +
      <a href="https://vuejs.org/" target="_blank" rel="noopener">Vue 3</a>.
    </h3>
  </div>
</template>

<style scoped>
h1 {
  font-weight: 500;
  font-size: 2.6rem;
  position: relative;
  top: -10px;
}

h3 {
  font-size: 1.2rem;
}

.greetings h1,
.greetings h3 {
  text-align: center;
}

@media (min-width: 1024px) {
  .greetings h1,
  .greetings h3 {
    text-align: left;
  }
}
</style> -->
<style>
    body {
        font-family: Arial, sans-serif;
        max-width: 1200px;
        margin: 0 auto;
        padding: 20px;
        background-color: #f5f5f5;
    }
    .container {
        background: white;
        padding: 30px;
        border-radius: 10px;
        box-shadow: 0 2px 10px rgba(0,0,0,0.1);
    }
    .button-group {
        margin-bottom: 30px;
    }
    button {
        background: #007bff;
        color: white;
        border: none;
        padding: 12px 24px;
        margin: 5px;
        border-radius: 5px;
        cursor: pointer;
        font-size: 16px;
        transition: background-color 0.3s;
    }
    button:hover {
        background: #0056b3;
    }
    button:disabled {
        background: #6c757d;
        cursor: not-allowed;
    }
    .character-list {
        display: grid;
        grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
        gap: 20px;
        margin-top: 20px;
    }
    .character-card {
        background: #f8f9fa;
        padding: 20px;
        border-radius: 8px;
        border: 1px solid #dee2e6;
    }
    .character-detail {
        background: #e3f2fd;
        padding: 20px;
        border-radius: 8px;
        border-left: 4px solid #2196f3;
        margin-top: 20px;
    }
    .loading {
        text-align: center;
        color: #666;
        font-style: italic;
    }
    .error {
        background: #ffebee;
        color: #c62828;
        padding: 15px;
        border-radius: 5px;
        border-left: 4px solid #f44336;
        margin: 10px 0;
    }
    .input-group {
        margin: 20px 0;
    }
    input[type="text"] {
        padding: 10px;
        border: 1px solid #ddd;
        border-radius: 5px;
        margin-right: 10px;
        font-size: 16px;
    }
    pre {
        background: #f4f4f4;
        padding: 15px;
        border-radius: 5px;
        overflow-x: auto;
        font-size: 14px;
    }
</style>
<template>

  <div id="app">
      <div class="container">
          <h1>Character Database</h1>
          
          <!-- Button controls -->
          <div class="button-group">
              <button @click="fetchAllCharacters" :disabled="loading">
                  {{ loading && currentAction === 'fetchAll' ? 'Loading...' : 'Get All Characters' }}
              </button>
              
              <div class="input-group">
                  <input 
                      type="text" 
                      v-model="characterId" 
                      placeholder="Enter character ID"
                      @keyup.enter="fetchSingleCharacter"
                  >
                  <button @click="fetchSingleCharacter" :disabled="loading || !characterId">
                      {{ loading && currentAction === 'fetchSingle' ? 'Loading...' : 'Get Character' }}
                  </button>
              </div>
              
              <button @click="clearData">Clear Data</button>
          </div>
  
          <!-- Error display -->
          <div v-if="error" class="error">
              <strong>Error:</strong> {{ error }}
          </div>
  
          <!-- Loading indicator -->
          <div v-if="loading" class="loading">
              Loading data from API...
          </div>
  
          <!-- Display all characters -->
          <div v-if="characters.length > 0">
              <h2>All Characters ({{ characters.length }} found)</h2>
              <div class="character-list">
                  <div v-for="character in characters" :key="character.id" class="character-card">
                      <h3>{{ character.name || 'Unnamed Character' }}</h3>
                      <p><strong>ID:</strong> {{ character.id }}</p>
                      <!-- Display other character properties dynamically -->
                      <div v-for="(value, key) in character" :key="key">
                          <p v-if="key !== 'id' && key !== 'name'">
                              <strong>{{ formatKey(key) }}:</strong> {{ formatValue(value) }}
                          </p>
                      </div>
                  </div>
              </div>
          </div>
  
          <!-- Display single character -->
          <div v-if="singleCharacter" class="character-detail">
              <h2>Character Details</h2>
              <h3>{{ singleCharacter.name || 'Unnamed Character' }}</h3>
              <pre>{{ JSON.stringify(singleCharacter, null, 2) }}</pre>
          </div>
  
          <!-- Help text -->
          <div v-if="!characters.length && !singleCharacter && !loading" style="margin-top: 30px; color: #666;">
              <p>Click "Get All Characters" to fetch all characters from your API, or enter a character ID and click "Get Character" to fetch a specific one.</p>
              <p><strong>Note:</strong> Make sure your FastAPI backend is running and accessible. The default API base URL is set to <code>http://localhost:8000</code></p>
          </div>
      </div>
  </div>
</template>

<script>
import { } from 'VueAxios'
import { createApp } from 'vue';

createApp({
    data() {
        return {
            characters: [],        // Array to store all characters
            singleCharacter: null, // Object to store single character
            characterId: '',       // Input field for character ID
            loading: false,        // Loading state
            error: null,          // Error message
            currentAction: null,   // Track which action is loading
            // Your FastAPI backend URL - change this if needed
            apiBaseUrl: 'http://localhost:8998'
        }
    },
    methods: {
        // Fetch all characters from /characters endpoint
        async fetchAllCharacters() {
            this.loading = true;
            this.currentAction = 'fetchAll';
            this.error = null;
            this.singleCharacter = null; // Clear single character when fetching all
            
            try {
                const response = await axios.get(`${this.apiBaseUrl}/characters`);
                this.characters = response.data;
                console.log('Fetched characters:', response.data);
            } catch (error) {
                this.handleError('Failed to fetch characters', error);
            } finally {
                this.loading = false;
                this.currentAction = null;
            }
        },

        // Fetch single character from /characters/{character_id} endpoint
        async fetchSingleCharacter() {
            if (!this.characterId.trim()) {
                this.error = 'Please enter a character ID';
                return;
            }

            this.loading = true;
            this.currentAction = 'fetchSingle';
            this.error = null;
            this.characters = []; // Clear all characters when fetching single
            
            try {
                const response = await axios.get(`${this.apiBaseUrl}/characters/${this.characterId}`);
                this.singleCharacter = response.data;
                console.log('Fetched character:', response.data);
            } catch (error) {
                this.handleError(`Failed to fetch character with ID: ${this.characterId}`, error);
            } finally {
                this.loading = false;
                this.currentAction = null;
            }
        },

        // Clear all data
        clearData() {
            this.characters = [];
            this.singleCharacter = null;
            this.characterId = '';
            this.error = null;
        },

        // Handle API errors
        handleError(message, error) {
            console.error('API Error:', error);
            
            if (error.response) {
                // Server responded with error status
                this.error = `${message}: ${error.response.status} - ${error.response.data?.detail || error.response.statusText}`;
            } else if (error.request) {
                // Request made but no response received
                this.error = `${message}: Unable to connect to the API. Make sure your FastAPI server is running.`;
            } else {
                // Something else happened
                this.error = `${message}: ${error.message}`;
            }
        },

        // Format object keys for display (convert snake_case to Title Case)
        formatKey(key) {
            return key.replace(/_/g, ' ').replace(/\b\w/g, l => l.toUpperCase());
        },

        // Format values for display
        formatValue(value) {
            if (typeof value === 'object' && value !== null) {
                return JSON.stringify(value);
            }
            return value;
        }
    }
}).mount('#app');
</script>