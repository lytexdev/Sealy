<template>
    <div>
        <h2>Register</h2>
        <form @submit.prevent="handleRegister">
            <div>
                <label>Username:</label>
                <input v-model="username" type="text" required>
            </div>
            <div>
                <label>Email:</label>
                <input v-model="email" type="email" required>
            </div>
            <div>
                <label>Password:</label>
                <input v-model="password" type="password" required>
            </div>
            <button type="submit">Register</button>
        </form>
        <p v-if="message">{{ message }}</p>
    </div>
</template>

<script setup>
import { ref } from 'vue'
import axios from 'axios'
import { useRouter } from 'vue-router'

const username = ref('')
const email = ref('')
const password = ref('')
const message = ref('')
const router = useRouter()

const handleRegister = async () => {
    try {
        const response = await axios.post('/api/register', {
            username: username.value,
            email: email.value,
            password: password.value
        })
        message.value = response.data.msg
        router.push('/login')
    } catch (error) {
        message.value = error.response?.data?.msg || 'Registration failed'
    }
}
</script>
