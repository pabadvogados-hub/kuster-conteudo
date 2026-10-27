/**
 * Monta o video final a partir de um edit.json.
 *
 *   node editar.mjs <nome-do-corte>            vertical 1080x1920 (Reels/Shorts/TikTok)
 *   node editar.mjs <nome-do-corte> --largo    horizontal 1920x1080 (YouTube)
 *
 * Espera encontrar:
 *   edits/<nome-do-corte>/edit.json     as decisoes de edicao
 *   public/<video do edit.json>         a gravacao bruta
 *   public/<captions do edit.json>      as palavras com tempo (gerado por: npm run legendar)
 *
 * Resultado: edits/<nome-do-corte>/final.mp4
 */
import { execFileSync } from "node:child_process";
import { existsSync, readFileSync, mkdtempSync, writeFileSync } from "node:fs";
import { tmpdir } from "node:os";
import path from "node:path";

const args = process.argv.slice(2);
const largo = args.includes("--largo");
const nome = args.find((a) => !a.startsWith("--"));

if (!nome) {
  console.error("Uso: node editar.mjs <nome-do-corte> [--largo]");
  process.exit(1);
}

const pastaEdit = path.join(process.cwd(), "edits", nome);
const arquivoEdit = path.join(pastaEdit, "edit.json");

if (!existsSync(arquivoEdit)) {
  console.error(`Nao achei ${path.relative(process.cwd(), arquivoEdit)}.`);
  console.error("Copie edits/EXEMPLO/edit.json para uma pasta nova e preencha.");
  process.exit(1);
}

const edit = JSON.parse(readFileSync(arquivoEdit, "utf-8"));

const faltando = [];
for (const chave of ["video", "captions", "accent", "ranges"]) {
  if (edit[chave] === undefined) faltando.push(chave);
}
if (faltando.length) {
  console.error(`Faltam campos no edit.json: ${faltando.join(", ")}`);
  process.exit(1);
}
for (const chave of ["video", "captions"]) {
  const arquivo = path.join(process.cwd(), "public", edit[chave]);
  if (!existsSync(arquivo)) {
    console.error(`Nao achei public/${edit[chave]}.`);
    if (chave === "captions") console.error("Rode antes: npm run legendar");
    process.exit(1);
  }
}
if (!Array.isArray(edit.ranges) || edit.ranges.length === 0) {
  console.error("O edit.json nao tem nenhum trecho em 'ranges' - nada a montar.");
  process.exit(1);
}

const props = {
  video: edit.video,
  captions: edit.captions,
  accent: edit.accent,
  ranges: edit.ranges,
  hook: edit.hook ?? null,
  callouts: edit.callouts ?? [],
  showCaptions: edit.showCaptions ?? true,
};

const arquivoProps = path.join(mkdtempSync(path.join(tmpdir(), "edit-")), "props.json");
writeFileSync(arquivoProps, JSON.stringify(props), "utf-8");

const saida = path.join(pastaEdit, "final.mp4");
const duracao = edit.ranges.reduce((n, r) => n + (r.toMs - r.fromMs), 0) / 1000;

console.log(`Corte: ${nome}`);
console.log(`${edit.ranges.length} trecho(s), ${duracao.toFixed(1)}s de video final`);
console.log(`Formato: ${largo ? "1920x1080 (largo)" : "1080x1920 (vertical)"}`);

execFileSync(
  process.platform === "win32" ? "npx.cmd" : "npx",
  ["remotion", "render", largo ? "Wide" : "Short", saida, `--props=${arquivoProps}`],
  { stdio: "inherit" },
);

console.log(`\nPronto: ${path.relative(process.cwd(), saida)}`);
