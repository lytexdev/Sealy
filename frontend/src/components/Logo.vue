<template>
    <div class="logo">
        <img class="logo-image" :src="logoUrl" alt="Sealy logo" height="64px" width="64px">
        <h1>{{ title }}</h1>
    </div>
</template>

<script setup>
import { defineProps } from 'vue'

const props = defineProps({
    title: String
})
const logoUrl = '/static/logo.svg'
</script>
