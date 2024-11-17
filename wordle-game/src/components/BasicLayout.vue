<template>
    <a-layout id="basic-app-layout">
        <a-layout>
            <div class="basic-app-container">
                <word-line
                        v-for="(line, index) in wordLines"
                        :edit-index="letterIndex"
                        :letters="line"
                        :ref="el => { if (el) wordLineRefs[index] = el }"
                        :result="result"
                ></word-line>
                <a-button type="primary" @click="">Test</a-button>
                <key-board @key-press="handleKeyPress" ref="keyboard"></key-board>
            </div>
        </a-layout>
    </a-layout>
</template>

<script setup>
import {ref, onMounted, onBeforeUnmount} from 'vue';
import WordLine from "@/components/WordLine.vue";
import KeyBoard from "@/components/KeyBoard.vue";
import {axios} from "@/axios.js";
import {Modal} from "ant-design-vue";
import {App} from "@/app";

const rowIndex = ref(0);
const letterIndex = ref(0);
const wordLines = ref([['', '', '', '', ''], ['', '', '', '', ''], ['', '', '', '', ''], ['', '', '', '', ''], ['', '', '', '', '']]);
const wordLength = ref(5);
const maxTry = ref(5);
const result = ref('');
const keyboard = ref(null);
// 创建一个 ref 数组来存储每个 word-line 的引用
const wordLineRefs = ref([]);


async function getWord() {
    axios.get('/api/get_word', {
        params: {length: wordLength.value}
    }).then(data => {
        result.value = data.data.word;
        console.log(result);
    });
}



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
const handleKeyPress = async (key) => {

    if (key === 'Enter') {
        if (letterIndex.value === wordLength.value) {
            let res = await wordLineRefs.value[rowIndex.value].flipCards();
            if (res.success) {
                keyboard.value.handleColor(res.checkResult);
                moveCursor(1, -wordLength.value);
                if (res.isWin) {
                    //确认后 reload
                    Modal.success({
                        title: '恭喜',
                        content: '你赢啦',
                    });
                    restart();
                }
                if (rowIndex.value === maxTry.value) {
                    Modal.error({
                        title: '失败',
                        content: `你输啦，正确答案是${result.value}`,
                    })
                    restart();
                }
            }
        }
    } else if (key === 'Backspace') {
        clearLastLetter();
    } else {
        addLetter(key);
    }
};

function restart() {
    rowIndex.value = 0;
    letterIndex.value = 0;
    wordLines.value = [['', '', '', '', ''], ['', '', '', '', ''], ['', '', '', '', ''], ['', '', '', '', ''], ['', '', '', '', '']];
    getWord();
    for (let i = 0; i < wordLineRefs.value.length; i++) {
        wordLineRefs.value[i].reset();
    }
    keyboard.value.reset();
}

function reload() {
    window.location.reload();
}

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

onMounted(() => {
    getWord();
})
</script>

<style lang="less">
@import "@/assets/theme.less";
@import "@/assets/message.less";
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
