

run:
	@echo "Starting backend and frontend..."
	@uv run uvicorn Backend.app.main:app --reload & \
	cd Frontend && npm run dev
