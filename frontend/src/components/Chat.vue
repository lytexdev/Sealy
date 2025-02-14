<template>
    <div>
        <h2>Chat with {{ recipientName }}</h2>
        <div>
            <textarea v-model="messageText" placeholder="Type your message"></textarea>
            <button @click="sendMessage">Send</button>
        </div>
        <div v-for="(msg, index) in messages" :key="index">
            <p>{{ msg }}</p>
        </div>
    </div>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue'
import axios from 'axios'
import { useRoute } from 'vue-router'
import { useSocket } from '../composables/useSocket'
import { encryptMessage, decryptMessage } from '../services/cryptoService'

const route = useRoute()
const recipientSlug = route.params.recipientSlug

const slugParts = recipientSlug.split('-')
const recipientId = parseInt(slugParts.pop())
const recipientName = slugParts.join(' ')

const socket = useSocket()
const messageText = ref('')
const messages = ref([])

const currentUserId = localStorage.getItem('user_id')
if (currentUserId) {
    socket.emit('join', { user_id: currentUserId })
}

const loadMessageHistory = async () => {
    try {
        const token = localStorage.getItem('access_token')
        const response = await axios.get(`/api/messages/${recipientId}`, {
            headers: { Authorization: `Bearer ${token}` }
        })
        for (const msg of response.data) {
            try {
                const plaintext = await decryptMessage(msg.ciphertext, msg.iv)
                messages.value.push(`${msg.sender_id == currentUserId ? 'Me' : recipientName}: ${plaintext}`)
            } catch (err) {
                console.error('Decryption error for stored message', err)
            }
        }
    } catch (error) {
        console.error('Failed to load message history', error)
    }
}

const sendMessage = async () => {
    if (messageText.value.trim() === '') return
    const { ciphertext, iv } = await encryptMessage(messageText.value)
    socket.emit('send_message', {
        sender_id: currentUserId,
        recipient_id: String(recipientId),
        message: ciphertext,
        iv: iv
    })
    messages.value.push(`Me: ${messageText.value}`)
    messageText.value = ''
}

onMounted(async () => {
    await loadMessageHistory()
    socket.on('receive_message', async data => {
        try {
            if (String(data.sender_id) === String(recipientId) || String(data.recipient_id) === String(recipientId)) {
                const plaintext = await decryptMessage(data.message, data.iv)
                messages.value.push(`${data.sender_id == currentUserId ? 'Me' : recipientName}: ${plaintext}`)
            }
        } catch (err) {
            console.error('Decryption error', err)
        }
    })
})
</script>
