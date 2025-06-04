<script>
import DnDMainView from './views/DnDMainView.vue'
import axios from 'axios';

export default {
  components: {
    DnDMainView
  },
  data() {
    return {
      isLoading: false,
      characterData: {},
      campaignData: {},
      characterIds: {},
      forceUpdate: false
    }
  },
  methods: {
    async getAllCharacterData(characterIds, forceUpdate) {
      try {
      const res = await axios.get(
        `http://127.0.0.1:8998/characters`, {
        params: {
          "force_update": forceUpdate,
          "char_ids": characterIds
        },
        paramsSerializer: { indexes: null },
      });
      this.characterData = res.data.characters;
      this.campaignData = res.data.campaign;
      console.log(this.characterData)
    } catch(error) {
        console.error(error);
      };
    },
    async getOneCharactersData(characterId, forceUpdate) {
      try {
        const res = await axios.get(
          `http://127.0.0.1:8998/characters/${characterId}`, {
            params: {"force_update": forceUpdate},
            paramsSerializer: { indexes: null },
          })
          if (res.data) {
            this.characterData[characterId] = res.data
          }
          console.log(this.characterData)
        } catch(error) {
          console.log(error);
        }
      }
    }
  }
</script>

<template>
  <div class="wrapper">
    <DnDMainView 
      :campaignData="campaignData" 
      :characterData="characterData"
      :getOneCharactersData="getOneCharactersData"
      :getAllCharacterData="getAllCharacterData"
      >
    </DnDMainView>

  </div>
  <button @click="getAllCharacterData(characterIds, false)">Get Data</button>
</template>
