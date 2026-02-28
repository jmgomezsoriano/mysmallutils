import multiprocessing
import time
import unittest

import uvicorn
from deprecation import deprecated
from fastapi import FastAPI
from fastapi.responses import JSONResponse
from mysutils.request import retry_get, ServiceError

HOST = "127.0.0.1"
PORT = 8000
BASE_URL = f"http://{HOST}:{PORT}"


def create_test_app() -> FastAPI:
    app = FastAPI()

    @app.get("/ok")
    async def ok():
        return {"message": "Todo bien"}

    @app.get("/fail")
    async def fail():
        return JSONResponse(status_code=500, content={"error": "Internal Server Error"})

    return app


def run_server():
    app = create_test_app()
    uvicorn.run(app, host=HOST, port=PORT, log_level="error")


class RequestsTestCase(unittest.TestCase):
    def setUp(self):
        self.proc = multiprocessing.Process(target=run_server)
        self.proc.start()
        time.sleep(1.5)  # espera para que el servidor arranque

    def tearDown(self):
        if self.proc.is_alive():
            self.proc.terminate()
            self.proc.join()

    def test_retry_get(self):
        response = retry_get(f"{BASE_URL}/ok", num_tries=2)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {"message": "Todo bien"})

    def test_retry_try_on_status(self):
        with self.assertRaises(ServiceError) as ex:
            response = retry_get(f"{BASE_URL}/fail", num_tries=3, wait_time=0.1, statuses={500})
        self.assertEqual(ex.exception.status_code, 500)

    def test_retry_delete(self):
        response = retry_get(f"{BASE_URL}/ok", num_tries=2)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {"message": "Todo bien"})


if __name__ == '__main__':
    unittest.main()
