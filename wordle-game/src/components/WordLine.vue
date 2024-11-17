<template>
    <a-popover trigger="hover" placement="right" title="Translation">
        <template #content>
            <WordCard/>
        </template>
        <div class="word-line">
            <div
                    class="word-line-item"
                    v-for="(letter, index) in letters"
                    :key="index"
                    :class="{ 'flip-vertical': shouldFlip[index],
                          'green-card': isGreen[index],
                          'yellow-card': isYellow[index]}"
            >
                {{ letter }}
            </div>
        </div>
    </a-popover>
</template>
<script setup lang="ts">
import {ref, onMounted, watch} from 'vue';
import WordCard from "@/components/WordCard.vue";

const props = defineProps({
    editIndex: {
        type: Number,
        default: 0
    },
    letters: {
        type: Array,
        default: () => ['', '', '', '', '']
    }
});

const letters = ref(props.letters);
const shouldFlip = ref(new Array(letters.value.length).fill(false));
const isGreen = ref(new Array(letters.value.length).fill(false));
const isYellow = ref(new Array(letters.value.length).fill(false));

const checkCondition = (index: number): boolean => {
    // 这里可以根据实际需求编写判断逻辑
    return letters.value[index] === 'Y'; // 示例条件：字母为 'Y' 时变为绿色
};


function checkWordleGuess(guess: Array<string>, target: string) {
    if (guess.length !== target.length) {
        throw new Error("猜的单词长度必须与目标单词长度相同");
    }

    const result = [];
    const targetLetters = target.split('');
    const guessLetters = guess.slice(); // 复制 guess 数组以避免修改原始数据

    // 标记已使用的字母
    const usedTargetLetters = new Array(target.length).fill(false);

    // 第一步：检查完全匹配的字母
    for (let i = 0; i < guess.length; i++) {
        if (guessLetters[i] === targetLetters[i]) {
            result.push({ letter: guessLetters[i], status: 'correct' });
            usedTargetLetters[i] = true;
        } else {
            result.push({ letter: guessLetters[i], status: 'absent' });
        }
    }

    // 记录目标单词中每个字母的剩余次数
    const remainingTargetLetters: Record<string, number> = {};
    for (let i = 0; i < target.length; i++) {
        if (!usedTargetLetters[i]) {
            if (!remainingTargetLetters[targetLetters[i]]) {
                remainingTargetLetters[targetLetters[i]] = 0;
            }
            remainingTargetLetters[targetLetters[i]]++;
        }
    }

    // 第二步：检查位置错误但存在于目标单词中的字母
    for (let i = 0; i < guess.length; i++) {
        if (result[i].status === 'absent') {
            if (remainingTargetLetters[guessLetters[i]] && remainingTargetLetters[guessLetters[i]] > 0) {
                result[i].status = 'present';
                remainingTargetLetters[guessLetters[i]]--;
            }
        }
    }

    return result;
}


const flipCards = () => {
    const result = checkWordleGuess(letters.value, 'HELLO'); // 假设目标单词是 'hello'
    shouldFlip.value.forEach((_, index) => {
        setTimeout(() => {
            shouldFlip.value[index] = !shouldFlip.value[index];
            switch (result[index].status) {
                case 'correct':
                    isGreen.value[index] = true;
                    break;
                case 'present':
                    isYellow.value[index] = true;
                    break;
                default:
                    isGreen.value[index] = false;
                    isYellow.value[index] = false;
                    break;
            }
        }, index * 500); // 每个卡片间隔500毫秒翻转
    });
};
defineExpose({flipCards});
</script>

<style scoped lang="less">
.word-line {
    display: flex;
    justify-content: center;
    align-items: center;
    margin-bottom: 10px;
    gap: 10px;

    .word-line-item {
        display: inline-block;
        width: 60px;
        height: 60px;
        overflow: hidden;
        border-radius: 4px;
        background-color: #eee;
        border: #cbcbcb solid 1px;
        text-align: center;
        line-height: 60px;
        font-size: 45px;
        font-weight: bold;
        font-family: 'SFMono-Regular', Consolas, 'Liberation Mono', Menlo, Courier, monospace;
        transition: transform 0.5s ease-in-out, background-color 0.5s ease-in-out;

        &.flip-vertical {
            transform: rotateX(360deg);
        }

        &.green-card {
            background-color: #7dbd2b;
            color: white;
        }

        &.yellow-card {
            background-color: #e5b217;
            color: white;
        }
    }
}
</style>
