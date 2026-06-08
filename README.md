# Kumiko Generator

A modern and fluid web interface to transform your images into beautiful Kumiko patterns (traditional Japanese woodworking styles using geometric triangles and hexagons). This project is highly optimized to prepare models for 3D printing or laser cutting.

This project is a customized and containerized standalone fork of the original repository by [hampusudd/kumiko_generator](https://github.com/hampusudd/kumiko_generator).

## Features

- 1/3 - 2/3 Studio Layout: Fixed settings panel on the left, and a dynamic high-definition SVG live preview on the right.
- Unified Drag and Drop Zone: Drop your image anywhere in the box to load it instantly. No redundant clicks or double uploads.
- Force Grid Size (Auto-Crop): A crucial option for 3D printing. Automatically crops your image from the center to strictly respect your requested dimensions (e.g., 14x14) without distorting the geometric pattern.
- Native Multilingual Support: Instant on-the-fly toggling between French, English, and German.
- Built-in Security: Strict MIME-type checking on uploads to completely block any malicious scripts or execution attempts.
- Auto-Cleanup: An automatic internal routine that securely purges input images and rendered files older than 7 days.

## Quick Start and Installation (Docker)

The project is fully containerized. To spin it up on your local machine or seedbox, ensure you have Docker and Docker Compose installed, then run your build command:
docker compose up -d --build

The application will be accessible on the port configured in your docker-compose.yml file (defaulting to port 8000 or routed via your reverse proxy).

## Project Structure

- web_app.py: FastAPI backend server handling routing, security, PIL image auto-cropping, and cron cleanup.
- templates/index.html: Fully responsive frontend dashboard with advanced Drag and Drop and a built-in i18n translation dictionary.
- main_api.py: Core mathematical script generating the vector Kumiko wireframes.
- input_images/: Temporary storage for uploaded source images (purged every 7 days).
- output_svg/: Temporary storage for generated SVG blueprints (purged every 7 days).
