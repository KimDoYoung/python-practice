.PHONY: clean

clean:
	@echo "Cleaning up __pycache__, .pyc, and .DS_Store files..."
	find ./backend -type d -name "__pycache__" -exec rm -rf {} +
	find ./backend -type f -name "*.pyc" -delete
	find . -type f -name ".DS_Store" -delete
	@echo "Clean up completed."
