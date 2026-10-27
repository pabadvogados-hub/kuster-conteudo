// Opcoes: https://remotion.dev/docs/config
import { Config } from "@remotion/cli/config";

Config.setRspack(true);
Config.setVideoImageFormat("jpeg");
Config.setOverwriteOutput(true);

// Em maquina Windows com Chrome instalado, o render fica mais rapido usando o Chrome local.
// Se o caminho abaixo nao existir na sua maquina, nao precisa mexer: o Remotion baixa o proprio
// navegador na primeira renderizacao. Para apontar outro caminho, use a variavel de ambiente
// CHROME_PATH antes de rodar o comando.
Config.setChromiumOpenGlRenderer("angle");
if (process.env.CHROME_PATH) {
  Config.setBrowserExecutable(process.env.CHROME_PATH);
  Config.setChromeMode("chrome-for-testing");
}
