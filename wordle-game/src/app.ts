import { message } from "ant-design-vue";

export class App {
    static showMessage(msg: string) {
        message.info({
            content: msg,
            duration: 0.5,
            class: 'message-box',
            style: {
                marginTop: '50vh',
            }
        });
    }
}
