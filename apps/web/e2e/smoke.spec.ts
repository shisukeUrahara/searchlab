import AxeBuilder from "@axe-core/playwright";
import { expect, test, type Page } from "@playwright/test";

const PAGES = ["/", "/map", "/eval", "/queries", "/sources"];

async function cannotScrollSideways(page: Page) {
  const x = await page.evaluate(() => {
    window.scrollTo(400, window.scrollY);
    return window.scrollX;
  });
  expect(x).toBe(0);
}

test("suggestion chip only fills the box; Search runs the query", async ({ page }) => {
  await page.goto("/");
  const chip = page.getByRole("group", { name: "Example queries" }).getByRole("button").first();
  const text = (await chip.textContent())?.trim() ?? "";
  await chip.click();
  await expect(page.getByRole("textbox", { name: "Question or identifier" })).toHaveValue(text);
  await expect(page.getByText("No search yet")).toBeVisible();
  await page.getByRole("button", { name: "Search", exact: true }).click();
  const verdict = page.getByText(/Expected passage (at rank \d+|not in these results)/).filter({ visible: true });
  await expect(verdict.first()).toBeVisible();
});

test("search shows three methods and opens a passage", async ({ page, isMobile }) => {
  await page.goto("/?q=" + encodeURIComponent("KDP D JCL update requirements"));
  if (isMobile) {
    for (const tab of ["BM25", "Dense", "Hybrid"]) await expect(page.getByRole("tab", { name: tab })).toBeVisible();
  } else {
    for (const name of ["BM25 (keyword)", "Dense (vector)", "Hybrid (RRF)"]) {
      await expect(page.getByRole("region", { name })).toBeVisible();
    }
  }
  await page.getByRole("region", { name: "Hybrid (RRF)" }).getByRole("button").first().click();
  const dialog = page.getByRole("dialog", { name: "Passage detail" });
  await expect(dialog).toBeVisible();
  await expect(dialog.getByRole("link", { name: /Open source/ })).toBeVisible();
  await page.keyboard.press("Escape");
  await expect(dialog).toBeHidden();
});

test("queries paginate and filter by class", async ({ page }) => {
  await page.goto("/queries");
  await expect(page.getByText(/Showing 1–15 of 80 holdout queries/)).toBeVisible();
  await page.getByLabel("Next page").click();
  await expect(page.getByText(/Showing 16–30 of 80/)).toBeVisible();
  await page.getByRole("button", { name: /^Exact identifier/ }).click();
  await expect(page.getByText(/of 27 holdout queries/)).toBeVisible();
  await page.getByRole("tab", { name: /Tuning set/ }).click();
  await expect(page.getByText(/of 13 tuning queries/)).toBeVisible(); // class filter is kept
  await page.getByRole("button", { name: /^All/ }).click();
  await expect(page.getByText(/of 40 tuning queries/)).toBeVisible();
});

test("vector map renders and a query lights up hits", async ({ page }) => {
  await page.goto("/map?q=" + encodeURIComponent("software peer review checklist"));
  await expect(page.getByText("Hybrid top hits")).toBeVisible();
  await expect(page.locator("canvas").first()).toBeVisible();
  await page.getByText("Hybrid top hits").locator("..").getByRole("button").first().click();
  await expect(page.getByRole("region", { name: "Passage inspector" })).toBeVisible();
});

test("evaluation dashboard shows charts and metrics", async ({ page }) => {
  await page.goto("/eval");
  await expect(page.getByText("Head to head")).toBeVisible();
  await expect(page.getByText("MRR@10").first()).toBeVisible();
  await expect(page.locator(".recharts-surface").first()).toBeVisible();
});

test("theme toggle switches to dark and persists", async ({ page }) => {
  await page.goto("/sources");
  const html = page.locator("html");
  const before = await html.getAttribute("class");
  await page.getByRole("button", { name: "Toggle dark mode" }).click();
  await expect.poll(async () => (await html.getAttribute("class"))?.includes("dark")).toBe(!before?.includes("dark"));
  await page.reload();
  await expect.poll(async () => (await html.getAttribute("class"))?.includes("dark")).toBe(!before?.includes("dark"));
});

test("API failure shows a clear error", async ({ page }) => {
  await page.route("**/search", (r) => r.abort());
  await page.goto("/");
  await page.getByRole("textbox", { name: "Question or identifier" }).fill("anything");
  await page.getByRole("button", { name: "Search", exact: true }).click();
  await expect(page.getByRole("alert").filter({ hasText: "network_error" })).toBeVisible();
});

for (const path of PAGES) {
  for (const scheme of ["light", "dark"] as const) {
    test(`${path} (${scheme}): no sideways scroll, no serious a11y issues`, async ({ page }) => {
      await page.emulateMedia({ colorScheme: scheme });
      await page.goto(path);
      await page.waitForLoadState("networkidle");
      await cannotScrollSideways(page);
      const result = await new AxeBuilder({ page }).withTags(["wcag2a", "wcag2aa"]).exclude("canvas").analyze();
      const serious = result.violations.filter((v) => v.impact === "serious" || v.impact === "critical");
      expect(serious.map((v) => `${v.id}: ${v.nodes.length} node(s) e.g. ${v.nodes[0]?.target}`)).toEqual([]);
    });
  }
}
