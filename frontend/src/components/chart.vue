<script>
import axios from 'axios';
    defineProps({
        campagnTitle,
        characterData,
    })
</script>
<template>
    <div class="chart">
        <h1 class="chart-header">{{ campaignTitle }}</h1>
    </div>
</template>