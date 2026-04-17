import { AgentReply, ChatMessage } from "../agent/types";

export type ChatTransport = {
  readonly name: string;
  connect(onMessage: (message: ChatMessage) => Promise<void>): Promise<void>;
  sendMessage(reply: AgentReply): Promise<void>;
  close(): Promise<void>;
};
