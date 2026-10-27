import { expect, test } from "@playwright/test";

test("search shows three columns, opens a chunk, closes with Esc", async ({ page }) => {
  await page.goto("/");
  await page.getByLabel("Question or error string").fill("X-Hub-Signature-256");
  await page.getByRole("button", { name: "Search" }).click();

  for (const name of ["BM25 (keyword)", "Dense (vector)", "Hybrid (RRF)"]) {
    await expect(page.getByRole("region", { name })).toBeVisible();
  }
  await page.getByRole("region", { name: "BM25 (keyword)" }).getByRole("button").first().click();
  await expect(page.getByRole("dialog", { name: "Chunk detail" })).toBeVisible();
  await page.keyboard.press("Escape");
  await expect(page.getByRole("dialog")).toBeHidden();
});

test("labeled query shows expected-chunk verdict", async ({ page }) => {
  await page.goto("/queries");
  await page.getByRole("link", { name: /per_page/ }).first().click();
  await expect(page.getByText(/Expected chunk (found at rank \d+|not in these results)/).first()).toBeVisible();
});

test("eval page lists the committed runs", async ({ page }) => {
  await page.goto("/eval");
  await expect(page.getByRole("table").first()).toBeVisible();
  await expect(page.getByText("Recall@5").first()).toBeVisible();
});

test("API down shows a clear error, not a blank page", async ({ page }) => {
  await page.route("**/search", (r) => r.abort());
  await page.goto("/");
  await page.getByLabel("Question or error string").fill("anything");
  await page.getByRole("button", { name: "Search" }).click();
  await expect(page.getByRole("alert").filter({ hasText: "network_error" })).toBeVisible();
});
