from fastapi import FastAPI, Request
import httpx

app = FastAPI()

@app.get("/{path:path}")
async def proxy(request: Request, path: str):
    url = f"http://{path}"

    async with httpx.AsyncClient() as client:
        proxy_request = client.build_request(
            request.method, url, headers=dict(request.headers), content=await request.body()
        )
        proxy_response = await client.send(proxy_request)
    
    return proxy_response

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
