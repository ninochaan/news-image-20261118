// News-image entry: the 18 November 2026 broadsheet, pre-rendered.
// The program runs with no network, so it ships the image the repository
// already holds: it reads entry.png from beside this file and writes the
// same bytes to the output directory. The image is located relative to
// this file, never relative to the process working directory, because the
// grader may invoke the program from anywhere.
//
// Local run: mkdir -p out && MAKEFUN_OUTPUT_DIR=out node main.ts

import { mkdirSync, readFileSync, writeFileSync } from "node:fs";
import { dirname, join } from "node:path";
import { fileURLToPath } from "node:url";

function main(): void {
  const here = dirname(fileURLToPath(import.meta.url));
  const pixels = readFileSync(join(here, "entry.png"));
  if (pixels.length === 0) {
    throw new Error("entry.png beside main.ts is empty");
  }
  const target = process.env.MAKEFUN_OUTPUT_DIR ?? "/output";
  mkdirSync(target, { recursive: true });
  writeFileSync(join(target, "entry.png"), pixels);
}

main();
