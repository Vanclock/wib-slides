# wib-slides
Public image host and slide generator for World in Brief Daily (Instagram carousel).
- `tools/setup.sh` installs dependencies; `tools/gen_slides.py spec.json` renders 1080x1350 JPG slides (see `examples/spec-example.json`).
- Each day's slides go in `YYYY-MM-DD/01.jpg ... 08.jpg` and are served at `https://raw.githubusercontent.com/Vanclock/wib-slides/main/YYYY-MM-DD/NN.jpg`.

## Roma sem sentido (@romasemsentido)
`tools/gen_rome.py spec.json` renders the Portuguese Rome carousel (`rs-NN.jpg`, cream/terracotta style). See `examples/spec-rome-example.json`. Rome slides are published under `rome/YYYY-MM-DD/NN.jpg`.
