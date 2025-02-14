import { createApp } from "vue";
import { createRouter, createWebHistory } from "vue-router";
import axios from "axios";
import { io } from "socket.io-client";
import App from "./App.vue";
import Register from "./components/Register.vue";
import Login from "./components/Login.vue";
import UserList from "./components/UserList.vue";
import Chat from "./components/Chat.vue";

axios.defaults.withCredentials = true;

const socket = io(window.location.origin, {
  withCredentials: true,
});

const routes = [
  { path: "/", redirect: "/users" },
  { path: "/register", component: Register },
  { path: "/login", component: Login },
  { path: "/users", component: UserList, name: "UserList" },
  { path: "/chat/:recipientSlug", component: Chat, name: "Chat", props: true },
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

const app = createApp(App);

app.config.globalProperties.$socket = socket;

app.use(router);
app.mount("#app");
