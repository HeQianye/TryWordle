import { defineConfig } from 'vite';
import vue from '@vitejs/plugin-vue';
import path from 'path';

// https://vite.dev/config/

/**
 * 将给定的目录路径与当前脚本所在目录路径进行合并，以获取绝对路径。
 *
 * @param dir 相对路径或目录名，将与当前脚本所在目录路径合并。
 * @returns 返回合并后的绝对路径。
 */
function resolve(dir: string): string {
    return path.join(__dirname, dir);
}



// 定义是否使用远程服务的常量
const useRemote = false;

// 根据是否使用远程服务来决定是否使用HTTPS
const useHttps = useRemote ? false : false;

// 定义远程代理的URL，根据是否使用远程服务来选择不同的地址
const proxyRemote = useRemote ? "localhost:5000" : "127.0.0.1:5000";

// 导出一个定义配置的函数
export default defineConfig({
    // 根据环境变量来设置基础路径
    base: process.env.NODE_ENV === "production" ? "/manage/" : "/",
    // 使用Vue插件
    plugins: [vue()],
    build: {
        // 设置目标浏览器版本，以确保兼容性
        target: ["edge90", "chrome90", "firefox90", "safari15"], // 2021年以后的浏览器均可使用
    },
    css: {
        // preprocessorOptions: {
        //     less: {
        //         // 在Less文件中不使用字符集声明
        //         charset: false,
        //         // 在每个Less文件开始时自动添加全局样式
        //         additionalData: '@import "@/assets/mixin.less";',
        //     },
        // },
    },
    resolve: {
        // 设置模块路径别名，以简化长路径的引用
        alias: [
            {
                find: "@",
                replacement: resolve("src"),
            },
        ],
    },
    server: {
        // 配置开发服务器的代理
        proxy: {
            "/api": {
                // 根据是否使用HTTPS来设置目标URL
                target: `${useHttps ? "https" : "http"}://${proxyRemote}`,
                // 更改请求的来源地址
                changeOrigin: true,
                // 忽略SSL证书验证
                secure: false,
                rewrite: (path) => path.replace(/^\/api/, ''),
            },
            "/signalr": {
                // 配置WebSocket代理
                target: `${useHttps ? "wss" : "ws"}://${proxyRemote}`,
                changeOrigin: true,
                // 启用WebSocket支持
                ws: true,
                secure: false,
            },
            "/debug": {
                // 配置调试接口的代理
                target: `${useHttps ? "https" : "http"}://${proxyRemote}`,
                changeOrigin: true,
                secure: false,
            },
            "/permanent": {
                // 配置持久化接口的代理
                target: `${useHttps ? "https" : "http"}://${proxyRemote}`,
                changeOrigin: true,
                secure: false,
            },
        },
    },
});
