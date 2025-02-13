<template>
    <div>
        <h2>Login</h2>
        <form @submit.prevent="handleLogin">
            <div>
                <label>Username:</label>
                <input v-model="username" type="text" required>
            </div>
            <div>
                <label>Password:</label>
                <input v-model="password" type="password" required>
            </div>
            <button type="submit">Login</button>
        </form>
        <p v-if="message">{{ message }}</p>
    </div>
</template>

<script setup>
import { ref } from 'vue'
import axios from 'axios'
import { useRouter } from 'vue-router'

const username = ref('')
const password = ref('')
const message = ref('')
const router = useRouter()

const handleLogin = async () => {
    try {
        const response = await axios.post('/api/login', {
            username: username.value,
            password: password.value
        })
        localStorage.setItem('access_token', response.data.access_token)
        router.push('/chat')
    } catch (error) {
        message.value = error.response?.data?.msg || 'Login failed'
    }
}
</script>
