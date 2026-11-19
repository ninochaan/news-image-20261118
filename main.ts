// A working news-image entry (Node 22, standard library only): its image is the
// entry.png beside this file, and the program copies it to /output/entry.png.
// The image path is resolved from this file's own location, never from the
// working directory: the grader runs `node /bot/main.ts` from elsewhere.
//
// Outside the grader's container, MAKEFUN_OUTPUT_DIR stands in for /output:
//   mkdir -p out && MAKEFUN_OUTPUT_DIR=out node main.ts

import { copyFileSync, existsSync, mkdirSync } from "node:fs";
import { join } from "node:path";

const outDir = process.env.MAKEFUN_OUTPUT_DIR ?? "/output";
mkdirSync(outDir, { recursive: true });
const src = new URL("./entry.png", import.meta.url);
if (!existsSync(src)) throw new Error("entry.png is missing beside main.ts");
copyFileSync(src, join(outDir, "entry.png"));
