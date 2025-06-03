<template>
  <div>
    <p>{{ msg }}</p>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  name: 'GetAllCharacterData',
  data() {
    return {
      msg: {}
    };
  },
  methods: {
    getAllCharacterData() {
      axios.get('/characters', {
        params: {
          "force_update": false,
          "char_ids": ["146993912", "144768530"]
        },
        paramsSerializer: {
          indexes: null
        },
      })
        .then((res) => {
          console.log(res)
          this.msg = res.data;
        })
        .catch((error) => {
          console.error(error);
        });
    },
  },
  created() {
    this.getAllCharacterData();
  },
};
</script>