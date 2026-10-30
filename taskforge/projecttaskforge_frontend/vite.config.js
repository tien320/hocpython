import { defineConfig } from "vite";

export default defineConfig({
  server: {
    allowedHosts: ["path-dedicator-wise.ngrok-free.dev"],
    proxy: {
      "/api/v1": {
        target: "http://127.0.0.1:8000",
        changeOrigin: true,
      },
    },
  },
});
