from fastapi import FastAPI, Request, Response
import httpx

app = FastAPI()

@app.get("/{path:path}")
async def proxy(request: Request, path: str):
    url = f"http://{path}"

    try:
        async with httpx.AsyncClient() as client:
            proxy_request = client.build_request(
                request.method, url, headers=dict(request.headers), content=await request.body()
            )
            proxy_response = await client.send(proxy_request)
        
        return Response(
            content=proxy_response.content,
            status_code=proxy_response.status_code,
            headers=dict(proxy_response.headers)
        )
    except httpx.RequestError as e:
        return Response(
            content=f"An error occurred while requesting {url}: {str(e)}",
            status_code=500
        )

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
