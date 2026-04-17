export type ChatMessage = {
  id: string;
  roomId: string;
  userId: string;
  username: string;
  text: string;
  timestamp: string;
};

export type AgentReply = {
  roomId: string;
  text: string;
  replyToMessageId?: string;
};
