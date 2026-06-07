# Kumiko Generator & Dashboard

This project is an enhanced fork of the original [hampusudd/kumiko_generator](https://github.com/hampusudd/kumiko_generator). While the core engine processes images into stunning **Kumiko-style geometric SVG panels**, this fork introduces a **modern, fully-containerized Web Dashboard** to configure, preview, and download your designs instantly without touching the command line.

The generated SVG outputs are perfectly optimized for **3D printing (such as MakerWorld/Bambu Lab grids), CNC, or laser cutting**.

---

## 🚀 New Features in this Fork

j **Web UI Dashboard:** A dark-themed, sleek interface to upload images and tweak parameters on the fly.
* **Live High-Definition Preview & Spinner:** Inspect your generated Kumiko pattern matrix directly in your browser with a smooth loading animation.
* **Dynamic Configuration:** Adjust grid dimensions, orientation, and colors visually using native color pickers.
* **Multi-language Support (i18n):** Fully translated into **English**, **Français**, and **Deutsch** with an easy-to-extend JSON translation file.
* **One-Click Download:** Dedicated route to grab your ready-to-fabricate SVG panels.
* **Smart Storage Management:** Integrated automatic cleanup that purges temp files older than 7 days to keep your server lean.
* **Production Ready:** Fully Dockerized and easily deployable behind reverse proxies like **Nginx Proxy Manager**.

---

## �� Quick Start with Docker Compose

No need to struggle with local Python environments or missing system libraries. Everything is packaged into a lightweight Docker container.

	### 1. Run the Application
Clone this repository, navigate to the folder, and fire it up:

```bash
docker compose up -d --build
```

### 2. Accessing the Dashboard
By default, the web interface will be exposed on port `8060`. Open your browser and navigate to:
``http://localhost:8060`` (or ``http://your-server-ip:8060``)

---

## 🔒 Production Deployment (Nginx Proxy Manager)

If you want to secure your dashboard behind a domain name with HTTPS via **Nginx Proxy Manager**, it is highly recommended to isolate the container ports and attach it to your proxy network.

You can achieve this by creating `docker-compose.override.yml` file (keep it out of Git!) to map your existing external proxy network:

```yaml
version: '3.8'

services:
  kumiko_app:
    ports: []
    networks:
      - your_proxy_network

networks:
  your_proxy_network:
    external: true
```

Inside Nginx Proxy Manager, configure your Proxy Host with:
* **Forward Hostname/IP:** `kumiko_app`
* **Forward Port:** `8000` *(Internal FastAPI port)*

---

## 🚛 Dashboard Settings Explained

### ↔ Grid Resolution (Width & Height)
Controls both the grid density and panel aspect ratio.
* *Note on Geometry:* Kumiko triangles are naturally wider than they are tall. To prevent visual stretching, adjust your grid dimensions (Columns x Rows) to roughly match the aspect ratio of your source image.

### 📒 Hexagon Orientation
Toggle between **Pointy** (vertices pointing up) and **Flat** (flat edges on top) arrangements to match your physical 3D-printed backing grids.

### �8 Prominent Colors Amount
Controls how many dominant colors the algorithm extracts from your picture.
* **Tip:** 5 colors are highly recommended for optimal results (usually 4 filament colors + 1 background color).

### ⿻ Filament & Background Customization
+ **Background Color:** Sets the canvas color behind the inserts.
* **Border Color:** Matches the structural grid filament you plan to use for printing the outlines.
* **Exclude Background:** If set to *Yes*, the generator skips creating intricate patterns in solid background areas, saving you tons of printing time and filament.

---

## 📂 Project Structure

```text
. 
✜── main_api.py             # Tailored execution script for the Web UI
*✜── web_app.py              # FastAPI Backend server & cleanup routine
✜── templates/
Ⓞ   ✜── index.html          # Responsive, multilingual Frontend dashboard with CSS spinner
✜── translations.json       # i18n Dictionary (EN / FR / DE)
✜── docker-compose.yml      # Docker stack configuration
✜── Dockerfile              # Isolated environment definition
✜── main.py                 # Original CLI entry point
✜── config.py               # Legacy configuration file
✜── geometry/               # Grid generation & mapping mechanics
✜── image/                  # Sampling & color extraction core
└── rendering/              # SVG compilation layer
```

---

## 📭 Credits & License

* **Original Algorithm:** Kudos to [hampusudd](https://github.com/hampusudd) for the brilliant feature-based pattern classification logic.
* **Modifications & Web Stack:** Remastered by Séb.
* **License:** This project is open-source and licensed under the MIT License.
