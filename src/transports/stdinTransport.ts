import readline from "readline";
import { randomBytes } from "crypto";

import { AgentReply, ChatMessage } from "../agent/types";
import { ChatTransport } from "./chatTransport";

export class StdinTransport implements ChatTransport {
  readonly name = "stdin";
  private rl?: readline.Interface;

  async connect(onMessage: (message: ChatMessage) => Promise<void>): Promise<void> {
    this.rl = readline.createInterface({
      input: process.stdin,
      output: process.stdout,
      prompt: "user> ",
    });

    console.log("PillBot local simulation started. Use Ctrl+C to stop.");

    this.rl.on("line", async (line: string) => {
      const message: ChatMessage = {
        id: randomBytes(16).toString("hex"),
        roomId: "general",
        userId: "local-user",
        username: "local-user",
        text: line,
        timestamp: new Date().toISOString(),
      };

      await onMessage(message);
      this.rl?.prompt();
    });

    this.rl.prompt();
  }

  async sendMessage(reply: AgentReply): Promise<void> {
    console.log(`${reply.roomId}> pillbot> ${reply.text}`);
  }

  async close(): Promise<void> {
    this.rl?.close();
  }
}
