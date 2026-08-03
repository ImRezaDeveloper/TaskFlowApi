set -e  # اگه خطایی باشه، متوقف کن

echo "🔍 Running ruff check --fix ..."
ruff check --fix .

echo "🎨 Running ruff format ..."
ruff format .

echo "✅ Done!"