<script>
import DnDMainView from './views/DnDMainView.vue'
import ThemeProvider from './components/ThemeProvider.vue'
import axios from 'axios';

export default {
  components: {
    DnDMainView,
    ThemeProvider
  },
  data() {
    return {
      characterData: {},
      campaignData: {}
    }
  },
  mounted() {
    // checks if cached file exists on server
    const allIds = this.characterData ? Object.keys(this.characterData) : [];
    this.getAllCharacterData(allIds, false);
  },
  methods: {
    async getAllCharacterData(characterIds, forceUpdate) {
      if (characterIds === undefined) return {};
      if (characterIds.length === 0 && forceUpdate) return {};
      try {
        const res = await axios.get(
          'http://127.0.0.1:8998/characters', {
          params: {
            "force_update": forceUpdate,
            "char_ids": characterIds
          },
          paramsSerializer: { indexes: null },
        });
        if (res.data && res.data.characters) {
          // console.log('Received character data:', res.data.characters);
          this.characterData = { ...this.characterData, ...res.data.characters };
        }
        if (res.data && res.data.campaigns) {
          // console.log('Received campaign data:', res.data.campaigns);
          this.campaignData = { ...this.campaignData, ...res.data.campaigns };
        }
      } catch(error) {
        console.error('Error fetching character data:', error);
      };
    },
    async updateCurrentCharactersData(characterId, forceUpdate) {
      if (!characterId || characterId === '-') {
        // console.log('No valid character ID provided for update');
        return;
      };
      try {
        const res = await axios.get(
          `http://127.0.0.1:8998/characters/${characterId}`, {
            params: {"force_update": forceUpdate},
            paramsSerializer: { indexes: null },
          });
        if (res.data) {
          // console.log('Updated character data:', res.data);
          if (res.data.characters) {
            this.characterData = {...this.characterData, ...res.data.characters};
          };
          if (res.data.campaigns) {
            this.campaignData = {...this.campaignData, ...res.data.campaigns};
          };
        };
      } catch(error) {
        console.error('Error updating character data:', error);
      };
    },
    async deleteAllCachedData() {
      try {
        await axios.delete('http://127.0.0.1:8998/characters')
        // console.log('All cached data deleted');
        this.campaignData = {};
        this.characterData = {};
      } catch(error) {
        console.error('Error deleting cached data:', error);
      }
    },
    async deleteCharacterById(characterId) {
      if (!characterId || !Object.keys(this.characterData).includes(characterId)) {
        // console.log('Character ID not found or invalid:', characterId);
        return;
      }
      try {
        // console.log('Deleting character:', characterId);
        const res = await axios.delete(`http://127.0.0.1:8998/characters/${characterId}`);
        if (res.data) {
          // console.log('Server response after deletion:', res.data);
          // Replace entire objects to ensure reactivity
          this.characterData = { ...res.data.characters };
          this.campaignData = { ...res.data.campaigns };
        } else {
          // If no data returned, the character was the last one
          // console.log('No data returned, assuming all characters deleted');
          this.characterData = {};
          this.campaignData = {};
        }
      } catch(error) {
        console.error('Error deleting character:', error);
      };
    },
  }
};
</script>

<template>
  <ThemeProvider>
    <div class="wrapper">
      <DnDMainView 
        :campaignData="campaignData" 
        :characterData="characterData"
        :updateCurrentCharactersData="updateCurrentCharactersData"
        :getAllCharacterData="getAllCharacterData"
        :deleteAllCachedData="deleteAllCachedData"
        :deleteCharacterById="deleteCharacterById"
      />
    </div>
  </ThemeProvider>
</template>

<style>
body {
  font-family: 'Gill Sans', 'Gill Sans MT', Calibri, 'Trebuchet MS', sans-serif;
  margin: 0;
  padding: 0;
  background-color: var(--bg-primary);
  color: var(--text-primary);
  transition: background-color 0.2s ease, color 0.2s ease;
}

.wrapper {
  min-height: 100vh;
  background-color: var(--bg-primary);
}
</style>