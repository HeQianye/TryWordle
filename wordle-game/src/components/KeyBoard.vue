<template>
    <!-- 虚拟键盘 -->
    <div class="keyboard">
        <a-space class="keyboard-row" v-for="(row, index) in keyboardRows" :key="row[0]+index">
            <a-button
                :class="['keyboard-key', 'white',
                { 'green': keyStatusMap.get(key)==='green'},
                { 'yellow': keyStatusMap.get(key)==='yellow'},
                { 'gray': keyStatusMap.get(key)==='gray'}
                ]"
                type="primary"
                size="large"
                v-for="key in row"
                :key="key"
                @click="handleKeyPress(key)"
            >
                {{ key }}
            </a-button>
        </a-space>
    </div>
</template>

<script setup lang="ts">
import { ref } from 'vue';
import { defineEmits } from 'vue';

// 定义键盘的每一行
const keyboardRows = ref([
    ['Q', 'W', 'E', 'R', 'T', 'Y', 'U', 'I', 'O', 'P'],
    ['A', 'S', 'D', 'F', 'G', 'H', 'J', 'K', 'L'],
    ['↵','Z', 'X', 'C', 'V', 'B', 'N', 'M','Del']
]);

const keyStatusMap = ref(new Map([
        ['A', 'default'],
        ['B', 'default'],
        ['C', 'default'],
        ['D', 'default'],
        ['E', 'default'],
        ['F', 'default'],
        ['G', 'default'],
        ['H', 'default'],
        ['I', 'default'],
        ['J', 'default'],
        ['K', 'default'],
        ['L', 'default'],
        ['M', 'default'],
        ['N', 'default'],
        ['O', 'default'],
        ['P', 'default'],
        ['Q', 'default'],
        ['R', 'default'],
        ['S', 'default'],
        ['T', 'default'],
        ['U', 'default'],
        ['V', 'default'],
        ['W', 'default'],
        ['X', 'default'],
        ['Y', 'default'],
        ['Z', 'default'],
        ['↵', 'default'],
        ['Del', 'default']
    ]
));
// 定义 emit 事件
const emit = defineEmits(['key-press']);

function handleColor(result: any[]) {
    console.log(result);
    console.log(keyStatusMap.value);

    for (let i = 0; i < result.length; i++) {
        const { letter, status } = result[i];
        switch (status) {
            case 'correct':
                keyStatusMap.value.set(letter, 'green');
                break;
            case 'present':
                if (keyStatusMap.value.get(letter) !== 'green') {
                    keyStatusMap.value.set(letter, 'yellow');
                }
                break;
            case 'absent':
                keyStatusMap.value.set(letter, 'gray');
                break;
            default:
                console.warn(`Unknown status: ${status}`);
                break;
        }
    }
}

function reset() {
    keyStatusMap.value.clear();
    // 重新设置默认状态
    keyboardRows.value.forEach(row => {
        row.forEach(key => {
            keyStatusMap.value.set(key, 'default');
        });
    });
}
// 获取按键的类名
const getKeyClass = (key: string) => {
    return keyStatusMap.value.get(key) || 'default';
};
// 处理按键事件
const handleKeyPress = (key: string) => {
    // 特殊按键处理
    if (key === '↵') {
        key = 'Enter';
    } else if (key === 'Del') {
        key = 'Backspace';
    }
    emit('key-press', key);
};

defineExpose({
    handleColor,
    reset
})
</script>


<style scoped lang="less">
.keyboard {
    padding-top:20px;
    display: flex;
    flex-direction: column;
    justify-content: center;
}
.keyboard-key {
    width: 50px;
    height: 60px;
    font-size: 24px;
}
.keyboard-row {
    margin-top: 10px;
    margin-bottom: 10px;
    display: flex;
    justify-content: center;
}
.color-disabled() {
  color: rgba(0, 0, 0, 0.25)!important;
  background-color: #f5f5f5!important;
  border-color: #d9d9d9!important;
  pointer-events: none;
  cursor: not-allowed;
}

.ant-btn {
    &.white {
        &, &:active, &.active {
            color: #5d5d5d !important;
            font-weight: bold;
            box-shadow: none !important;
            background-color: #E1EAF4 !important;
            border-color: #E1EAF4 !important;
        }

        &:hover, &:focus {
            background-color: #cfd4d9 !important;
            border-color: #cfd4d9 !important;
        }

        &[disabled] {
            .color-disabled();
        }
    }
    &.green {
        &, &:active, &.active {
            color: #fff !important;
            background-color: #7dbd2b !important;
            border-color: #7dbd2b !important;
            box-shadow: none !important;
        }
        &:hover, &:focus {
            background-color: #a2d265 !important;
            border-color: #a2d265 !important;
        }
        &[disabled] {
            .color-disabled();
        }
    }
    &.yellow {
        &, &:active, &.active {
            color: #fff !important;
            background-color: #f4b400 !important;
            border-color: #f4b400 !important;
            box-shadow: none !important;
        }
        &:hover, &:focus {
            background-color: #f5c94d !important;
            border-color: #f5c94d !important;
        }
        &[disabled] {
            .color-disabled();
        }
    }
    &.gray{
        &, &:active, &.active {
            color: #fff !important;
            background-color: #9e9e9e !important;
            border-color: #9e9e9e !important;
            box-shadow: none !important;
        }
        &:hover, &:focus {
            background-color: #bdbdbd !important;
            border-color: #bdbdbd !important;
        }
        &[disabled] {
            .color-disabled();
        }
    }
}
</style>
