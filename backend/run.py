import os
import uvicorn
from settings.server import app

if __name__ == "__main__":
    uvicorn.run(app, host=os.environ.get('APP_HOST', '0.0.0.0'), port=int(os.environ.get('APP_PORT', 2223)))