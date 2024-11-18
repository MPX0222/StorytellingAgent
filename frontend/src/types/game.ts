export enum GamePhase {
  INTRO = 'intro',
  EXAM_HALL = 'exam_hall',
  HALLWAY = 'hallway',
  ROOFTOP = 'rooftop'
}

export interface GameState {
  currentTime: string;
  location: string;
  dialog: string;
  availableActions: string[];
  currentPhase: string;
  cycleCount: number;
  inExamHall: boolean;
  inDialogue: boolean;
  joeySaved: boolean;
  loading: boolean;
  messages: Array<{
    text: string;
    type: 'system' | 'user' | 'agent';
  }>;
}

export interface DialogueMessage {
  text: string;
  type: 'system' | 'user' | 'agent';
}

export interface Character {
  name: string;
  age: number;
  description: string;
}

export interface GameAction {
  actionType: string;
} 