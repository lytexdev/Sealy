<template>
    <div>
        <h2>User List</h2>
        <ul>
            <li v-for="user in users" :key="user.id">
                <a @click="selectUser(user)">{{ user.username }}</a>
            </li>
        </ul>
    </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import axios from 'axios'
import { useRouter } from 'vue-router'

const users = ref([])
const router = useRouter()

const fetchUsers = async () => {
    try {
        const token = localStorage.getItem('access_token')
        const response = await axios.get('/api/users', {
            headers: { Authorization: `Bearer ${token}` }
        })
        users.value = response.data
    } catch (error) {
        console.error('Failed to fetch users', error)
    }
}

const selectUser = (user) => {
    const slug = `${user.username.toLowerCase().replace(/\s+/g, '-')}-${user.id}`
    router.push({ name: 'Chat', params: { recipientSlug: slug } })
}

onMounted(() => {
    fetchUsers()
})
</script>
