import asyncio, sys, os, json
from playwright.async_api import async_playwright
EXE="/opt/pw-browsers/chromium_headless_shell-1194/chrome-linux/headless_shell"
FPS=25; TOTAL=53.6
async def run(layer, times, outdir):
    os.makedirs(outdir, exist_ok=True)
    async with async_playwright() as p:
        b=await p.chromium.launch(executable_path=EXE, args=["--allow-file-access-from-files"])
        pg=await b.new_page(viewport={"width":1080,"height":1920})
        await pg.goto("file:///home/user/edit/gfx/index.html"); await pg.evaluate("document.fonts.ready")
        await pg.wait_for_timeout(300)
        for fr,t in times:
            on=await pg.evaluate(f"render({t},'{layer}')")
            if on: await pg.screenshot(path=f"{outdir}/{fr:05d}.png", omit_background=True)
        await b.close()
if __name__=="__main__":
    layer=sys.argv[1]
    if sys.argv[2]=="all": times=[(i,round(i/FPS,4)) for i in range(int(TOTAL*FPS))]
    else: times=[(int(round(float(x)*FPS)),float(x)) for x in sys.argv[2].split(",")]
    asyncio.run(run(layer,times,sys.argv[3]))
