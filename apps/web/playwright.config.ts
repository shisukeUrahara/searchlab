import { defineConfig } from "@playwright/test";

export default defineConfig({
  testDir: "./e2e",
  use: { baseURL: "http://localhost:3000" },
  // Expects the API on :8000 and the web app on :3000 (see README / docker-compose).
});
