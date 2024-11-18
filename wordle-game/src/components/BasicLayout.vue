<template>
    <a-layout id="basic-app-layout">
        <div class="basic-app-header">
            <a-flex align="center" justify="space-between" class="title" horizontal>
                <a-button class="white" type="primary" @click="giveUp">
                    GIVE UP
                </a-button>
                <div class="basic-app-title">
                    TRY WORDLE
                </div>
                <a-button class="white" type="primary" @click="settingsVisible = true">
                    SETTING
                </a-button>
            </a-flex>
        </div>
        <a-layout>
            <div class="basic-app-container">
                <word-line
                        v-for="(line, index) in wordLines"
                        :edit-index="letterIndex"
                        :letters="line"
                        :ref="el => { if (el) wordLineRefs[index] = el }"
                        :result="result"
                ></word-line>
                <key-board @key-press="handleKeyPress" ref="keyboardRef"></key-board>
            </div>
        </a-layout>
    </a-layout>
    <a-modal v-model:open="settingsVisible" title="Settings" @ok="applySettings">
        <a-form>
            <a-form-item label="Word Length">
                <a-select v-model:value="selectedWordLength" style="width: 120px">
                    <a-select-option v-for="length in [3, 4, 5, 6, 7, 8, 9, 10]" :key="length" :value="length">
                        {{ length }}
                    </a-select-option>
                </a-select>
            </a-form-item>
            <a-form-item label="Max Try">
                <a-input-number v-model:value="selectedMaxTry" :min="1" :max="10" style="width: 120px"></a-input-number>
            </a-form-item>
        </a-form>
    </a-modal>
</template>

<script setup>
import {ref, onMounted, onBeforeUnmount} from 'vue';
import WordLine from "@/components/WordLine.vue";
import KeyBoard from "@/components/KeyBoard.vue";
import {axios} from "@/axios.js";
import {Modal} from "ant-design-vue";
import {App} from "@/app";
const wordLength = ref(5);
const maxTry = ref(6);
const rowIndex = ref(0);
const letterIndex = ref(0);
const wordLines = ref(getEmptyMatrix(maxTry.value, wordLength.value));
const result = ref('');
const keyboardRef = ref(null);
// 创建一个 ref 数组来存储每个 word-line 的引用
const wordLineRefs = ref([]);
const selectedWordLength = ref(wordLength.value);
const selectedMaxTry = ref(maxTry.value);
const settingsVisible = ref(false);
const applySettings = () => {
    wordLength.value = selectedWordLength.value;
    maxTry.value = selectedMaxTry.value;
    restart();
    settingsVisible.value = false;
};



async function getWord() {
    axios.get('/api/get_word', {
        params: {length: wordLength.value}
    }).then(data => {
        result.value = data.data.word;
        console.log(result);
    });
}

function getEmptyMatrix(row, col) {
    return Array.from({length: row}, () => Array(col).fill(''));
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
                keyboardRef.value.handleColor(res.checkResult);
                moveCursor(1, -wordLength.value);
                if (res.isWin) {
                    //确认后 reload
                    Modal.success({
                        title: "CONGRATULATION!!",
                        content: `You win, the answer is ${result.value}`,
                    });
                    restart();
                }
                if (rowIndex.value === maxTry.value) {
                    Modal.error({
                        title: 'FAILURE',
                        content: `You lost, the answer is ${result.value}`,
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
    wordLines.value = getEmptyMatrix(maxTry.value, wordLength.value);
    getWord();
    for (let i = 0; i < wordLineRefs.value.length; i++) {
        wordLineRefs.value[i].reset();
    }
    keyboardRef.value.reset();
}

function reload() {
    window.location.reload();
}
function giveUp() {
    App.showMessage(result.value);
    restart();
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
    //width: 100vw;
    //height: 100vh;

    .basic-app-header {
        display: flex;
        justify-content: space-between;
        align-items: center;
        padding: 0 24px;
        height: 48px;
        background: #fff;
        border-bottom: 1px solid #f0f0f0;

        .title {
            width: calc(600px);
            margin: auto;
        }

        .basic-app-title {
            font-size: 24px;
            font-weight: bold;
            color: #000000;
        }
    }

    .ant-layout {
        background: #fff;
    }

    .basic-app-container {
        margin: auto;
        width: 500px;
        height: calc(100vh - 48px);
        background-color: #ffffff;
        margin-top: 10px;
    }
}


</style>
