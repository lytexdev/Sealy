import { createApp } from "vue"
import { createRouter, createWebHistory } from "vue-router"
import axios from "axios"
import App from "./App.vue"

axios.defaults.withCredentials = true
const app = createApp(App)
const routes = [
]

const router = createRouter({
	history: createWebHistory(),
	routes,
})

app.use(router)
app.mount("#app")
