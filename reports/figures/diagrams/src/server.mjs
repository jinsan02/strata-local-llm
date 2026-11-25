// 구조도 PNG 내보내기용 로컬 서버: 정적 파일 + POST /save?name=<이름>.png
import { createServer } from "node:http";
import { readFileSync, writeFileSync, existsSync } from "node:fs";
import { join, dirname, basename } from "node:path";
import { fileURLToPath } from "node:url";

const here = dirname(fileURLToPath(import.meta.url));
const types = { ".html": "text/html; charset=utf-8", ".excalidraw": "application/json", ".json": "application/json", ".png": "image/png", ".ttf": "font/ttf" };
createServer((req, res) => {
  const u = new URL(req.url, "http://localhost");
  if (req.method === "POST" && u.pathname === "/save") {
    const name = basename(u.searchParams.get("name") || "");
    if (!/^[\w.-]+\.(png|svg|json)$/.test(name)) { res.writeHead(400).end("bad name"); return; }
    const chunks = [];
    req.on("data", (c) => chunks.push(c));
    req.on("end", () => { writeFileSync(join(here, "out", name), Buffer.concat(chunks)); res.writeHead(200).end("ok " + name); });
    return;
  }
  const p = join(here, basename(u.pathname === "/" ? "render.html" : u.pathname));
  if (!existsSync(p)) { res.writeHead(404).end(); return; }
  res.writeHead(200, { "Content-Type": types[p.slice(p.lastIndexOf("."))] || "application/octet-stream" }).end(readFileSync(p));
}).listen(5178, "127.0.0.1", () => console.log("listening 5178"));
