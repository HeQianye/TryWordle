import { createApp } from 'vue';
import antd from 'ant-design-vue';
import AppComponent from '@/App.vue';


let vue = createApp(AppComponent);
vue.use(antd);
app.vue = vue;
vue.mount("#app");
