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
    this.getAllCharacterData({}, false);
  },
  methods: {
    async getAllCharacterData(characterIds, forceUpdate) {
      try {
        const res = await axios.get(
          'http://127.0.0.1:8998/characters', {
          params: {
            "force_update": forceUpdate,
            "char_ids": characterIds
          },
          paramsSerializer: { indexes: null },
        });
        this.characterData = res.data.characters;
        this.campaignData = res.data.campaign;
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
          this.characterData[characterId] = res.data
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