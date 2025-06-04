<script setup>
const props = defineProps({
  campaignData: Object,
  characterData: Object,
  getOneCharactersData: Function
})
</script>

<template>
  <div class="greetings">
    <h1 class="green">{{ campaignData?.name || "Derngerns ern Dergens" }}</h1>
    <ul v-for="(value, key) in characterData" :key="key">
        <button @click="getOneCharactersData(key, true)">{{ value.name }}</button>
    </ul>
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
</style>