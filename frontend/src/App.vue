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
        this.characterData = {...this.characterData, ...res.data.characters};
        this.campaignData = {...this.campaignData, ...res.data.campaigns};
      } catch(error) {
        console.error(error);
      };
    },
    async updateCurrentCharactersData(characterId, forceUpdate) {
      try {
        const res = await axios.get(
          `http://127.0.0.1:8998/characters/${characterId}`, {
            params: {"force_update": forceUpdate},
            paramsSerializer: { indexes: null },
          })
        if (res.data) {
          this.characterData = {...this.characterData, ...res.data.characters};
          this.campaignData = {...this.campaignData, ...res.data.campaigns};
        }
      } catch(error) {
        console.log(error);
      }
    },
    async deleteAllCachedData() {
      try {
        await axios.delete('http://127.0.0.1:8998/characters')
        this.campaignData = {}
        this.characterData = {}
      } catch(error) {
        console.log(error);
      }
    },
    async deleteCharacterById(characterId) {
      if (!Object.keys(this.characterData).includes(characterId)) return;
      try {
        const res = await axios.delete(`http://127.0.0.1:8998/characters/${characterId}`)
        if (res.data) {
          this.characterData = {...this.characterData, ...res.data.characters};
          this.campaignData = {...this.campaignData, ...res.data.campaigns};
        }
      } catch(error) {
        console.log(error);
      }
    }
  }
}
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