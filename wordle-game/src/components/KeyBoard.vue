<template>
    <!-- 虚拟键盘 -->
    <div class="keyboard">
        <a-space class="keyboard-row" v-for="(row, index) in keyboardRows" :key="index">
            <a-button 
                class="keyboard-key gray"
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

// 定义 emit 事件
const emit = defineEmits(['key-press']);

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
    &.gray {

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
}
</style>
