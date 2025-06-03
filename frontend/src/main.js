import './assets/main.css'

import { createApp } from 'vue'
import App from './App.vue'
import router from './router'

const app = createApp(App)
// axios.defaults.withCredentials = true;
// axios.defauls.baseURL = 'http://127.0.0.1:8998';
app.use(router)
app.mount('#app')
