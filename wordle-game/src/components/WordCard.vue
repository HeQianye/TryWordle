<template>
    <div class="word-cards">
        <a-typography :title="props.data.word">
            <a-typography-title :level="3">{{ props.data.word }}</a-typography-title>
            <span> {{ props.data.pronunciation.replace("\\n", "   ") }}</span>
            <br/>
            <a-typography-text strong>词义:</a-typography-text>
            <a-typography-paragraph>
                <ul v-for="(item, index) in meaningItems" :key="index">
                    <li>
                        {{ item }}
                    </li>
                </ul>
            </a-typography-paragraph>
            <a-typography-text strong>用法:</a-typography-text>
            <a-typography-paragraph>
                <ul v-for="(item, index) in props.data.example.split('\\n').slice(0,2)" :key="index">
                   <li>{{ item }}</li>
                </ul>
            </a-typography-paragraph>
        </a-typography>
    </div>
</template>

<script setup>
import { computed } from 'vue';

const props = defineProps({
    data: {
        type: Object,
        default: () => ({
            word: '',
            pronunciation: '',
            meaning: '',
            example: ''
        })
    }
});

// 计算属性，将 meaning 按照 \n 分割成数组
const meaningItems = computed(() => {
    return props.data.meaning ? props.data.meaning.split("\\n") : [];
});
</script>

<style scoped>
.word-cards {
    max-width: 100%;
    max-height: 100%;
    border-radius: 5px;
    white-space: pre-line;
    overflow: auto;
}
</style>
