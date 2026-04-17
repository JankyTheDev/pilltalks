export type AppConfig = {
  botName: string;
  botDisclosure: string;
  botSystemPrompt: string;
  projectName: string;
  projectWebsite?: string;
  projectX?: string;
  projectTelegram?: string;
  contractAddress?: string;
  allowedRooms: string[];
  aiMode: "off" | "template";
  transport: "stdin" | "pumpfun-live";
  pumpfunStreamUrl?: string;
  pumpfunSendUrl?: string;
  pumpfunApiKey?: string;
  pumpfunBotUserId?: string;
};

function getEnv(name: string): string | undefined {
  const value = process.env[name];
  if (!value) {
    return undefined;
  }

  const trimmed = value.trim();
  return trimmed.length > 0 ? trimmed : undefined;
}

export function loadConfig(argv: string[]): AppConfig {
  const transportArg = argv.find((arg) => arg.startsWith("--transport="));
  const transport = transportArg?.split("=")[1] ?? getEnv("TRANSPORT") ?? "stdin";

  if (transport !== "stdin" && transport !== "pumpfun-live") {
    throw new Error(`Unsupported transport "${transport}". Use "stdin" or "pumpfun-live".`);
  }

  return {
    botName: getEnv("BOT_NAME") ?? "PillBot",
    botDisclosure:
      getEnv("BOT_DISCLOSURE") ??
      "PillBot is an automated account for public pump.fun chat support. Not financial advice.",
    botSystemPrompt:
      getEnv("BOT_SYSTEM_PROMPT") ??
      "You are PillBot. You are a disclosed automated account. Be concise, useful, and never pretend to be human.",
    projectName: getEnv("PROJECT_NAME") ?? "Pill Project",
    projectWebsite: getEnv("PROJECT_WEBSITE"),
    projectX: getEnv("PROJECT_X"),
    projectTelegram: getEnv("PROJECT_TELEGRAM"),
    contractAddress: getEnv("CONTRACT_ADDRESS"),
    allowedRooms: (getEnv("ALLOWED_ROOMS") ?? "general")
      .split(",")
      .map((room) => room.trim())
      .filter(Boolean),
    aiMode: getEnv("AI_MODE") === "off" ? "off" : "template",
    transport,
    pumpfunStreamUrl: getEnv("PUMPFUN_STREAM_URL"),
    pumpfunSendUrl: getEnv("PUMPFUN_SEND_URL"),
    pumpfunApiKey: getEnv("PUMPFUN_API_KEY"),
    pumpfunBotUserId: getEnv("PUMPFUN_BOT_USER_ID"),
  };
}
