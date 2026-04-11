"""Импорты для работы"""
import json
import tkinter as tk
from tkinter import filedialog
import base64
import os
from urllib.parse import quote_plus
import requests

# --- API URLs ---
TEXT_MODELS_URL = "https://text.pollinations.ai/models"
IMAGE_MODELS_URL = "https://image.pollinations.ai/models"
TEXT_GENERATION_OPENAI_URL = "https://text.pollinations.ai/openai" # OpenAI compatible endpoint
IMAGE_GENERATION_BASE_URL = "https://image.pollinations.ai/prompt/"

