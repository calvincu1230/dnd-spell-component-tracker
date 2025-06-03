import 'bootstrap/dist/css/bootstrap.css';
import { createApp } from "vue";
import axios from 'axios';

import App from './App.vue';
import router from './router';

const app = createApp(App);

axios.defaults.withCredentials = true;
axios.defaults.baseURL = 'http://127.0.0.1:8998';  // FastAPI backend

app.use(router);
app.mount("#app");