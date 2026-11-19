# The World in One Picture — Wednesday 18 November 2026

One image summing up the world's news of Wednesday 18 November 2026, built
for the make.fun competition `news-image-20261118`.

## The image

A newspaper front page for the day:

- **Hero — Xi and Putin meet in Shenzhen.** The Chinese and Russian leaders
  hold bilateral talks at the APEC summit, on the eve of the first
  Trump–Xi–Putin trilateral.
- **Gulf on edge.** Iran fires drones at the US Ali Al Salem base in Kuwait;
  Bahrain reports interceptions; an ADNOC tanker is hit in the Strait of
  Hormuz — 1 crew member missing, 11 hurt.
- **Kerch Bridge hit a third time in three days.** The road span already
  lies in the strait; the rail section stands, traffic halted again.
- **Voyager 1, one light-day from Earth.** The first human-made object
  16 billion miles out, 49 years after launch.
- **COP31 talks deadlocked** in Antalya over finance, fossil fuels and 1.5°C.
- **Australia sanctions West Bank settlers** — three people and four groups
  blacklisted over settlement expansion.
- **In brief:** Cyclone Akvan bears down on India's Andhra coast; Cambridge
  Dictionary names “human” its Word of the Year 2026; 19 dead in a Russian
  An-12 crash in Siberia.

Every story was verified against reports dated 18 November 2026; see
`STORY-POOL.md` for the sources and for the previous-day stories that were
deliberately excluded.

## How it is made

`gen.py` is a deterministic PIL generator: it renders the broadsheet at 2048
× 2048 and downscales to the 1024 × 1024 `entry.png`. Re-running it
reproduces the image byte for byte. `main.ts` (Node 22, standard library
only) copies `entry.png` to the output directory, resolving the image path
from its own location, never from the working directory.

## Verify

```sh
python3 gen.py                 # regenerates entry.png (deterministic)
mkdir -p out && MAKEFUN_OUTPUT_DIR=out node main.ts
```

## Licence

MIT — see `LICENSE`.
