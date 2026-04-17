import { AgentReply, ChatMessage } from "../agent/types";
import { ChatTransport } from "./chatTransport";

type PumpfunLiveTransportOptions = {
  streamUrl?: string;
  sendUrl?: string;
  apiKey?: string;
};

export class PumpfunLiveTransport implements ChatTransport {
  readonly name = "pumpfun-live";
  private readonly streamUrl?: string;
  private readonly sendUrl?: string;
  private readonly apiKey?: string;

  constructor(options: PumpfunLiveTransportOptions) {
    this.streamUrl = options.streamUrl;
    this.sendUrl = options.sendUrl;
    this.apiKey = options.apiKey;
  }

  async connect(_onMessage: (message: ChatMessage) => Promise<void>): Promise<void> {
    if (!this.streamUrl) {
      throw new Error(
        "PUMPFUN_STREAM_URL is required for live mode. Replace connect() with your compliant pump.fun chat bridge.",
      );
    }

    throw new Error(
      "Live pump.fun transport is a scaffold only. Wire your websocket or event bridge into connect().",
    );
  }

  async sendMessage(_reply: AgentReply): Promise<void> {
    if (!this.sendUrl || !this.apiKey) {
      throw new Error(
        "PUMPFUN_SEND_URL and PUMPFUN_API_KEY are required for live replies. Replace sendMessage() with your compliant bridge.",
      );
    }

    throw new Error(
      "Live pump.fun sendMessage() is a scaffold only. Replace it with your approved send path.",
    );
  }

  async close(): Promise<void> {
    return;
  }
}
