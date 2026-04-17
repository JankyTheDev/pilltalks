import "dotenv/config";

import { PillBotAgent } from "./agent/pillBotAgent";
import { loadConfig } from "./config";
import { ChatTransport } from "./transports/chatTransport";
import { PumpfunLiveTransport } from "./transports/pumpfunLiveTransport";
import { StdinTransport } from "./transports/stdinTransport";

async function main() {
  const config = loadConfig(process.argv.slice(2));

  const agent = new PillBotAgent({
    botName: config.botName,
    botDisclosure: config.botDisclosure,
    botSystemPrompt: config.botSystemPrompt,
    projectName: config.projectName,
    projectWebsite: config.projectWebsite,
    projectX: config.projectX,
    projectTelegram: config.projectTelegram,
    contractAddress: config.contractAddress,
    allowedRooms: config.allowedRooms,
    aiMode: config.aiMode,
    botUserId: config.pumpfunBotUserId,
  });

  const transport: ChatTransport =
    config.transport === "pumpfun-live"
      ? new PumpfunLiveTransport({
          streamUrl: config.pumpfunStreamUrl,
          sendUrl: config.pumpfunSendUrl,
          apiKey: config.pumpfunApiKey,
        })
      : new StdinTransport();

  console.log(`Starting ${agent.describe()} on transport "${transport.name}"`);

  await transport.connect(async (message) => {
    const reply = await agent.handleMessage(message);
    if (!reply) {
      return;
    }

    await transport.sendMessage(reply);
  });
}

main().catch((error) => {
  console.error("Startup failed:", error);
  process.exit(1);
});
