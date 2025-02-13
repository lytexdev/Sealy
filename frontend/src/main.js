import { createApp } from "vue";
import { createRouter, createWebHistory } from "vue-router";
import axios from "axios";
import { io } from "socket.io-client";
import App from "./App.vue";
import Register from "./components/Register.vue";
import Login from "./components/Login.vue";
import Chat from "./components/Chat.vue";

axios.defaults.withCredentials = true;

const socket = io("http://localhost:5000", {
  withCredentials: true,
});

const routes = [
  { path: "/", redirect: "/login" },
  { path: "/register", component: Register },
  { path: "/login", component: Login },
  { path: "/chat", component: Chat },
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

const app = createApp(App);

app.config.globalProperties.$socket = socket;

app.use(router);
app.mount("#app");
