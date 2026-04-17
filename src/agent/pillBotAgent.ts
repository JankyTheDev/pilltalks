import { AgentReply, ChatMessage } from "./types";

type PillBotOptions = {
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
  botUserId?: string;
};

const MAX_REPLY_LENGTH = 280;
const SAFETY_PATTERNS = [/private key/i, /seed phrase/i, /send (me|us) sol/i, /guaranteed profit/i];

export class PillBotAgent {
  private readonly botName: string;
  private readonly botDisclosure: string;
  private readonly botSystemPrompt: string;
  private readonly projectName: string;
  private readonly projectWebsite?: string;
  private readonly projectX?: string;
  private readonly projectTelegram?: string;
  private readonly contractAddress?: string;
  private readonly allowedRooms: Set<string>;
  private readonly aiMode: "off" | "template";
  private readonly botUserId?: string;

  constructor(options: PillBotOptions) {
    this.botName = options.botName;
    this.botDisclosure = options.botDisclosure;
    this.botSystemPrompt = options.botSystemPrompt;
    this.projectName = options.projectName;
    this.projectWebsite = options.projectWebsite;
    this.projectX = options.projectX;
    this.projectTelegram = options.projectTelegram;
    this.contractAddress = options.contractAddress;
    this.allowedRooms = new Set(options.allowedRooms);
    this.aiMode = options.aiMode;
    this.botUserId = options.botUserId;
  }

  describe(): string {
    return `${this.botName}: ${this.botSystemPrompt}`;
  }

  async handleMessage(message: ChatMessage): Promise<AgentReply | null> {
    if (!this.allowedRooms.has(message.roomId)) {
      return null;
    }

    if (this.botUserId && message.userId === this.botUserId) {
      return null;
    }

    const text = message.text.trim();
    if (!text) {
      return null;
    }

    const safetyReply = this.checkSafety(text);
    if (safetyReply) {
      return {
        roomId: message.roomId,
        text: safetyReply,
        replyToMessageId: message.id,
      };
    }

    const lowered = text.toLowerCase();
    if (!this.shouldRespond(lowered)) {
      return null;
    }

    return {
      roomId: message.roomId,
      text: this.composeReply(message.username, text, lowered),
      replyToMessageId: message.id,
    };
  }

  private checkSafety(text: string): string | null {
    if (SAFETY_PATTERNS.some((pattern) => pattern.test(text))) {
      return `${this.botDisclosure} Never share keys, seed phrases, or funds in chat or DMs. Use only official public links.`;
    }

    return null;
  }

  private shouldRespond(lowered: string): boolean {
    return (
      lowered.includes("pillbot") ||
      lowered.includes("help") ||
      lowered.includes("what is this") ||
      lowered.includes("contract") ||
      lowered === "ca" ||
      lowered.includes("website") ||
      lowered.includes("twitter") ||
      lowered.includes("x.com") ||
      lowered.includes("telegram") ||
      lowered.includes("tg") ||
      lowered.includes("buy") ||
      lowered.includes("launch") ||
      lowered.includes("where") ||
      lowered.includes("how")
    );
  }

  private composeReply(username: string, original: string, lowered: string): string {
    if (lowered.includes("what is this")) {
      return `${this.botDisclosure} I answer basic ${this.projectName} questions and public info in live chat.`;
    }

    if (lowered.includes("contract") || lowered === "ca") {
      return this.contractAddress
        ? `${this.botDisclosure} ${this.projectName} contract address: ${this.contractAddress}`
        : `${this.botDisclosure} Contract address is not configured yet.`;
    }

    if (lowered.includes("website")) {
      return this.projectWebsite
        ? `${this.botDisclosure} Website: ${this.projectWebsite}`
        : `${this.botDisclosure} Website is not configured yet.`;
    }

    if (lowered.includes("twitter") || lowered.includes("x.com")) {
      return this.projectX
        ? `${this.botDisclosure} X/Twitter: ${this.projectX}`
        : `${this.botDisclosure} X/Twitter link is not configured yet.`;
    }

    if (lowered.includes("telegram") || lowered.includes("tg")) {
      return this.projectTelegram
        ? `${this.botDisclosure} Telegram: ${this.projectTelegram}`
        : `${this.botDisclosure} Telegram link is not configured yet.`;
    }

    if (lowered.includes("buy")) {
      return `${this.botDisclosure} I can point to public project links and contract info, but I do not give buy or sell advice.`;
    }

    if (this.aiMode === "template") {
      const reply = `${this.botDisclosure} ${username}, I can help with ${this.projectName} links, contract lookup, launch basics, and chat safety. You asked: "${original}"`;
      return reply.length <= MAX_REPLY_LENGTH
        ? reply
        : `${this.botDisclosure} ${username}, I can help with ${this.projectName} links, contract lookup, launch basics, and chat safety.`;
    }

    return `${this.botDisclosure} ${username}, ask about contract info, links, launch basics, or chat safety.`;
  }
}
