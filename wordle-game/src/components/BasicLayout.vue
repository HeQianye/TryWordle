<template>
    <a-layout id="basic-app-layout">
        <a-layout>
            <div class="basic-app-container">
                <word-line
                        v-for="(line, index) in wordLines"
                        :edit-index="letterIndex"
                        :letters="line"
                        :ref="el => { if (el) wordLineRefs[index] = el }"
                ></word-line>
                <key-board @key-press="handleKeyPress"></key-board>
            </div>
        </a-layout>
    </a-layout>
</template>

<script setup>
import {ref, onMounted, onBeforeUnmount} from 'vue';
import WordLine from "@/components/WordLine.vue";
import KeyBoard from "@/components/KeyBoard.vue";

const rowIndex = ref(0);
const letterIndex = ref(0);
const wordLines = ref([['', '', '', '', ''], ['', '', '', '', ''], ['', '', '', '', ''], ['', '', '', '', ''], ['', '', '', '', '']]);
const wordLength = ref(5);
const result = 'hello';
// 创建一个 ref 数组来存储每个 word-line 的引用
const wordLineRefs = ref([]);
// 辅助函数
const moveCursor = (rowDelta, letterDelta) => {
    rowIndex.value += rowDelta;
    letterIndex.value += letterDelta;
};

const clearLastLetter = () => {
    if (letterIndex.value > 0) {
        wordLines.value[rowIndex.value][letterIndex.value - 1] = '';
        letterIndex.value--;
    }
};

const addLetter = (key) => {
    if (letterIndex.value < wordLength.value) {
        wordLines.value[rowIndex.value][letterIndex.value] = key;
        letterIndex.value++;
    }
};

// 主处理函数
const handleKeyPress = (key) => {
    if (key === 'Enter') {
        if (letterIndex.value === wordLength.value) {
            wordLineRefs.value[rowIndex.value].flipCards();
            moveCursor(1, -wordLength.value);
        }
    } else if (key === 'Backspace') {
        clearLastLetter();
    } else {
        addLetter(key);
    }
};

onMounted(() => {
    window.addEventListener('keydown', handleGlobalKeyPress);
});
onBeforeUnmount(() => {
    window.removeEventListener('keydown', handleGlobalKeyPress);
});


const handleGlobalKeyPress = (event) => {
    const key = event.key;
    if (key === 'Enter' || key === 'Backspace' || /^[A-Za-z]$/.test(key)) {
        event.preventDefault(); // 防止默认行为
        let processedKey = '';
        processedKey = key;
        if (key.length === 1) {
            processedKey = key.toUpperCase();
        }
        handleKeyPress(processedKey);
    }
};

function check() {
    return true;
}
</script>

<style lang="less">
@import "@/assets/theme.less";

#app {
    background: #fff;
}

#basic-app-layout {
    width: 100vw;
    height: 100vh;
    overflow: hidden;

    .ant-layout {
        background: #fff;
    }

    .basic-app-container {
        margin: auto;
        width: 500px;
        height: calc(100vh - 48px);
        background-color: #ffffff;
    }
}
</style>
