<script>
import { RouterLink, RouterView } from 'vue-router'
import HelloWorld from './components/HelloWorld.vue'
import axios from 'axios';

export default {
  components: {
    HelloWorld
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
    <HelloWorld 
      :campaignData="campaignData" 
      :characterData="characterData"
      :getOneCharactersData="getOneCharactersData">
    </HelloWorld>

  </div>
  <button @click="getAllCharacterData(characterIds, false)">Get Data</button>
</template>

<style scoped>
header {
  line-height: 1.5;
  max-height: 100vh;
}

.logo {
  display: block;
  margin: 0 auto 2rem;
}

nav {
  width: 100%;
  font-size: 12px;
  text-align: center;
  margin-top: 2rem;
}

nav a.router-link-exact-active {
  color: var(--color-text);
}

nav a.router-link-exact-active:hover {
  background-color: transparent;
}

nav a {
  display: inline-block;
  padding: 0 1rem;
  border-left: 1px solid var(--color-border);
}

nav a:first-of-type {
  border: 0;
}

@media (min-width: 1024px) {
  header {
    display: flex;
    place-items: center;
    padding-right: calc(var(--section-gap) / 2);
  }

  .logo {
    margin: 0 2rem 0 0;
  }

  header .wrapper {
    display: flex;
    place-items: flex-start;
    flex-wrap: wrap;
  }

  nav {
    text-align: left;
    margin-left: -1rem;
    font-size: 1rem;

    padding: 1rem 0;
    margin-top: 1rem;
  }
}
</style>
